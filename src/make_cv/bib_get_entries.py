#!/usr/bin/env python3
import json
import os
from scholarly import scholarly
from scholarly import ProxyGenerator

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.customization import convert_to_unicode
from bibtexparser.bparser import BibTexParser
from bibtexautocomplete.core import main as btac

import re
import string
import argparse
from datetime import date
import sys

from .bib_add_keywords import add_keyword

# pip3 install scholarly
# pip3 uninstall urllib3
# pip3 install 'urllib3<=2'

def getyear(paperbibentry):
	if "year" in paperbibentry.keys(): 
		return(int(paperbibentry["year"]))
	if "date" in paperbibentry.keys():
		return(int(paperbibentry["date"][:4]))
	return(0)

def bib_get_entries(bibfile,author_id,years,outputfile,scraper_id=None):

	newentries = []
	
	# Set up a ProxyGenerator object to use free proxies
	# This needs to be done only once per session
	# Helps avoid google scholar locking out 
	if scraper_id:
		pg = ProxyGenerator()
		success = pg.ScraperAPI(scraper_id)
		if success:
			print('ScraperAPI in use')
			scholarly.use_proxy(pg)
		
	# Get Google Scholar Data for Author	
	author = scholarly.search_author_id(author_id)
	author = scholarly.fill(author,sections=['indices','publications'])

	if years > 0:
		today = date.today()
		year = today.year
		begin_year = year - years
	else:
		begin_year = 0
		
	# Load bibfile
	# homogenize_fields: Sanitize BibTeX field names, for example change `url` to `link` etc.
	tbparser = BibTexParser(common_strings=True)
	tbparser.homogenize_fields = False  # no dice
	tbparser.alt_dict['url'] = 'url'    # this finally prevents change 'url' to 'link'
	tbparser.expect_multiple_parse = True
	with open(bibfile) as bibtex_file:
		bibtex_str = bibtex_file.read()
	
	bib_database = bibtexparser.loads(bibtex_str, tbparser)
	entries = bib_database.entries
	
	# Create list of titles in bibfile compressing out nonalphanumeric characters
	titles = [re.sub('[\\W_]', '', entry['title']).lower() if 'title' in entry.keys() else None for entry in entries]
	# Create list of google publication ids if they exist
	google_pub_ids = [entry["google_pub_id"] if "google_pub_id" in entry.keys() else None for entry in entries]
	
	# Set arguments for btac
	sys.argv.clear()
	sys.argv.append('')
	sys.argv.append('-i')
	sys.argv.append('-f')
	sys.argv.append('-m')
	sys.argv.append('btac.bib')
	
	useGoogle = False

	# Loop through google scholar entries
	for pub in author['publications']:
		if 'pub_year' in pub['bib']:
			year = pub['bib']['pub_year']
		else:
			continue
		
		if not(int(year) >= begin_year):
			continue
		
		# First try to match by publication id
		au_pub_id = pub['author_pub_id']
		pub_id = au_pub_id[au_pub_id.find(':')+1:]
		indices = [i for i, x in enumerate(google_pub_ids) if x == pub_id]
		if len(indices) == 1:
			# found match
			continue
		
		print('Should I try to find a match for:')
		print(pub['bib'])
		YN = input('Y/N?')
		if YN == 'N':
			continue
			
		
		if useGoogle:
			# Try to find bibtex record using google scholar
			query = scholarly.search_pubs(pub['bib']['title'])
			if (query):
				for pub in query:
					bibtex_str = scholarly.bibtex(pub)
					print(bibtex_str)
					YN = input('Is this entry correct and ready to be added?\nOnce an entry is added any future changes must be done manually.\n[Y/N]? ')
					if YN == 'Y':
						bib_database = bibtexparser.loads(bibtex_str, tbparser)
						bib_database.entries[-1]['google_pub_id'] = pub_id
						add_keyword(bib_database.entries[-1])
						newentries.append(bib_database.entries[-1]['ID'])
		else:
			# try to fill entry using bibtex autocomplete?
			with open('btac.bib','w') as tempfile:
				tempfile.write('@article{' +pub_id +',\n title={'+pub['bib']['title'] +'},\n}')
			tempfile.close()
			btac()
			with open('btac.bib') as bibtex_file:
				bibtex_str = bibtex_file.read()
			
			print(bibtex_str)
			YN = input('Is this entry correct and ready to be added?\nOnce an entry is added any future changes must be done manually.\n[Y/N]? ')
			if YN == 'Y':
				bib_database = bibtexparser.loads(bibtex_str, tbparser)
				bib_database.entries[-1]['google_pub_id'] = pub_id
				if 'booktitle' in bib_database.entries[-1].keys():
					bib_database.entries[-1]['ENTRYTYPE'] = 'inproceedings'
				elif 'note' in bib_database.entries[-1].keys():
					bib_database.entries[-1]['ENTRYTYPE'] = 'misc'
				add_keyword(bib_database.entries[-1])
				IDstring = re.search('^[A-z]+',bib_database.entries[-1]['author']).group(0)
				IDstring += year
				IDstring += re.search('^[A-z]+',bib_database.entries[-1]['title']).group(0)
				bib_database.entries[-1]['ID'] = IDstring
				newentries.append(bib_database.entries[-1]['ID'])
				
				
# 		journal = re.search('^[A-z. ]+',citestring).group(0)
# 		startpage = re.search('[0-9]+-',citestring).group(0)
# 		startpage = startpage[:len(startpage)-1]
# 		cite_title = 
# 
# 		# Try to match by title
# 		cite_title = re.sub('[\W_]', '', pub['bib']['title']).lower()
# 		citestring = pub['bib']['citation']
# 		
# 		indices = [i for i, x in enumerate(titles) if x == cite_title]
# 		if len(indices) == 1:
# 			# found match
# 			entries[indices[0]]['citations'] = str(ncites)
# 			entries[indices[0]]['google_pub_id'] = str(pub_id)
# 			continue
	
	writer = BibTexWriter()
	writer.order_entries_by = None
	with open(outputfile, 'w') as thebibfile:
		bibtex_str = bibtexparser.dumps(bib_database,writer)
		thebibfile.write(bibtex_str)
	
	if useGoogle:	
		sys.argv.clear()
		sys.argv.append('')
		sys.argv.append('-c')
		sys.argv.append('doi')
		sys.argv.append('-i')
		sys.argv.append('-e')
		sys.argv.append('')
		for entry in newentries:
			sys.argv[-1] = entry
			btac()
	
	for file in ['dump.text','btac.bib']:
		try:
			os.remove(file)
		except OSError as err:
			print("")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This script adds citations counts to a bib file')
	parser.add_argument('-o', '--output',default="scholarship1.bib",help='the name of the output file')
	parser.add_argument('-y', '--years',default="1",type=int,help='the number of years to go back, default is 1 year')
	parser.add_argument('bibfile',help='the .bib file to add the citations to')
	parser.add_argument('-a', '--author_id',default="",help='the google scholar id for the author. If not provided it will look for a file titled "google_id" in the current working directory')
	parser.add_argument('-s', '--scraperID',help='A scraper ID in case Google Scholar is blocking requests')          
	args = parser.parse_args()
	
	if (not args.author_id):
		with open("google_id") as google_file:
			args.author_id = google_file.readline().strip('\n\r')
		
	bib_get_entries(args.bibfile,args.author_id,args.years,args.output,args.scraperID)
	

		
	
# my Google Scholar ID: 'm_of3wYAAAAJ'
# my scraperAPI API key '4ea7a522ac7475f907fe6595bb2a38dd'
	

	
	





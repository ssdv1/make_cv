#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# writes latex files for creating bibliography
# Usually run from CV/Tables folder like this
# pubs2latex_far.py ../../Scholarship/scholarship.bib

import os, sys
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.customization import convert_to_unicode
from bibtexparser.bparser import BibTexParser
from datetime import date
import argparse
import numpy as np

categories = ["journal","conference","patent","book","invited","refereed"]

def getyear(paperbibentry):
	if "year" in paperbibentry.keys(): 
		return(int(paperbibentry["year"]))
	if "date" in paperbibentry.keys():
		return(int(paperbibentry["date"][:4]))
	return(0)

def main(f,years,inputfile):

	nrecord = np.zeros(len(categories))

	# homogenize_fields: Sanitize BibTeX field names, for example change `url` to `link` etc.
	tbparser = BibTexParser(common_strings=True)
	tbparser.homogenize_fields = False  # no dice
	tbparser.alt_dict['url'] = 'url'    # this finally prevents change 'url' to 'link'

	try:
		bibtex_file = open(inputfile)
		bibtex_str = bibtex_file.read()
		bib_database = bibtexparser.loads(bibtex_str, tbparser)
		bib_database.entries = sorted(bib_database.entries, key=lambda k: getyear(k), reverse=True)	
	except OSError:
		print("Could not open/read file: " +inputfile)
		return(nrecord)

	if years > 0:
		today = date.today()
		year = today.year
		begin_year = year - years
	else:
		begin_year = 0

	for count,etype in enumerate(categories):
		f[count].write("\\begin{enumerate}\n")

	for icpbe, paperbibentry in enumerate(bib_database.entries):
		year = getyear(paperbibentry)
		if not(year >= begin_year):
			continue
	
		if "keywords" in paperbibentry.keys():
			kword = str(paperbibentry["keywords"])
			for count,etype in enumerate(categories):
				if kword.find(etype) > -1:
					f[count].write("\\item\n\\fullcite{"+paperbibentry["ID"]+"}\n")
					nrecord[count] += 1

	for count,etype in enumerate(categories):
		f[count].write("\\end{enumerate}\n")

	return(nrecord)
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This script outputs bibliographic latex citations to a latex table for (journals,refereed conferences,conferences,patents,books,invited talks) received in the last [YEARS] years')
	parser.add_argument('-y', '--years',default="0",type=int,help='the number of years to output, default is all')
	parser.add_argument('-a', '--append', action='store_const',const="a",default="w")
	parser.add_argument('-e', '--ending',default="_far",type=str,help='ending to append to filenames')
	parser.add_argument('inputfile',help='the input bibliography file name')
	parser.add_argument('outputpath',help='the input bibliography file name')         
	args = parser.parse_args()
	
	f = [open(args.outputpath +os.sep +etype+args.ending+".tex", args.append) for count,etype in  enumerate(categories)]	
	necord = main(f,args.years,args.inputfile)
	
	for count,etype in enumerate(categories):
		f[count].close()
		if (necord[count] == 0):	
			os.remove(args.outputpath +os.sep +etype+args.ending+".tex")
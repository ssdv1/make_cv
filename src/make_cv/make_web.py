#! /usr/bin/env python3
# Script to create cv
# must be executed from Faculty/CV folder
# script folder must be in path

import os
import sys
import glob
import pandas as pd
import platform
import shutil

# Source is faculty folder
if platform.system() == 'Windows':
	faculty_source = r"S:\departments\Mechanical & Aeronautical Engineering\Faculty"
	gathered_source = r"S:\departments\Mechanical & Aeronautical Engineering\Confidential Information\Department Data"
	sys.path.insert(0, r"S:\departments\Mechanical & Aeronautical Engineering\Faculty\_Scripts")	
else:
	faculty_source = r"/Volumes/Mechanical & Aerospace Engineering/Faculty"
	gathered_source = r"/Volumes/Mechanical & Aerospace Engineering/Confidential Information/Department Data"
	sys.path.insert(0, r"/Volumes/Mechanical & Aerospace Engineering/Faculty/_Scripts")

# override faculty source to be relative to CV folder
faculty_source = ".."

# default to writing entire history
years = 0

import grants2latex_far
import props2latex_far
import UR2latex
import bib2latex_far
import thesis2latex_far
import personal_awards2latex
import student_awards2latex
import service2latex
import publons2latex
import teaching2latex
import publons2excel

if not os.path.exists('Tables'):
	os.makedirs('Tables')
		
# open files
fgrants = open('Tables' +os.sep +'grants.tex', 'w') # file to write
fprops = open('Tables' +os.sep +'proposals.tex', 'w') # file to write
fur = open('Tables' +os.sep +'UR.tex', 'w') # file to write
pubfiles = ["journal.tex","conference.tex","patent.tex","book.tex","invited.tex","refereed.tex"]
fpubs = [open('Tables' +os.sep +name, 'w') for name in pubfiles]
fthesis = open('Tables' +os.sep +'thesis.tex', 'w') # file to write
fpawards = open('Tables' +os.sep +'personal_awards.tex', 'w') # file to write
fsawards = open('Tables' +os.sep +'student_awards.tex', 'w') # file to write
fservice = open('Tables' +os.sep +'service.tex', 'w') # file to write
freviews = open('Tables' +os.sep +'reviews.tex', 'w') # file to write
fteaching = open('Tables' +os.sep +'teaching.tex', 'w') # file to write
	
	
# Grants
filename = faculty_source +os.sep +"Proposals & Grants" +os.sep +"proposals & grants.xlsx"
nrows = grants2latex_far.main(fgrants,years,filename)
fgrants.close()
if not(nrows):
	os.remove('Tables' +os.sep +'grants.tex')

# Proposals
nrows = props2latex_far.main(fprops,years,filename)	
fprops.close()
if not(nrows):
	os.remove('Tables' +os.sep +'proposals.tex')

# Undergraduate Research
filename = faculty_source +os.sep +"Service" +os.sep +'undergraduate research data.xlsx'
nrows = UR2latex.main(fur,years,filename)	
fur.close()
if not(nrows):
	os.remove('Tables' +os.sep +'UR.tex')

# Scholarly Works
filename = faculty_source +os.sep +"Scholarship" +os.sep +'scholarship.bib'
if os.path.isfile(filename):
	nrecords = bib2latex_far.main(fpubs,years,filename)
	for counter in range(len(pubfiles)):
		fpubs[counter].close()
		if not(nrecords[counter]):
			os.remove('Tables'+os.sep +pubfiles[counter])

# Thesis Publications & Graduate Advisees
filename1 = faculty_source +os.sep +"Scholarship" +os.sep +'current student data.xlsx'
filename2 = faculty_source +os.sep +"Scholarship" +os.sep +'thesis data.xlsx'
nrows = thesis2latex_far.main(fthesis,years,filename1,filename2)
fthesis.close()
if not(nrows):
	os.remove('Tables'+os.sep +'thesis.tex')

# Personal Awards
filename = faculty_source +os.sep +"Awards" +os.sep +'personal awards data.xlsx'
nrows = personal_awards2latex.main(fpawards,years,filename)
fpawards.close()
if not(nrows):
	os.remove('Tables'+os.sep +'personal_awards.tex')

# Student Awards
filename = faculty_source +os.sep +"Awards" +os.sep +'student awards data.xlsx'
nrows = student_awards2latex.main(fsawards,years,filename)	
fsawards.close()
if not(nrows):
	os.remove('Tables'+os.sep +'student_awards.tex')

# Service Activities
filename = faculty_source +os.sep +"Service" +os.sep +'service data.xlsx'
nrows = service2latex.main(fservice,years,filename)	
fservice.close()
if not(nrows):
	os.remove('Tables'+os.sep +'service.tex')

# Reviewing Activities
jsonfiles = glob.glob(faculty_source +os.sep +"Service" +os.sep +"*.json")
print(jsonfiles)
if len(jsonfiles) == 1:
	publons2excel.main(jsonfiles[0],"reviews data.xlsx")
	os.remove(jsonfiles[0])

filename = faculty_source +os.sep +"Service" +os.sep +'reviews data.xlsx'
nrows = publons2latex.main(freviews,years,filename)
freviews.close()
if not(nrows):
	os.remove('Tables'+os.sep +'reviews.tex')
	
# Teaching
filename = faculty_source +os.sep +"Teaching" +os.sep +'teaching evaluation data.xlsx'
nrows = teaching2latex.main(fteaching,years,filename)	
fteaching.close()
if not(nrows):
	os.remove('Tables'+os.sep +'teaching.tex')

import subprocess

#mk4ht htlatex wepbage.tex 'xhtml,charset=utf-8,pmathml' ' -cunihtf -utf8 -cvalidate'
#biber webpage.bcf
#mk4ht htlatex wepbage.tex 'xhtml,charset=utf-8,pmathml' ' -cunihtf -utf8 -cvalidate'

subprocess.run(["mk4ht", "htlatex", "webpage.tex", "xhtml,charset=utf-8,pmathml", "-cunihtf -utf8 -cvalidate"]) 
#subprocess.run(["biber", "webpage.bcf"]) 
#subprocess.run(["mk4ht", "htlatex", "webpage.tex", "\'xhtml,charset=utf-8,pmathml\'", "\' -cunihtf -utf8 -cvalidate\'"]) 
#subprocess.run(["mk4ht", "htlatex", "webpage.tex", "\'xhtml,charset=utf-8,pmathml\'", "\' -cunihtf -utf8 -cvalidate\'"]) 

# cleanup
for file in ["webpage.aux","webpage.bbl","weboage.bcf","webpage.blg","webpage.log","webpage.run.xml","webpage.4ct","webpage.4tc","webpage.dvi","webpage.idv","webpage.tmp","webpage.xref"]:
	try:
		os.remove(file)
	except OSError as err:
		print("")




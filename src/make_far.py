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

import grants2latex_far
import props2latex_far
import UR2latex_far
import bib2latex_far
import thesis2latex_far
import personal_awards2latex_far
import student_awards2latex_far
import service2latex_far
import publons2latex_far
import teaching2latex_far

years = 3

if not os.path.exists('Tables'):
	os.makedirs('Tables')
		
# open files
fgrants = open('Tables' +os.sep +'grants_far.tex', 'w') # file to write
fprops = open('Tables' +os.sep +'proposals_far.tex', 'w') # file to write
fur = open('Tables' +os.sep +'undergraduate_research_far.tex', 'w') # file to write
pubfiles = ["journal_far.tex","conference_far.tex","patent_far.tex","book_far.tex","invited_far.tex","refereed_far.tex"]
fpubs = [open('Tables' +os.sep +name, 'w') for name in pubfiles]
fthesis = open('Tables' +os.sep +'thesis_far.tex', 'w') # file to write
fpawards = open('Tables' +os.sep +'personal_awards_far.tex', 'w') # file to write
fsawards = open('Tables' +os.sep +'student_awards_far.tex', 'w') # file to write
fservice = open('Tables' +os.sep +'service_far.tex', 'w') # file to write
freviews = open('Tables' +os.sep +'reviews_far.tex', 'w') # file to write
fteaching = open('Tables' +os.sep +'teaching_far.tex', 'w') # file to write
	
	
# Grants
filename = faculty_source +os.sep +"Proposals & Grants" +os.sep +"proposals & grants.xlsx"
nrows = grants2latex_far.main(fgrants,years,filename)
fgrants.close()
if not(nrows):
	os.remove('Tables' +os.sep +'grants_far.tex')

# Proposals
nrows = props2latex_far.main(fprops,years,filename)	
fprops.close()
if not(nrows):
	os.remove('Tables' +os.sep +'proposals_far.tex')

# Undergraduate Research
filename = faculty_source +os.sep +"Service" +os.sep +'undergraduate research data.xlsx'
nrows = UR2latex_far.main(fur,years,filename)	
fur.close()
if not(nrows):
	os.remove('Tables' +os.sep +'undergraduate_research_far.tex')

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
	os.remove('Tables'+os.sep +'thesis_far.tex')

# Personal Awards
filename = faculty_source +os.sep +"Awards" +os.sep +'personal awards data.xlsx'
nrows = personal_awards2latex_far.main(fpawards,years,filename)
fpawards.close()
if not(nrows):
	os.remove('Tables'+os.sep +'personal_awards_far.tex')

# Student Awards
filename = faculty_source +os.sep +"Awards" +os.sep +'student awards data.xlsx'
nrows = student_awards2latex_far.main(fsawards,years,filename)	
fsawards.close()
if not(nrows):
	os.remove('Tables'+os.sep +'student_awards_far.tex')

# Service Activities
filename = faculty_source +os.sep +"Service" +os.sep +'service data.xlsx'
nrows = service2latex_far.main(fservice,years,filename)	
fservice.close()
if not(nrows):
	os.remove('Tables'+os.sep +'service_far.tex')

# Reviewing Activities
filename = faculty_source +os.sep +"Service" +os.sep +'reviews data.xlsx'
nrows = publons2latex_far.main(freviews,years,filename)
freviews.close()
if not(nrows):
	os.remove('Tables'+os.sep +'reviews_far.tex')
	
# Teaching
filename = faculty_source +os.sep +"Teaching" +os.sep +'teaching evaluation data.xlsx'
nrows = teaching2latex_far.main(fteaching,years,filename)	
fteaching.close()
if not(nrows):
	os.remove('Tables'+os.sep +'teaching_far.tex')

import subprocess

#subprocess.run(["pdflatex", "far.tex"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT) 
subprocess.run(["pdflatex", "far.tex"]) 
subprocess.run(["biber", "far.bcf"]) 
subprocess.run(["pdflatex", "far.tex"],stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT) 
print("trying to delete far.pdf file.  If this gets stuck, delete far.pdf yourself and it should continue")
print("If it doesn't continue after that, hit ctrl-c, delete cv.pdf and try again")
while True:
    try:
        os.remove("far.pdf")
        break
    except OSError as err:
        continue
subprocess.run(["pdflatex", "far.tex"]) 

# cleanup
for file in ["far.aux","far.bbl","far.bcf","far.blg","far.log","far.out","far.run.xml","far.toc","biblatex-dm.cfg"]:
	try:
		os.remove(file)
	except OSError as err:
		print("")



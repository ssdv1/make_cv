#! /usr/bin/env python3
# Script to create cv
# must be executed from Faculty/CV folder
# script folder must be in path
import os
import sys
import subprocess
import glob
import shutil
import configparser
import argparse

from .make_cv import make_cv_tables
from .make_cv import add_default_args
from .make_cv import process_default_args
from .make_cv import read_args
from .make_cv import sections

from .create_config import create_config
from .create_config import verify_config

def main(argv = None):
	parser = argparse.ArgumentParser(description='This script creates a cv using python and LaTeX plus provided data')
	add_default_args(parser)
	
	[configuration,args] = read_args(parser,argv)
	
	config = configuration['WEB']
	process_default_args(config,args)
	make_cv_tables(config,'Tables_web',0)
	
	with open('exclusions.tex', 'w') as exclusions:
		for section in sections:
			if not config.getboolean(section): exclusions.write('\\setboolean{' +section +'}{false}\n')
	
	with open('biblatex-dm.cfg', 'w') as configLatex:
		configLatex.write('\\DeclareDatamodelFields[type=field, datatype=integer, nullok=true]{citations}\n')
		configLatex.write('\\DeclareDatamodelEntryfields{citations}\n')
	
	subprocess.run(["mk4ht", "htlatex", "web.tex", "xhtml,charset=utf-8,pmathml", "-cunihtf -utf8 -cvalidate"]) 
	subprocess.run(["biber", "web.bcf"]) 
	subprocess.run(["mk4ht", "htlatex", "web.tex", "xhtml,charset=utf-8,pmathml", "-cunihtf -utf8 -cvalidate"]) 
	subprocess.run(["mk4ht", "htlatex", "web.tex", "xhtml,charset=utf-8,pmathml", "-cunihtf -utf8 -cvalidate"]) 

	# cleanup
	for file in ["web.aux","web.bbl","web.bcf","web.blg","web.log","web.run.xml","web.4ct","web.4tc","web.dvi","web.idv","web.tmp","web.xref","web.bdf.bbl","web.bdf.blg","web.lg","biblatex-dm.cfg","exclusions.tex"]:
		try:
			os.remove(file)
		except OSError as err:
			print("")

if __name__ == "__main__":
	main()

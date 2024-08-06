#!/usr/bin/env python

import configparser

sections = {'Journal','Refereed','Book','Conference','Patent','Invited','PersonalAwards','StudentAwards','Service','Reviews','GradAdvisees','UndergradResearch','Teaching','Grants','Proposals'} 

defaults = {'data_dir': '..',
				'GoogleID': '',
				'ScraperID': '',
				'UseScraper': 'false',
				'ReviewsFileJSON': 'reviews data.json',
				'UpdateCitations': 'false',
				'UpdateStudentMarkers': 'false',
				'GetNewScholarshipEntries': 'false',
				'SearchForDOIs': 'false',
				'ConvertJSON': 'false'}

files = {'ScholarshipFile': 'scholarship.bib',
			'PersonalAwardsFile': 'personal awards data.xlsx',
			'StudentAwardsFile': 'student awards data.xlsx',
			'ServiceFile': 'service data.xlsx',
			'ReviewsFile': 'reviews data.xlsx',
			'CurrentGradAdviseesFile':'current student data.xlsx',
			'GradThesesFile': 'thesis data.xlsx',
			'UndergradResearchFile': 'undergraduate research data.xlsx',
			'TeachingFile': 'teaching evaluation data.xlsx',
			'ProposalsFile': 'proposals & grants.xlsx',
			'GrantsFile': 'proposals & grants.xlsx'} 

folders = {'ScholarshipFolder': 'Scholarship',
			'PersonalAwardsFolder': 'Awards',
			'StudentAwardsFolder': 'Awards',
			'ServiceFolder': 'Service',
			'ReviewsFolder': 'Service',
			'CurrentGradAdviseesFolder':'Scholarship',
			'GradThesesFolder': 'Scholarship',
			'UndergradResearchFolder': 'Service',
			'TeachingFolder': 'Teaching',
			'ProposalsFolder': 'Proposals & Grants',
			'GrantsFolder': 'Proposals & Grants'} 
			
cv_keys = {'IncludeStudentMarkers': 'true',
			'IncludeCitationCounts': 'true'}

def verify_cv_config(config):
	
	for key in defaults:
		if not key in config.keys():
			print(key +' is missing from config file')
			return False
	
	for key in files:
		if not key in config.keys():
			print(key +' is missing from config file')
			return False
	
	for key in folders:
		if not key in config.keys():
			print(key +' is missing from config file')
			return False
			
	for key in cv_keys:
		if not key in config.keys():
			print(key +' is missing from config file')
			return False
			
	for key in sections:
		if not key in config.keys():
			print(key +' is missing from config file')
			return False
	
	return True

def create_config(filename):
	config = configparser.ConfigParser()
	config['DEFAULT'] = defaults		
	for key,value in files.items():
		config['DEFAULT'][key] = value

	for key,value in folders.items():
		config['DEFAULT'][key] = value
		
	config['CV'] = cv_keys
	for section in sections:
		config['CV'][section] = 'true'    

	with open(filename, 'w') as configfile:
	  config.write(configfile)
  
if __name__ == "__main__":
	create_config('cv.cfg')
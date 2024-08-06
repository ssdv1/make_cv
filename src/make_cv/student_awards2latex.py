#! /usr/bin/env python3

# Python code to scatter Undergraduate research data to faculty folders
# First argument is file to scatter, second argument is Faculty 
# scatter <file to scatter> <Faculty folder> 

# import modules
import pandas as pd
import os
import sys

from .stringprotect import str2latex
from .stringprotect import abbreviate_name_list

def student_awards2latex(f,years,inputfile):
	source = inputfile # file to read
	try:
		source_data = pd.read_excel(source,sheet_name="Data")
	except OSError:
		print("Could not open/read file: " + source)
		return
	
	if years > 0:
		today = date.today()
		year = today.year
		begin_year = year - years
		df = df[df['Year'].apply(lambda x: int(x)) >= begin_year]
	
	df = source_data.fillna('')
	df.sort_values(by=['Year','Title','Student'], inplace=True, ascending = [False,True,True])
	df.reset_index(drop=True,inplace=True)
	nrows = df.shape[0] 

	if (nrows > 0):
		#print(df.columns)

		f.write("\\begin{tabularx}{\\linewidth}{XXl}\nTitle & Student  & Year \\\\\n\\hline\n")
		count = 0
		while count < nrows:
			f.write(str2latex(df.loc[count,"Title"]) + " & " +abbreviate_name_list(df.loc[count,"Student"]) + " & " +str2latex(df.loc[count,"Year"]) +"\\\\\n")
			count += 1
	
		f.write("\\end{tabularx}\n")
	
	return(nrows)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This script outputs student awards data to a latex table for awards received in the last [YEARS] years')
	parser.add_argument('-y', '--years',default="0",type=int,help='the number of years to output, default is all')
	parser.add_argument('-a', '--append', action='store_const',const="a",default="w")
	parser.add_argument('inputfile',help='the input excel file name')           
	parser.add_argument('outputfile',help='the output latex table name')
	args = parser.parse_args()
	
	f = open(args.outputfile, args.append) # file to write
	nrows = student_awards2latex(f,args.years,args.inputfile)
	f.close()
	
	if (nrows == 0):
		os.remove(args.outputfile)
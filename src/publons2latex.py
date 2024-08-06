#! /usr/bin/env python3
# This script outputs reviewing data to a latex table
# that shows a list of journals reviewed for and the number of papers reviewed for each
# journal in the last 5 years
# 
# To run "publons2latex.py <filename> <outputname.txt>"

# import modules
import pandas as pd
import os
import sys
from datetime import datetime
from stringprotect import str2latex

def main(f,years,inputfile):
	source = inputfile  # file to read
	try:
		reviews = pd.read_excel(source,header=0)
	except OSError:
		print("Could not open/read file: " + source)
		return
		
	if years > 0:
		today = date.today()
		year = today.year
		begin_year = year - years
		reviews = reviews[reviews['Start'].apply(lambda x: x.year) >= begin_year]

	# Find start date
	yearmin = 3000
	for d in reviews["Start"]:
		year = d.year
		yearmin = min([year,yearmin])

	table = reviews.pivot_table(index=['Journal'], values=['Rounds'], aggfunc=('count','sum'),observed=False)
	table.reset_index(inplace=True)
	table.columns=['Journal','Reviews','Rounds']
	#print(table)
	nrows = table.shape[0] 

	if (nrows > 0):
		f.write("\\begin{tabularx}{\linewidth}{Xl}\nJournal & Reviews(Rounds)  \\\\\n\\hline\n")

		count = 0
		total_reviews = 0
		total_rounds = 0
		while count < nrows:
			f.write(str2latex(table.loc[count,"Journal"]) + " & " +str(table.loc[count,"Reviews"]) +"(" +str(table.loc[count,"Rounds"]) +")" +"\\\\\n")
			total_reviews += table.loc[count,"Reviews"]
			total_rounds += table.loc[count,"Rounds"]
			count += 1
	f.write("\\end{tabularx}\n")
	f.write("Reviews since " +str(yearmin)+ ": " +str(total_reviews) +"(" +str(total_rounds) +")")
	return(nrows)
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This script outputs reviewing data to a latex table in the last [YEARS] years')
	parser.add_argument('-y', '--years',default="0",type=int,help='the number of years to output, default is all')
	parser.add_argument('-a', '--append', action='store_const',const="a",default="w")
	parser.add_argument('inputfile',help='the input excel file name')           
	parser.add_argument('outputfile',help='the output latex table name')
	args = parser.parse_args()
	
	f = open(args.outputfile, args.append) # file to write
	nrows = main(f,args.years,args.inputfile)
	f.close()
	
	if (nrows == 0):
		os.remove(args.outputfile)
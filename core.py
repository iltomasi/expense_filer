#!/usr/bin/env python

import os
import yaml
import fnmatch
import pandas as pd
from argparse import ArgumentParser
import xlsxwriter


############################################################################
############################################################################
############################################################################

def load_bank():
	# with open("bank_info.yaml", 'r') as stream:
	# 	try:
	# 		print(yaml.load(stream))
	# 		return yaml.load(stream)
	# 	except yaml.YAMLError as exc:
	# 		print(exc)

	f = open("bank_info.yaml")

	dataMap = yaml.load(f)

	return dataMap

############################################################################
############################################################################
############################################################################

def generate_report(folder, date, event):
	#init 
	report = []

	print 'Processing folder ' + folder + ' for ' + event 


	for directory in os.listdir(folder):
		#print directory
		for root, dirnames, filenames in os.walk(os.path.join(folder,directory)):
			for filename in fnmatch.filter(filenames, '*.xlsx'):
				
				#get who the expense belongs to
				expensee = filename[11:13]
				#print expensee

				## get board member name
				if expensee == 'AT': 
					name = 'Alessandro'
				if expensee == 'TA': 
					name = 'Tiziano'
				if expensee == 'TB': 
					name = 'Bobo'
				if expensee == 'FB': 
					name = 'Francesco'
				if expensee == 'SP': 
					name = 'Sandip'


				print 'Processing ' + filename +  ' in ' + os.path.join(folder,directory)
				temp = process_excel(os.path.join(folder,directory,filename),expensee)
				temp['REASON'] = date + name + event
				report.append(temp)


	return report

############################################################################
############################################################################
############################################################################


def process_excel(excel_file, who_is_expensing):
	bank_details = load_bank()
	#print bank_details[who_is_expensing]
	person = os.path.basename(os.path.normpath(excel_file))

	print '### ' + excel_file
	print 'Opening Excel file ' + excel_file
	df = pd.read_excel(excel_file , header=None)

	#retrieve amount from excel file
	amount = scan_excel_content(df)

	bank_details[who_is_expensing]['AMOUNT'] = amount

	#print amount
	#print '*' * 100

	return bank_details[who_is_expensing]

############################################################################
############################################################################
############################################################################


def scan_excel_content(df):
	#get excel dimensions
	[x,y] = df.shape 
	#print 'x_max: ' + str(x) + ' y_max '+ str(y)
	
	curr_x = 0
	curr_y = 0
	while curr_y < y:
		while curr_x < x:
			#print curr_x,curr_y
			#print df.iloc[curr_x,curr_y]

			#look for Total cost (to be reimbursed) and return cell next to it
			if df.iloc[curr_x,curr_y] == 'Total cost (to be reimbursed)':
				return df.iloc[curr_x,curr_y+1]


			curr_x = curr_x + 1 

		curr_x = 0 
		curr_y = curr_y + 1 



############################################################################
############################################################################
############################################################################

def save_to_file(report,filename):
	print 'Saving'
	print(report)
	#"sort dictionary": ACCOUNT HOLDER, SWIFT, IBAN and AMOUNT


	for item in report:
		print item

		f = open('./outputs/' + filename, 'a')
		f.write('ACCOUNT HOLDER: ' + item['ACCOUNT_HOLDER'] + '\n')
		f.write('SWIFT: ' + item['SWIFT'] + '\n')
		f.write('IBAN: ' + item['IBAN'] + '\n')
		f.write('AMOUNT: ' + str(item['AMOUNT']) + 'Euro\n')
		f.write('REASON: ' + str(item['REASON']) + '\n')
		f.write ('___' * 10 + '\n\n\n')
		f.close()

############################################################################
############################################################################
############################################################################


def create_excel(spreadsheet_name, expenses, event):

	# Create a workbook and add a worksheet.
	workbook = xlsxwriter.Workbook('./outputs/' + spreadsheet_name + '.xlsx')
	worksheet = workbook.add_worksheet()

	#add Title
	worksheet.write(0, 1, event)

	# Start from the first cell. Rows and columns are zero indexed.
	row = 1
	col = 0

	# Iterate over the data and write it out row by row.
	for item in (expenses):
		#round to two decimals
		amount = round(item['AMOUNT'],2)
		#comma separated, not dot separated
		amount_str = str(amount).replace('.',',')
		
		#print type(reason)
		worksheet.write(row, col,     item['ACCOUNT_HOLDER'] +' ' + event)
		worksheet.write(row, col + 1, item['REASON'])
		worksheet.write(row, col + 2, amount_str)
		row += 1

	# Write a total using a formula.
	worksheet.write(row, 0, 'Total')
	worksheet.write(row, 2, '=SUM(C1:C4)')

	workbook.close()


############################################################################
############################################################################
############################################################################

def assemble_email(event):
	filenames = ['email.txt', './outputs/' + event + '.txt']
	with open('./outputs/' +'email' + event +'.txt', 'w') as outfile:
	    for fname in filenames:
	        with open(fname) as infile:
	            for line in infile:
	                outfile.write(line)

############################################################################
############################################################################
############################################################################


if __name__ == "__main__":
	parser = ArgumentParser(description='Tool designed to create expense report for internal accounting.')
	parser.add_argument('--event',type=str, dest="event", required = True, default='', help='Directory where receipts are stored')
	parser.add_argument('--directory', type=str, required=True, dest="directory", default="", help='Format: <date>_EventName')    

	args = parser.parse_args()

	# print args.event
	# print args.directory

	if args.event != "" and args.directory != "":
		#event = '22102017_MasterSchoolKickOff'
		report = generate_report(args.directory, args.event.split('_')[0], args.event.split('_')[1])
		save_to_file(report, args.event + '.txt')
		create_excel(args.event, report, 'KickOff Helsinki')
		assemble_email(args.event)



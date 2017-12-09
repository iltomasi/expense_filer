import xlsxwriter

def create_excel(spreadsheet_name, expenses):

	# Create a workbook and add a worksheet.
	workbook = xlsxwriter.Workbook(spreadsheet_name + '.xlsx')
	worksheet = workbook.add_worksheet()

	# Start from the first cell. Rows and columns are zero indexed.
	row = 0
	col = 0

	# Iterate over the data and write it out row by row.
	for reason, item, cost in (expenses):
		worksheet.write(row, col,     reason)
		worksheet.write(row, col + 1,     item)
		worksheet.write(row, col + 2, cost)
		row += 1

	# Write a total using a formula.
	worksheet.write(row, 0, 'Total')
	worksheet.write(row, 2, '=SUM(C1:C4)')

	workbook.close()


if __name__ == '__main__':

	# Some data we want to write to the worksheet.
	expenses = (
	    ['Reason','Rent', 1000],
	    ['Reason','Gas',   100],
	    ['Reason', 'Food',  300],
	    ['Reason', 'Gym',    50],
	)

	create_excel('alessandro', expenses)
import xlrd, datetime
from glidenumber.desc import descriptionscrap
import json

loc = ("data.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(1)

start_date_list = []
end_date_list = []
 
items = []

for i in range(1, 5):
    
    start_date = xlrd.xldate_as_tuple(sheet.cell_value(i, 7), wb.datemode) 
    start_date = str(start_date[0]) + "/" + str(start_date[1]) + "/" + str(start_date[2])

    end_date = xlrd.xldate_as_tuple(sheet.cell_value(i, 8), wb.datemode) 
    end_date = str(end_date[0]) + "/" + str(end_date[1]) + "/" + str(end_date[2])

    country = sheet.cell_value(i, 2)
    item = descriptionscrap(country, start_date, end_date)
    if item is not None:
        items.append(item) 


'''
##############################################################
#ITEMS ARE NOW AVAILABLE AS LIST OF DICTIONARIES IN THIS FILE#
##############################################################
'''

print(items)
for item in items:
        file = open('dataglide.jl', 'a')
        line = json.dumps(item) + "\n"
        file.write(line)

file.close()
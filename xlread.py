import xlrd, datetime
from floodlist.call import Scraper
from floodlist.floodlist.pipelines import items
import json
from itemadapter import ItemAdapter

loc = ("data.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(1)

start_date_list = []
end_date_list = []
countrylist = []
 
for i in range(sheet.nrows - 2, sheet.nrows):
    
    start_date = xlrd.xldate_as_tuple(sheet.cell_value(i, 7), wb.datemode) 
    start_date = str(start_date[0]) + "/" + str(start_date[1]) + "/" + str(start_date[2])

    end_date = xlrd.xldate_as_tuple(sheet.cell_value(i, 8), wb.datemode) 
    end_date = str(end_date[0]) + "/" + str(end_date[1]) + "/" + str(end_date[2])

    countrylist.append(sheet.cell_value(i, 2))
    start_date_list.append(start_date)
    end_date_list.append(end_date)


scraper = Scraper(start_date_list, end_date_list, countrylist)
scraper.run_spiders()



'''
##############################################################
#ITEMS ARE NOW AVAILABLE AS LIST OF DICTIONARIES IN THIS FILE#
##############################################################
'''

print(items)
for item in items:
        file = open('datas.jl', 'a')
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        file.write(line)

file.close()


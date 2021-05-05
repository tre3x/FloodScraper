
import scrapy
from scrapy.crawler import CrawlerProcess
from floodlist.floodlist.spiders.floodspider import StackSpider
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
import xlrd, datetime
import os

class Scraper:
    def __init__(self, start_date, end_date, countrylist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.countrylist = countrylist
        self.start_date = start_date
        self.end_date = end_date
        configure_logging()

        settings_file_path = 'floodlist.floodlist.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = StackSpider  # The spider you want to crawl

    @defer.inlineCallbacks
    def crawl(self):
        for i in range(len(self.start_date)):
            yield self.process.crawl(self.spider, inpcountry = self.countrylist[i], start_date = self.start_date[i], end_date = self.end_date[i])
        reactor.stop()

    def run_spiders(self):
        self.crawl()
        reactor.run()


'''
inpcountry = input("Enter Country : ")
start_date = input("Enter start date(YY/MM/DD):")
end_date = input("Enter end date(YY/MM/DD): ")



loc = ("/home/tre3x/Python/iitr/floodscraping/floodlist/data.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(1)

start_date_list = []
end_date_list = []
items = []
 
for i in range(1, 3):
    
    start_date = xlrd.xldate_as_tuple(sheet.cell_value(i, 7), wb.datemode) 
    start_date = str(start_date[0]) + "/" + str(start_date[1]) + "/" + str(start_date[2])

    end_date = xlrd.xldate_as_tuple(sheet.cell_value(i, 8), wb.datemode) 
    end_date = str(end_date[0]) + "/" + str(end_date[1]) + "/" + str(end_date[2])

    start_date_list.append(start_date)
    end_date_list.append(end_date)


def returndetails(start_date_list, end_date_list):
    class ItemCollectorPipeline(object):
        def __init__(self):
            self.ids_seen = set()

        def process_item(self, item, spider):
            items.append(item.copy())

    process = CrawlerProcess({
        'USER_AGENT': 'scrapy',
        'LOG_LEVEL': 'INFO',
        'ITEM_PIPELINES': { '__main__.ItemCollectorPipeline': 100 }
    })

        
    process.crawl(StackSpider, inpcountry = 'india', start_date = start_date_list[0], end_date = end_date_list[0])
    process.start()


    for item in items:
        print(item)

'''


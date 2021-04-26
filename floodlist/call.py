
import scrapy
from scrapy.crawler import CrawlerProcess

from floodlist.spiders.floodspider import StackSpider

items = []
inpcountry = input("Enter Country : ")
start_date = input("Enter start date(YY/MM/DD):")
end_date = input("Enter end date(YY/MM/DD): ")

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

process.crawl(StackSpider, inpcountry = inpcountry, start_date = start_date, end_date = end_date)
process.start()

for item in items:
    print(item)

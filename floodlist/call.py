
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

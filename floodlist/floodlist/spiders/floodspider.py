from scrapy import Spider, Request
from scrapy.selector import Selector
import scrapy
from ..items import FloodlistItem
import requests
from ..cookie import getcookie
from ..dictionary import Country, Month
import re
from ..pipelines import AppendPipeline
from datetime import date

class StackSpider(Spider):

        name = "floodlist"     #NAME OF ACTIVE SPIDER

        def  __init__(self, inpcountry, start_date, end_date):

            '''
            ##############################
            #INITIALIZING CLASS VARIABLES#
            ##############################
            '''          

            self.start_urls = [
            "http://floodlist.com/asia/",
            ]                                   #CORE URL

            self.page_number = 1

            self.start_date_temp = start_date
            self.end_date_temp = end_date
            self.start_date = start_date.split('/')
            self.end_date = end_date.split('/')
            self.start_year = self.start_date[0]
            self.start_date = date(int(self.start_date[0]), int(self.start_date[1]), int(self.start_date[2])) #RESTRUCTURING DATE TO SUITABLE FORM
            self.end_date = date(int(self.end_date[0]), int(self.end_date[1]), int(self.end_date[2]))         #RESTRUCTURING DATE TO SUITABLE FORM

            self.inpcountry = re.sub('[^0-9a-zA-Z]+', '', inpcountry)                  
            self.inpcountry = re.sub(r'(?<=[a-z])-(?=[a-z])', '', self.inpcountry)            #RESTRUCTURING COUNTRYNAME TO SUITABLE FORM
            
            self._cookie_str = getcookie(self.start_urls[0])[0]     
            self.cookies = dict(pair.split('=') for pair in self._cookie_str.split('; ')) #OBTAIN COOKIES OF THE URL FOR FURTHER USE
            
            self._user_agent = getcookie(self.start_urls[0])[1]    #HEADER FILES
            print("SCRAPING STARTED!!\n")
            print("COUNTRY : {} \nSTART DATE : {} \nEND DATE : {}\n".format(self.inpcountry, self.start_date, self.end_date))

        def start_requests(self):

            '''
            ######################################
            #CREATE INITIAL REQUEST TO THE PAGE#
            ######################################
            '''         
            return [Request(url=url, cookies=self.cookies, headers={'User-Agent': self._user_agent}) for url in self.start_urls]


        def parse(self, response):

            '''
            ##############################
            #SCRAPING ITEMS FROM THE PAGE#
            ##############################
            '''
            item = FloodlistItem()
            articles = response.css('article.page-article')
            for article in articles:
                flood = article.css('.entry-title a::text').extract()
                dat = article.css('span::text').extract()[0]
                desc = article.css('.entry-summary p::text').extract()
                classname = article.xpath('@class').extract()
                dattemp = dat
                countries = []
                
                for word in classname[0].split(' '):
                    if word.split('-')[0] == 'tag':
                        tagged_str = " ".join(word.split('-')[1:])
                        if tagged_str.lower() == self.inpcountry.lower():
                            dat = dat.replace(',', '')
                            dat = dat.split(' ')   
                            dat[1] = Month[dat[1]]
                            dat = date(int(dat[2]), int(dat[1]), int(dat[0]))
                            
                            if  self.start_date <= dat <= self.end_date:

                                desc_link = article.css('.entry-title a::attr(href)').extract()
                                #ADDING VALUES TO ITEM DICTIONARY
                                #item['start_date'] = self.start_date_temp
                                #item['end_date'] = self.end_date_temp
                                item['date'] = dattemp
                                item['country'] = tagged_str
                                item['weblink'] = desc_link

                                AppendPipeline(item)
                                #FOLLOWING FLOOD DESCRIPTION PAGE TO SCRAP DESCRIPTION OF FLOOD EVENTS
                                #yield response.follow(desc_link[0], self.parse_description, meta = {'item': item.copy(), 'main_url': response.url}, cookies=self.cookies, headers={'User-Agent': self._user_agent})
            
            
            next_page = response.css('.next::attr(href)').get()

            #CONDITIONS FOR MOVING TO NEXT PAGE
            if int(dattemp.split(' ')[-1]) < int(self.start_year):
                next_page = None

            if next_page is not None:
                self.page_number = self.page_number + 1
                yield Request(next_page,  cookies=self.cookies, headers={'User-Agent': self._user_agent}, callback = self.parse)

        '''
        def parse_description(self, response):

            ###############################################################################
            #SCRAPING DETAILED DESCRIPTION OF FLOOD EVENTS FROM INDIVIDUAL FOOD EVENT PAGE#
            ###############################################################################

            item= response.meta['item'].copy() 
            item['desc'] = response.css('p~ p+ p::text').extract()
            JsonWriterPipeline(item)
            yield response.follow( response.meta['main_url'], self.parse, meta = {'item': item})
        '''
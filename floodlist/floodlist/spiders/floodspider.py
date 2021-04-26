from scrapy import Spider, Request
from scrapy.selector import Selector
import scrapy
from ..items import FloodlistItem
import requests
from ..cookie import getcookie
from ..dictionary import Country, Month
import re
from datetime import date

class StackSpider(Spider):
        name = "floodlist"
        def  __init__(self, inpcountry, start_date, end_date):
            self.start_urls = [
            "http://floodlist.com/asia/",
            ]
            self.page_number = 1
            self.start_date = start_date.split('/')
            self.end_date = end_date.split('/')
            self.start_year = self.start_date[0]
            self.start_date = date(int(self.start_date[0]), int(self.start_date[1]), int(self.start_date[2]))
            self.end_date = date(int(self.end_date[0]), int(self.end_date[1]), int(self.end_date[2]))

            self.inpcountry = re.sub('[^0-9a-zA-Z]+', '', inpcountry)
            self.inpcountry = re.sub(r'(?<=[a-z])-(?=[a-z])', '', self.inpcountry)

            self._cookie_str = getcookie(self.start_urls[0])

            self._user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'

        def start_requests(self):
            
            cookies = dict(pair.split('=') for pair in self._cookie_str.split('; '))
            print(cookies)
            return [Request(url=url, cookies=cookies, headers={'User-Agent': self._user_agent})
                    for url in self.start_urls]

        def parse(self, response):
            
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
                    if word[0:3] == 'tag':
                        for setcountry in Country:
                            
                            tempcountry = re.sub('[^0-9a-zA-Z]+', '', setcountry[1])
                            tempcountry = re.sub(r'(?<=[a-z])-(?=[a-z])', '', tempcountry)
                            
                            tempcountrycheck = re.sub('[^0-9a-zA-Z]+', '', word[4:])
                            tempcountrycheck = re.sub(r'(?<=[a-z])-(?=[a-z])', '', tempcountrycheck)

                            if tempcountry.lower() == tempcountrycheck.lower():
                                countries.append(tempcountrycheck.lower())
                                break

                for c in countries:
                    if self.inpcountry.lower() == c:
                        dat = dat.replace(',', '')
                        dat = dat.split(' ')   
                        dat[1] = Month[dat[1]]
                        dat = date(int(dat[2]), int(dat[1]), int(dat[0]))


                        
                        if  self.start_date < dat < self.end_date:

                            item['flood'] = flood
                            item['date'] = dattemp
                            item['country'] = c
                            desc_link = article.css('.entry-title a::attr(href)').extract()
                            cookies = dict(pair.split('=') for pair in self._cookie_str.split('; '))
                            yield response.follow(desc_link[0], self.parse_description, meta = {'item': item.copy(), 'main_url': response.url}, cookies=cookies, headers={'User-Agent': self._user_agent})

            next_page = response.css('.next::attr(href)').get()

            if int(dattemp.split(' ')[-1]) < int(self.start_year):
                next_page = None

            if next_page is not None:
                self.page_number = self.page_number + 1
                cookies = dict(pair.split('=') for pair in self._cookie_str.split('; '))
                yield Request(next_page,  cookies=cookies, headers={'User-Agent': self._user_agent}, callback = self.parse)


        def parse_description(self, response):
            item= response.meta['item'].copy() 
            item['desc'] = response.css('p~ p+ p::text').extract()
            yield item
            yield response.follow( response.meta['main_url'], self.parse, meta = {'item': item})
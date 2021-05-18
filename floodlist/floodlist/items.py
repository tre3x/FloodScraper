# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FloodlistItem(scrapy.Item):
    # define the fields for your item here like:
    #start_date = scrapy.Field()
    #end_date = scrapy.Field()
    #date = scrapy.Field()
    #desc = scrapy.Field()
    #country = scrapy.Field()
    weblink = scrapy.Field()

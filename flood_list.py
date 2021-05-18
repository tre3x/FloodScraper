import os
from .floodlist.call import Scraper
from .floodlist.floodlist.pipelines import items
import json
from itemadapter import ItemAdapter


def getfloodlist(start, end, country):

    start_date_list = [start]
    end_date_list = [end]
    countrylist = [country]

    scraper = Scraper(start_date_list, end_date_list, countrylist)
    scraper.run_spiders()

    '''
    ##############################################################
    #ITEMS ARE NOW AVAILABLE AS LIST OF DICTIONARIES IN THIS FILE#
    ##############################################################
    '''

    return items

if __name__ == '__main__':
    getdetails()
import os
import argparse
from floodlist.call import Scraper
from floodlist.floodlist.pipelines import items
from itemadapter import ItemAdapter


def getfloodlist(start, end, country):

    start_date_list = [start]
    end_date_list = [end]
    countrylist = [country]

    scraper = Scraper(start_date_list, end_date_list, countrylist)
    scraper.run_spiders()

    return items

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--start", help="Initial Date - Must be in String : YYYY/MM/DD")
    parser.add_argument("--end", help="Final Date - Must be in String : YYYY/MM/DD")
    parser.add_argument("--country", help="Country Name")

    args = parser.parse_args()

    flood_list = getfloodlist(args.start, args.end, args.country)

    for flood in flood_list:
        print(flood)
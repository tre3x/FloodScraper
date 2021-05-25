# FloodScraper
A python module which scraps flood links from various websites like [Floodlist](http://floodlist.com/), [Glidenumber](https://glidenumber.net/) using frameworks like Scrapy, Selenium.

To use this module :
1. Clone this repository
2. Run `pip install -r requirements.txt`
3. Use the module by importing function `getfloodlist()` or `getglidenumber()` from `FloodScraper.flood_list` or `FloodScraper.glide_number` respectively.

The function takes **start_date**, **end_date**, and **country_name** as parameters.

All dates must be given in **YYYY/MM/DD** format.

# Flood Scraper
A python module which scraps flood details from various websites like [Floodlist](http://floodlist.com/) using frameworks like Scrapy.

## INSTALLATION
To install the tool - follow the steps below : 
- Clone the repo - `git clone https://github.com/tre3x/FloodScraper.git`
- Navigate to `cd FloodScraper`
- Switch to the [Floodlist](http://floodlist.com/) specific branch `git checkout floodlist`
- Create working environment - `conda env create -f environment.yml`

## Usage
Once the tool is installed, navigate to the directory and follow the steps as suggested : 
- Activate the conda package `conda activate floodscraper`

To start crawling -  `python main.py --start <initial-date>  --end <final-date> --country <country>`

Parameters : 
- *initial-date* : the initial date from which the flood details would be stored
- *final-date* : the final date upto which the flood details would be stored
- *country* : the country of interest

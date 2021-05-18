import os
from sys import platform
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options


def descriptionscrap(cont, startdate, enddate):
    startdate = startdate.split("/")
    enddate = enddate.split("/")

    options = Options()
    options.headless = True

    #INITIALIZING SELENIUM WEB DRIVER
    here = os.path.dirname(os.path.abspath(__file__))

    if platform == "linux" or platform == "linux2":
        geckoloc = os.path.join(here, "..", "geckodrivers", "geckodriver_linux")
    elif platform == "darwin":
        geckoloc = os.path.join(here, "..", "geckodrivers", "geckodriver_mac")
    elif platform == "win32":
        geckoloc = os.path.join(here, "..", "geckodrivers", "geckodriver_win.exe")

    driver = webdriver.Firefox(options = options, executable_path=geckoloc)
    driver.get('https://glidenumber.net/glide/public/search/search.jsp')

    #GETTING COUNTRY CODES
    country = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[2]/td[2]/select')
    for option in country.find_elements_by_tag_name('option'):
        if(option.get_attribute('innerHTML').replace("\n", "").replace(" ", "").lower() == cont.replace(" ", "").lower()):
            countrycode = option.get_attribute('value')

    #SELECTING OPTIONS FROM SELECT TAB
    driver.execute_script("tab = document.getElementById('level1'); tab.value = '" + str(countrycode) + "';" )
    driver.execute_script("tab = document.getElementById('events'); tab.options[10].selected = true; tab.options[11].selected = true; tab.options[0].selected = false; ")

    #ENTERING DATES
    startyear = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[2]/input[1]")
    startmonth = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[2]/input[2]")
    startday = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[2]/input[3]")

    startyear.send_keys(startdate[0])
    startmonth.send_keys(startdate[1])
    startday.send_keys(startdate[2])

    endyear = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[3]/input[1]")
    endmonth = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[3]/input[2]")
    endday = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[3]/input[3]")

    endyear.send_keys(enddate[0])
    endmonth.send_keys(enddate[1])
    endday.send_keys(enddate[2])

    #TRIGGERING SEARCH
    search = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[9]/td[2]/input[1]').click()
    item = []

    try:
        #SCRAPING DETAILS
        numresult = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[11]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td')
        numresult = int(numresult.text.split(' ')[0])
        
        for i in range(2, numresult + 2):
                details = {}
                links = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[11]/td/table[3]/tbody/tr[' + str(i) + ']/td[1]/a')
                details['links'] = links.get_attribute('href')
                item.append(details)

        driver.quit()
        return item
                
    except NoSuchElementException:
        driver.quit()
        pass
    


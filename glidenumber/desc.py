from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import json


def descriptionscrap(cont, startdate, enddate):
    startdate = startdate.split("/")
    enddate = enddate.split("/")

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options = options, executable_path=r'/geckodriver', log_path='/geckologs/geckodriver.log')
    driver.get('https://glidenumber.net/glide/public/search/search.jsp')


    country = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[2]/td[2]/select')


    for option in country.find_elements_by_tag_name('option'):
        if(option.get_attribute('innerHTML').replace("\n", "").replace(" ", "").lower() == cont.replace(" ", "").lower()):
            countrycode = option.get_attribute('value')

    driver.execute_script("tab = document.getElementById('level1'); tab.value = '" + str(countrycode) + "';" )
    driver.execute_script("tab = document.getElementById('events'); tab.value = 'FL' ")

    startyear = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[2]/input[1]")
    startmonth = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[2]/input[2]")
    startday = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[2]/input[3]")

    startyear.send_keys(startdate[0])
    startmonth.send_keys(startdate[1])
    startday.send_keys(startdate[2])

    startyear = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[3]/input[1]")
    startmonth = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[3]/input[2]")
    startday = driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[7]/td[3]/input[3]")

    startyear.send_keys(enddate[0])
    startmonth.send_keys(enddate[1])
    startday.send_keys(enddate[2])

    search = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[9]/td[2]/input[1]').click()

    try:
        numresult = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[11]/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td')
        numresult = int(numresult.text.split(' ')[0])
        file = open('/home/tre3x/Python/iitr/floodscraping/dataglide.jl', 'a')
        
        for i in range(2, numresult + 2):
                details = {}
                desc = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td[1]/table/tbody/tr[11]/td/table[3]/tbody/tr[' + str(i) + ']/td[4]')
                details['start-date'] = '/'.join(startdate)
                details['end-date'] = '/'.join(enddate)
                details['country'] = cont
                details['desc'] = desc.text

                line = json.dumps(details) + "\n"
                file.write(line)
        file.close()
                
    except NoSuchElementException:
        pass
    
    driver.quit()


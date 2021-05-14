import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def getcookie(url):

    '''
    ##################################################
    #OBTAINING COOKIES IN REALTIME FOR FLOODLIST PAGE#
    ##################################################
    '''

    options = Options()
    options.headless = True

    here = os.path.dirname(os.path.abspath(__file__))
    geckoloc = os.path.join(here, "geckodriver")
    logloc = os.path.join(here, "../geckologs/geckodriver.log")
    driver = webdriver.Firefox(options = options, executable_path=geckoloc, log_path=logloc)
    
    driver.get(url)
    cookie = driver.get_cookies()
    driver.quit()
    return (cookie[0]['name'] + "=" + cookie[0]['value'])

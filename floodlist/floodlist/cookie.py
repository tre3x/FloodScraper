import os
from sys import platform
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

    if platform == "linux" or platform == "linux2":
        geckoloc = os.path.join(here, "..", "..", "geckodrivers", "geckodriver_linux")
    elif platform == "darwin":
        geckoloc = os.path.join(here, "..", "..", "geckodrivers", "geckodriver_mac")
    elif platform == "win32":
        geckoloc = os.path.join(here, "..", "..", "geckodrivers", "geckodriver_win.exe")

    driver = webdriver.Firefox(options = options, executable_path=geckoloc)
    
    driver.get(url)
    cookie = driver.get_cookies()
    driver.quit()
    return (cookie[0]['name'] + "=" + cookie[0]['value'])

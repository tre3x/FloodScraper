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
    driver = webdriver.Firefox(options=options, executable_path=r'/home/tre3x/Python/iitr/floodscraping/floodlist/floodlist/geckodriver',log_path='/home/tre3x/Python/iitr/floodscraping/floodlist/geckologs/geckodriver.log')
    driver.get(url)
    cookie = driver.get_cookies()
    driver.quit()
    return (cookie[0]['name'] + "=" + cookie[0]['value'])

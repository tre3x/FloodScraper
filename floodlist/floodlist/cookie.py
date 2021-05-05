from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def getcookie(url):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'/geckodriver', log_path='/../geckologs/geckodriver.log')
    driver.get(url)
    cookie = driver.get_cookies()
    driver.quit()
    return (cookie[0]['name'] + "=" + cookie[0]['value'])

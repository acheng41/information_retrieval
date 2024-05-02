from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

import re

def pagesearch(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options = chrome_options)

    driver.get(url)

    price = "navigate to page for price"
    beds = None
    bath = None
    try:
        address = driver.find_element(By.CLASS_NAME, "mapaddress").text
        if address == 'google maps':
            address = "navigate to page for address"
        price = driver.find_element(By.CLASS_NAME, "price").text
        price = re.sub(r'[^\d.]', '', price)
        price = int(price)
    except NoSuchElementException:
        address = "navigate to page for address"

    try:
        rms = driver.find_element(By.CLASS_NAME, "shared-line-bubble")
        rms = rms.find_elements(By.TAG_NAME, 'b')
        if len(rms) > 0:
            beds = rms[0].text[:-2]
            bath = rms[1].text[:-2]
        if address == 'google maps':
            address = "navigate to page for address"
    except NoSuchElementException:
        address = "navigate to page for address"

    driver.quit()


    return beds, bath, address, price
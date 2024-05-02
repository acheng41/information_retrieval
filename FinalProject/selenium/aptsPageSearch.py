from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import re

def pagesearch(url):
    driver = webdriver.Chrome()

    price = "navigate to page for price"
    beds = None
    bath = None

    driver.get(url)

    # Find address or note missing address
    try:
        address = driver.find_element(By.CLASS_NAME, "delivery-address").text
        address = address.replace(",", "")
    except NoSuchElementException:
        address = "navigate to page for address"
    if address.startswith('google'):
        address = "navigate to page for address"
    
    try:
        listings = driver.find_element(By.ID, "pricingView")
    except StaleElementReferenceException:
        listings = driver.find_element(By.ID, "pricingView")
    
    rents = listings.find_elements(By.CLASS_NAME, "rentLabel")
    rms = listings.find_elements(By.CLASS_NAME, "detailsLabel")
    
    results = []
    for i in range(len(rms)):
        if len(rents[i].text) > 0:
            price = rents[i].text.split()
            price = re.sub(r'[^\d.]', '', price[0])
            price = int(price)
        else:
            break
        
        # Extract number of beds/baths
        if len(rms[i].text) > 0:
            rm = rms[i].find_elements(By.TAG_NAME, 'span')
            if len(rm) > 0:
                beds = rm[0].text.split()[0].replace(",", "")
                bath = rm[1].text.split()[0]

        # Account for missing address/room counts or special room types like 'studio'
        if beds.isnumeric() and address != "navigate to page for address":
            name = beds + 'BR/' + bath + 'Ba unit at ' + address
        elif beds.isnumeric():
            name = beds + 'BR/' + bath + 'Ba unit'
        elif address != "navigate to page for address": 
            name = beds + 'unit at ' + address
        else:
            name = beds + 'unit'

        results.append((name, url, price, beds, bath))

    driver.quit()

    

    return results
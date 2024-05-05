from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from WUPageSearch import pagesearch

from datetime import datetime

def reformat_inputs(origin, destination, date): 
    if origin == "BWI": 
        origin = "Baltimore, MD"
    else: 
        origin = "New York, NY"
        
    if destination == "BWI": 
        destination = "Baltimore, MD"
    else: 
        destination = "New York, NY"
        
    #Reformat Date 
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date, "%m/%d/%Y")
    # Format the month and year into "Month Year" format
    formatted_date_str = date_obj.strftime("%B %Y")
    # Extract the day as an integer
    day_integer = date_obj.day

    return origin, destination, formatted_date_str, day_integer


def WUSearch(origin, destination, date, mode):
    origin, destination, formatted_date_str, day_integer = reformat_inputs(origin, destination, date)

    driver = webdriver.Chrome()


    # Navigate to the wanderu.com website
    driver.get("https://www.wanderu.com")
    print("Driver Initialized")

    # Find Search Bar and enter Departure Location
    origin_search = driver.find_element(By.XPATH,'//input[@aria-label="departure" and @data-id="origin"]')
    origin_search.click()
    origin_search.clear()
    origin_search.send_keys(origin)
    origin_search.send_keys(Keys.RETURN)

    # Find Search Bar and enter Arrival Location
    destination_search = driver.find_element(By.XPATH,'//input[@aria-label="arrival" and @data-id="destination"]')
    destination_search.click()
    destination_search.send_keys(destination)
    destination_search.send_keys(Keys.RETURN)

    # Uncheck Find Cheap Hotels
    ads_button = driver.find_element(By.CLASS_NAME, "ZDzGDfvBWCtG")
    ads_button.click()
    print("unchecked hotel finder")

    # Set Calendar
    date_search = driver.find_element(By.CLASS_NAME, "LtV56aME5ABC")
    date_search.click()
    # WebDriverWait(driver, 3).until(EC.visibilityOfElementLocated(By.CLASS_NAME, "LtV56aME5ABC"))
    month_year = driver.find_element(By.XPATH, '//span[@data-id="header-date"]').text
    # prev_button = driver.find_element(By.XPATH, '//button[@aria-label="previous-month"]')
    next_button = driver.find_element(By.XPATH, '//button[@aria-label="next-month"]')
    cal_target  = datetime.strptime(formatted_date_str, "%B %Y")
    while(month_year != formatted_date_str):
        current = datetime.strptime(month_year, "%B %Y")
        # Compare the datetime objects
        if current < cal_target:
            next_button.click()
        month_year = driver.find_element(By.XPATH, '//span[@data-id="header-date"]').text

    target_date = driver.find_element(By.XPATH, '//td[@aria-label="{}-active"]'.format(day_integer))
    target_date.click()


    #Find Search Button
    search_button = driver.find_element(By.XPATH, '//button[@type="button" and @label="Search"]')
    # search_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'C9btmpKqYElu')]")))
    search_button.click()


    # # Wait for the search results to load
    import time
    time.sleep(10)


    # #Get Train Listing
    hover_train = driver.find_element(By.XPATH,'//span[@class="_0-gBaFd8Iwkq" and text()="Trains"]')
    # Create an ActionChains object
    action_train = ActionChains(driver)
    # Hover over the element
    action_train.move_to_element(hover_train).move_by_offset(20, 0).click().perform()
    WebDriverWait(driver, 10)

    #Press Button for all Listings
    num_listings = driver.find_elements(By.CLASS_NAME, "_8F5FhShfDaF3")
    current = int(num_listings[0].text)
    total = int(num_listings[1].text)

    while(current < total): 
        see_more = driver.find_elements(By.CLASS_NAME, "C9btmpKqYElu")[-1]
        see_more.click()
        WebDriverWait(driver, 10)
        current = int(driver.find_elements(By.CLASS_NAME, "_8F5FhShfDaF3")[0].text)
        WebDriverWait(driver, 10)

    #Get listings for Train
    listings = driver.find_elements(By.CLASS_NAME, "gPwYYvClbIG4")

    trains = []

    for ele in listings: 
        
        listing_info = {}

        data = ele.text
        lines = data.strip().split('\n')
        dept = lines[1]
        arr = lines[4]
        duration = lines[2]
        price = lines[0]
        listing_info['Mode'] = "Train"
        listing_info['Dept'] = dept
        listing_info['Arr'] = arr
        listing_info['Duration'] = duration
        listing_info['Price'] = price
        
        try: 
            company = ele.find_element(By.CLASS_NAME, "GrRm34rZfwjd").get_attribute('alt')
            listing_info['Company'] = company
        except: 
            listing_info['Company'] = "Unknown"
        
        trains.append(listing_info)

    WebDriverWait(driver, 10)
    driver.refresh()
    # #Get Bus Listing
    hover_bus = driver.find_element(By.XPATH,'//span[@class="_0-gBaFd8Iwkq" and text()="Buses"]')
    # Create an ActionChains object
    action_bus = ActionChains(driver)
    # Hover over the element
    action_bus.move_to_element(hover_bus).move_by_offset(20, 0).click().perform()
    WebDriverWait(driver, 10)

    #Press Button for all Listings
    num_listings = driver.find_elements(By.CLASS_NAME, "_8F5FhShfDaF3")
    current = int(num_listings[0].text)
    total = int(num_listings[1].text)

    while(current < total): 
        see_more = driver.find_elements(By.CLASS_NAME, "C9btmpKqYElu")[-1]
        see_more.click()
        WebDriverWait(driver, 10)
        current = int(driver.find_elements(By.CLASS_NAME, "_8F5FhShfDaF3")[0].text)
        WebDriverWait(driver, 10)

    #Get listings for Train
    listings = driver.find_elements(By.CLASS_NAME, "gPwYYvClbIG4")

    buses = []

    for ele in listings: 
        
        listing_info = {}

        data = ele.text
        lines = data.strip().split('\n')
        dept = lines[1]
        arr = lines[4]
        duration = lines[2]
        price = lines[0]
        listing_info['Mode'] = "Bus"
        listing_info['Dept'] = dept
        listing_info['Arr'] = arr
        listing_info['Duration'] = duration
        listing_info['Price'] = price
        try: 
            company = ele.find_element(By.CLASS_NAME, "GrRm34rZfwjd").get_attribute('alt')
            listing_info['Company'] = company
        except: 
            listing_info['Company'] = "Unknown"
        
        buses.append(listing_info)




    driver.quit()
    if mode == "Train Only": 
        print(len(trains))
        return trains
    elif mode == "Bus Only": 
        print(len(buses))
        return buses
    else: 
        print(len(trains + buses))
        return trains + buses
    


if __name__ == '__main__':
    listings = WUSearch("BWI", "JFK", "05/08/2024", "All")
    # print(listings)
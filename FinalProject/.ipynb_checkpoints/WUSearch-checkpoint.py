from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

from WUPageSearch import pagesearch

import datetime

def WUSearch(origin,destination, date ):
    # # Set up the WebDriver
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(options = chrome_options)
    driver = webdriver.Chrome()


    # Navigate to the wanderu.com website
    driver.get("https://www.wanderu.com")
    print("Driver Initialized")

    # Select One Way Search
    one_way = driver.find_element(By.ID, "tab-one-way")
    print("Found Tab")
    # round_trip =  driver.find_element(By.ID, "tab-round-trip")
    # if round_trip.get_attribute("aria-selected") == True:
    #     round_trip.click()
    #     one_way.click()
    # assert(one_way.get_attribute("aria-selected") == True)
    # assert (one_way.is_selected())        

    # Find Search Bar for Departure Location
    origin_search = driver.find_element(By.XPATH,'//input[@aria-label="departure" and @data-id="origin"]')
    origin_search.click()
    print("found origin")
    origin_search.send_keys(origin)
    origin_search.send_keys(Keys.RETURN)

    # Find Search Bar for Arrival Location
    destination_search = driver.find_element(By.XPATH,'//input[@aria-label="arrival" and @data-id="destination"]')
    destination_search.click()
    print("found destination")
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
    prev_button = driver.find_element(By.XPATH, '//button[@aria-label="previous-month"]')
    next_button = driver.find_element(By.XPATH, '//button[@aria-label="next-month"]')
    my_input = "June 2024"
    day_input = 3
    while(month_year != my_input):
        next_button.click()
        month_year = driver.find_element(By.XPATH, '//span[@data-id="header-date"]').text
    
    target_date = driver.find_element(By.XPATH, '//td[@aria-label="{}-active"]'.format(day_input))
    target_date.click()
    
        

    
    # formatted_date = "Sun, May 5"
    # date_search.send_keys(formatted_date)
    # date_search.send_keys(Keys.RETURN)
    print("date input")
    # driver.execute_script("arguments[0].removeAttribute('readonly')", date_search)
    # driver.execute_script("arguments[0].value = Fri, May 10", date_search)

    # driver.find_element(By.XPATH, '//div[contains(@aria-label,"10")]').click()

    #Find Search Button
    search_button = driver.find_element(By.XPATH, '//button[@type="button" and @label="Search"]')
    # search_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'C9btmpKqYElu')]")))
    search_button.click()
    print("clicked button")

    #Reformat Date 
    # Parse the date string into a datetime object
    # date_obj = datetime.strptime(date, "%m/%d/%Y")
    # # Format the datetime object as "Wed, May 8"
    # formatted_date = date_obj.strftime("%a, %b %d")

    # # input query into search bars
    # destination_search.send_keys(destination)
    # date_search.send_keys(formatted_date)
    # search_button.click()

    print("Clicked Search Button")

    # Wait for the search results to load
    #wait = WebDriverWait(driver, 10)
    #wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "placardBanner")))
    import time
    time.sleep(10)


    # #Get Bus Listing
    # bus_select = driver.find_element(By.CLASS_NAME, "qzpQl44t9ZqQ")
    # bus_select.click()
    
    # #Get Train Listings
    listings = driver.find_elements(By.CLASS_NAME, "jlnsJ9HbqHu3")
    # print(listings)
    
    results = []

    for i,ele in enumerate(listings):
        
        values = {}
        try:
            price = ele.find_element(By.XPATH, "//span[@aria-label='Price' and @aria-live='polite']").text
            # print(price)
            dept = ele.find_element(By.XPATH, "//div[@aria-label='depart' and @aria-live='polite']").text
            # print(dept)
            arr = ele.find_element(By.XPATH, "//div[@aria-label='arrive' and @aria-live='polite']").text
            # print(arr)
            values['Price'] = price
            values['Dept'] = dept
            values['Arr'] = arr
            print(values)
        except StaleElementReferenceException:
            # # Retry the element lookup in case of StaleElementReferenceException
            listing = ele.find_element(By.CLASS_NAME, "titlestring")
            # #name = listing.text
            # link = listing.get_attribute("href")
            # beds, bath, address, price = pagesearch(link)
            # #price = ele.find_element(By.CLASS_NAME, "priceinfo").text
            # name = beds + 'BR/' + bath + 'Ba unit at ' + address
        # print(name, '|', link, '|', price)
        results.append(values)
        # print(ele)
        if i>0:
            break
        
    print("done - craigslist.org")
    print(str(results[i])+"\n" for i in range(len(results)))

    # Close the browser
    # input()
    driver.quit()
    # print(results)
    return results

if __name__ == '__main__':
    WUSearch("Baltimore, MD", "New York, NY", "05/08/2024")
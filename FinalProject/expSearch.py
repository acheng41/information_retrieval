from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


def expSearch(origin, destination, date):
    input_day = datetime.strptime(date, "%m/%d/%Y").day
    day = str(input_day)
    print(day)

    date_object = datetime.strptime(date, "%m/%d/%Y")

    # Format the datetime object as "Month Year"
    formatted_date = date_object.strftime("%B %Y")
    print(formatted_date)
    
    if destination == "NYC":
        destination = "JFK"

    print(destination)
    # Set up the WebDriver
    driver = webdriver.Chrome()
    # Navigate to the Expedia flights page
    driver.get("https://www.expedia.com/Flights")

    # Click on the One-way link
    one_way_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "uitk-tab-anchor") and contains(.,"One-way")]'))
        )
    one_way_link.click()

    # Click on the "Leaving from" button
    origin_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Leaving from"]'))
    )
    origin_button.click()

    # Enter origin
    origin_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Leaving from"]'))
    )
    origin_input.send_keys(origin)
    origin_input.send_keys(Keys.RETURN)

    # Click on the "Going to" button
    destination_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Going to"]'))
    )
    destination_button.click()

    # Enter destination
    destination_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Going to"]'))
    )
    destination_input.send_keys(destination)
    destination_input.send_keys(Keys.RETURN)

    # Click on the Date Picker button to open the Date Picker
    date_picker_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "date_form_field-btn")))
    date_picker_button.click()

    # Wait for the calendar to load
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'uitk-calendar')))
    
    #Select Month
    h2_element = driver.find_elements(By.CLASS_NAME,"uitk-date-picker-month-name")

    while h2_element[0].text != formatted_date:
        next_button = driver.find_elements(By.XPATH, "//button[@data-stid='date-picker-paging']")[1]
        next_button.click()
        h2_element = driver.find_elements(By.CLASS_NAME,"uitk-date-picker-month-name")
        

    # Click on the specific day
    day_path = '//button[@data-day="' + day + '"]'
    day_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, day_path))
    )
    day_button.click()

    # Click on the "Done" button
    done_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-stid="apply-date-picker"]'))
    )
    done_button.click()

    # Click on the search button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@id="search_button"]'))
    )
    search_button.click()
    time.sleep(10)

    # Wait for the flight listings to load
    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, '//li[@data-test-id="offer-listing"]'))
    )

    #Load all Listings
    while True:
        try:
            # Wait for the button to be clickable
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@name='showMoreButton']"))
            )
            # Click the button
            button.click()
            
            # Sleep for a short while to allow the page to load after clicking
            time.sleep(2)  # Adjust the sleep time as needed
            
        except TimeoutException:
            # If the button is not found or not clickable, break out of the loop
            break


    all_listing_info = []

    while True:
        # Find all flight listings
        listings = driver.find_elements(By.XPATH, '//li[@data-test-id="offer-listing"]')
        # Iterate through each listing
        for listing in listings:
            # Dictionary to store information for the current listing
            listing_info = {}

            # Find elements within the current listing
            duration = listing.find_element(By.CSS_SELECTOR, '[data-test-id="journey-duration"]').text
            price = listing.find_element(By.CSS_SELECTOR, '.uitk-lockup-price').text
            airline_info = listing.find_element(By.CSS_SELECTOR, '[data-test-id="flight-operated"]').text.split(' • ')[0]
            dept, arr = listing.find_element(By.CSS_SELECTOR, '[data-test-id="departure-time"]').text.split(' - ')    

            # link_button = listing.find_element(By.XPATH, './/button[@data-test-id="select-link"]')
            # link = link_button.get_attribute("onclick").split("window.open('")[1].split("')")[0]     

            # Store information in the dictionary
            # listing_info['Link'] = link
            listing_info['Mode'] = "Plane"
            listing_info['Dept'] = dept
            listing_info['Arr'] = arr
            listing_info['Duration'] = duration.split('(')[0].strip()
            listing_info['Price'] = price
            listing_info['Company'] = airline_info

            # Add the dictionary to the list
            all_listing_info.append(listing_info)

        # Scroll to load more listings
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)
        # Wait for some time to let new listings load
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//li[@data-test-id="offer-listing"]'))
        )
        more_listings = driver.find_elements(By.XPATH, '//li[@data-test-id="offer-listing"]')

        if len(more_listings) == len(listings):
            break

    #Print all flight listings
    # for listing_info in all_listing_info:
    #     print(listing_info)
    #     print("\n")

    # print(len(all_listing_info))
    print("done - expedia.com")

    # Close the browser
    time.sleep(30)
    driver.quit()

    return all_listing_info

if __name__ == '__main__':
    listings = expSearch("BWI", "JFK", "07/10/2024")
    print(listings)

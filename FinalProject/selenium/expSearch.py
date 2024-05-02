import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def aptsSearch():
    # Set up the WebDriver
    driver = webdriver.Chrome()
    # Navigate to the Expedia flights page
    driver.get("https://www.expedia.com/Flights")
    # time.sleep(2)

    # Find the one-way button and click it
    one_way_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "uitk-tab-anchor") and contains(.,"One-way")]'))
        )
    # Click on the One-way link
    one_way_link.click()
    # time.sleep(2)

    # Find and enter the origin
   # Wait for the "Leaving from" button to be clickable
    origin_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Leaving from"]'))
    )

    # Click on the "Leaving from" button
    origin_button.click()

    # time.sleep(3)

    origin_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Leaving from"]'))
    )
    origin_input.send_keys("BWI")
    # time.sleep(5)
    origin_input.send_keys(Keys.RETURN)

    # Wait for the "Going to" button to be clickable
    destination_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Going to"]'))
    )
    # time.sleep(2)
    # Click on the "Going to" button
    destination_button.click()
    destination_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Going to"]'))
    )
    # time.sleep(1)
    destination_input.send_keys("JFK")
    # time.sleep(3)
    destination_input.send_keys(Keys.RETURN)



    # Date
    # Wait for the Date Picker button to be clickable
    date_picker_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "date_form_field-btn")))
    # time.sleep(2)
    # Click on the Date Picker button to open the Date Picker
    date_picker_button.click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'uitk-calendar')))

    # Wait for the specific day button to be clickable
    date_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-day="2"]'))
    )
    # time.sleep(2)
    # Click on the date
    date_button.click()

    # Wait for the "Done" button to be clickable
    done_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-stid="apply-date-picker"]'))
    )
    # time.sleep(1)
    # Click on the "Done" button
    done_button.click()



    # day_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='uitk-date-picker-day undefined' and @data-day='8']")))
    # day_button.click()

    # Click the search button
    # Wait for the search button to be clickable
    search_button = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@id="search_button"]'))
    )
    # time.sleep(2)
    # Click on the search button
    search_button.click()


    # Wait for the flight listings to load
    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.XPATH, '//li[data-test-id="offer-listing"]'))
    )

    # Find all flight listings
    listings = driver.find_elements(By.XPATH, '//li[@data-test-id="offer-listing"]')
    print(listings)

    all_listing_info = []

    # Iterate through each listing
    for listing in listings:
        # Dictionary to store information for the current listing
        listing_info = {}

        # Find elements within the current listing
        duration = listing.find_element(By.XPATH, './/span[@data-test-id="departure-time"]').text
        # price = listing.find_element(By.CSS_SELECTOR, '.uitk-lockup-price').text
        # airline_info = listing.find_element(By.CSS_SELECTOR, '[data-test-id="flight-operated"]').text.split(' • ')[0]
        # departure_time = listing.find_element(By.CSS_SELECTOR, '[data-test-id="departure-time"]').text         


        # Store information in the dictionary
        # listing_info['Dept|Arr'] = departure_time
        # listing_info['Arr'] = arrival_time
        listing_info['Duration'] = duration
        # listing_info['Price'] = price
        # listing_info['Airline'] = airline_info

        # Add the dictionary to the list
        all_listing_info.append(listing_info)

    print(all_listing_info)
    print("done - expedia.com")

    # Close the browser
    time.sleep(60)
    driver.quit()

    return all_listing_info

if __name__ == '__main__':
    aptsSearch()

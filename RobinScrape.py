from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tinydb import TinyDB, Query
import time
import os
from datetime import datetime, timedelta


#Get Selenium WebDriver
def init_driver():

    driver = webdriver.Chrome(os.getcwd() + "/chromedriver")

    return driver

#Initialize TinyDB for storing cruise info
def init_db():

    db = TinyDB('cruisedb.json')

#Get list of search result HTML elements (10 per page)
def get_page_results(driver, page_link):


    # Will be replaced by driver.get(page_link) after testing
    driver.get("https://secure.royalcaribbean.com/cruises")

    results = driver.find_element_by_class_name("bottom-section")

    results = results.find_elements_by_xpath("./*")

    childList = results[0].find_elements_by_xpath("./*")

    return childList



# ******************************************
# SCRAPING FUNCTIONS. GET CRUISE INFORMATION
# ******************************************

def get_cruise_name(cruise_listing):

    return cruise_listing.find_element_by_tag_name("h3").find_element_by_xpath("./a").text


def get_departure_location(cruise_listing):

    return cruise_listing.find_element_by_class_name("cruise-details").find_element_by_tag_name("strong").text


def get_port_list(cruise_listing):

    port_visit_list = cruise_listing.find_element_by_class_name("list-ports").find_elements_by_xpath("./*")

    port_text_list = []   

    for port in port_visit_list:
        #Extra li element at beginning. This if case weeds it out
        if not (port.get_attribute("class") == "show-for-small-only"):
            city_text = port.find_element_by_tag_name("strong").text
            state_text = port.find_element_by_tag_name("span").text
            combined_text = (city_text + " " + state_text)
            #print(combined_text)
            port_text_list.append(combined_text)

    return port_text_list


def get_price(cruise_listing):

    return cruise_listing.find_element_by_class_name("cruise-price").text


def get_learn_more_url(cruise_listing):

    return cruise_listing.find_element_by_class_name("cruise-detail-link").get_attribute("href")


# This one's still buggy. See comments inside of function
def get_departure_dates(cruise_listing, iterator, driver):

    view_dates_button = cruise_listing.find_element_by_class_name("viewAllDates")
        
    #Scrolling to next element. Currently scrolls too far (One past the target element).
    #Currently have to manually scroll during wait time. Don't know how to fix this at the moment...
    if not (iterator==0):
        driver.execute_script("return arguments[0].scrollIntoView(true);", view_dates_button)
        time.sleep(3)

    view_dates_button.click()

    time.sleep(3)

    # Sometimes the loading of dates will not fully execute within 3 seconds.
    # Rare case, and kind of a hacky fix. But, it works
    try:
        cruise_listing.find_element_by_class_name("inline-cruise-details").find_elements_by_xpath("./tbody/*")
    except NoSuchElementException:
        time.sleep(10)
        pass


    cruise_date_list = cruise_listing.find_element_by_class_name("inline-cruise-details").find_elements_by_xpath("./tbody/*")

    unformatted_departure_dates = []

    for cruise_date in cruise_date_list:
        date_text = cruise_date.find_element_by_xpath("./td/b").text[6:]
    #    print(date_text)
        unformatted_departure_dates.append(date_text)

    return unformatted_departure_dates


def get_formatted_return_list(departure_list, cruise_length):

    formatted_departure_list = get_formatted_date_list(departure_list)

    cruise_return_list = []

    for departure in departure_list:
        date = datetime.strptime(departure, '%d %b %Y')
        end = date + timedelta(days=cruise_length)
        endString = end.isoformat()[:10]
        cruise_return_list.append(endString)

    return cruise_return_list


def get_formatted_date_list(date_list):

    formatted_departure_list = []

    for item in date_list:     
        date = datetime.strptime(item, '%d %b %Y')
        dateString = date.isoformat()[:10]
        formatted_departure_list.append(dateString)

    return formatted_departure_list

#******************************
# END SCRAPING FUNCTIONS
#******************************


# Scrape all information for each result listed on page.
# Typically, 10 results per page
def get_individual_result_info(result_list,driver):

    i = 0

    # For every result, get info.
    for cruise_listing in result_list:

        cruise_title_text = get_cruise_name(cruise_listing)

        cruise_duration = int(cruise_title_text.split()[0])

        departure_location_text = get_departure_location(cruise_listing)

        port_text_list = get_port_list(cruise_listing)

        price_text = get_price(cruise_listing)

        learn_more_url = get_learn_more_url(cruise_listing)
        
        unformatted_departure_dates = get_departure_dates(cruise_listing, i, driver)

        formatted_departure_dates = get_formatted_date_list(unformatted_departure_dates)

        formatted_return_dates = get_formatted_return_list(unformatted_departure_dates, cruise_duration)

        i += 1

        #*************************************
        # Print Results (For Testing Purposes)
        #*************************************

        print("\nCruise Title: " + cruise_title_text)

        print("\nDeparture Location: " + departure_location_text)

        print("\nPort Locations:")
        for entry in port_text_list:
	        print(entry)

        print("\nPrice: " + price_text + "\n")

        print("\nLearn More URL: " + learn_more_url)

        print("\n Dates\n")

        n = 0

        for item in formatted_departure_dates:
            print(item + " - " + formatted_return_dates[n])
            n += 1


if __name__ == "__main__":
    drive = init_driver()
    listing = get_page_results(drive,"testing")
    get_individual_result_info(listing,drive)
    drive.get("https://www.google.com")
    drive.close()

    

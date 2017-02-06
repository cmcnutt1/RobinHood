from selenium import webdriver
from tinydb import TinyDB, Query
import time
import os
from datetime import datetime, timedelta


# Initialize Selenium WebDriver
def init_driver():

    driver = webdriver.Chrome(os.getcwd() + "/chromedriver")

    return driver

# Initialize cruise listing database (TinyDB)
def init_db():

    db = TinyDB('cruisedb.json')

# Get the reference to the itenerary HTML 
def get_page_result(driver, page_link):

    # Open up link in WebDriver
    driver.get(page_link)

    results = driver.find_element_by_class_name("col-8")

    results = results.find_elements_by_xpath("./*")

    #print(len(results))

    return results

#*************************
# SCRAPING FUNCTIONS
#*************************

def get_port_detail(day_info):

    return day_info.find_element_by_class_name("col-port-detail").find_element_by_xpath("./h3").text

def get_dock_detail(day_info):

    return day_info.find_element_by_class_name("tour-day").text

def get_formatted_info(port_detail, dock_detail, indicator):

    if(indicator == "Welcome:"):
        day_info = "Depart from " + port_detail[9:]
    elif(indicator == "Cruising:"):
        day_info = "Day at Sea"
    else:
        indicator = port_detail.split()[0] + " " + port_detail.split()[1] + " " + port_detail.split()[2]

        if(indicator == "Port of Arrival:"):
            day_info = "Arrive at " + port_detail[17:]
        else:
            indicator = dock_detail.split()
            indicator = indicator[(len(indicator) - 1)]

            if(indicator == "(DOCKED)"):
                day_info = "Docked at " + port_detail[14:]
            else:
                day_info = "Tendered at " + port_detail[14:]

    return day_info

#************************
# END SCRAPING FUNCTIONS
#************************


# Get day-by-day info for cruises
def get_individual_result_info(result_list,driver):

    day_by_day = []

    for day_info in result_list:

        port_detail = get_port_detail(day_info)

        dock_detail = get_dock_detail(day_info)

        indicator = port_detail.split()[0]

        iten_info = get_formatted_info(port_detail, dock_detail, indicator)

        day_by_day.append(iten_info)

        #Print, for testing purposes

        print(iten_info)


if __name__ == "__main__":
    drive = init_driver()

    link = "https://secure.royalcaribbean.com/cruises/4NightBahamasCruise-MJ04S135?currencyCode=USD&sCruiseType=CO&sailDate=11%2F27%2F2017"

    listing = get_page_result(drive,link)
    get_individual_result_info(listing,drive)
    drive.get("https://www.google.com")
    drive.close()

    

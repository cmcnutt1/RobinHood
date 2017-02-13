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

    time.sleep(3)

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

    include_entry = True

    if(indicator == "Welcome:"):
        day_info = "Depart from " + port_detail[9:]
    elif(indicator == "Cruising:" or indicator == "Disembark:" or "AT SEA" in port_detail):
        if(port_detail.split()[1] == "International"):
            include_entry = False
        day_info = "Day at Sea"
        if("Sound" in port_detail):
            day_info = port_detail.split()[1] + " " + port_detail.split()[2]
        

    else:
        indicator = port_detail.split()[0] + " " + port_detail.split()[1] + " " + port_detail.split()[2]

        if(indicator == "Port of Arrival:"):
            day_info = "Disembark at " + port_detail[17:]
        else:
            indicator = dock_detail.split()
            indicator = indicator[(len(indicator) - 1)]

            if(indicator == "(DOCKED)"):
                day_info = "Docked at " + port_detail[14:]
            else:
                day_info = "Tendered at " + port_detail[14:]

    if not(include_entry):
        day_info = "exclude"
    
    return day_info

 

#************************
# END SCRAPING FUNCTIONS
#************************


# Get day-by-day info for cruises
def get_itin_learn_more(link):

    driver = init_driver()

    result_list = get_page_result(driver, link)

    day_by_day = []

    sound_list = []

    sound_day = ""

    for day_info in result_list:
        
        if not (day_info.get_attribute("class") == "itenerary-alert"):

            port_detail = get_port_detail(day_info)

            dock_detail = get_dock_detail(day_info)

            indicator = port_detail.split()[0]

            itin_info = get_formatted_info(port_detail, dock_detail, indicator)

            #Sounds fucking everything up
            if(len(sound_list) > 1 and not "Sound" in itin_info):
                for item in sound_list:
                    sound_day = sound_day + item + ", "
                day_by_day.append("Cruising Through " + sound_day[:(len(sound_day) - 2)])
                day_by_day.append(itin_info)
                sound_list = []

            elif("Sound" in itin_info):
                sound_list.append(itin_info)

            elif not (itin_info == "exclude"):
                day_by_day.append(itin_info)

            else:
                print("International Dateline")

            #Print, for testing purposes

    '''for item in day_by_day:
        #print(item)
    TESTING^^'''

    driver.close()
    
    return day_by_day

if __name__ == "__main__":
    #drive = init_driver()

    link = "https://secure.royalcaribbean.com/cruises/EX07A146"

    #link = "https://secure.royalcaribbean.com/cruises/17NightAustraliaNewZealandCruise-RD17K025?currencyCode=USD&sCruiseType=CO&sailDate=02%2F25%2F2017"

    #link = "https://secure.royalcaribbean.com/cruises/24NightTranspacificCruise-EX24T003?currencyCode=USD&sCruiseType=CO&sailDate=04%2F22%2F2017"

    #link = "https://secure.royalcaribbean.com/cruises/4NightBahamasCruise-MJ04S135?currencyCode=USD&sCruiseType=CO&sailDate=11%2F27%2F2017"

    #listing = get_page_result(drive,link)

    get_itin_learn_more(link)
    #drive.get("https://www.google.com")
    #drive.close()

    

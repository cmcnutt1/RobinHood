from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from tinydb import TinyDB, Query
import time
import os
from datetime import datetime, timedelta

#Some globals for sleep time lengths
NAP = 2
REST = 5
SLUMBER = 10
HIBERNATE = 30


#Get Selenium WebDriver
def init_driver():

    driver = webdriver.Chrome(os.getcwd() + "/chromedriver")

    return driver

#Initialize TinyDB for retrieving cruise info
def init_db():

    db = TinyDB('cruisedb.json')



#************************************************
# INSERT FUNCTIONS (Better description needed)
# ***********************************************


# Cruise Title
def insert_cruise_title(cruise_title,driver):

    driver.find_element_by_id("titlewrap").find_element_by_xpath("./input").send_keys(cruise_title)
    

# Big HTML Chunk, inserted in the textbox below the title
def insert_cruise_main_info(info_html,driver):

    #Switch to text tab
    driver.find_element_by_id("content-html").click()

    time.sleep(NAP)

    #Send HTML chunk to text area 
    textarea = driver.find_element_by_id("wp-content-editor-container").find_element_by_class_name("wp-editor-area")
    textarea.send_keys(info_html + "\nThis should be a new line\n\n\n\n4 Lines Down")

    time.sleep(NAP)


# Get a dropdown value for ..something 
def select_badge_dropdown(driver):

    # Find dropdown button
    dropdown_button = driver.find_element_by_id("tour_tabs_meta[tour_badge]").find_element_by_class_name("select2-choice")    

    #Scroll to it
    driver.execute_script("return arguments[0].scrollIntoView(true);",dropdown_button)
    driver.execute_script("window.scrollBy(0,-350)")

    time.sleep(NAP)

    #Click it
    dropdown_button.click()

    time.sleep(NAP)

    # Once dropdown displayed, choose 'Starting From: '

    dropdown_selection = driver.find_element_by_id("select2-drop").find_element_by_class_name("select2-results").find_elements_by_xpath("./*")[3]

    dropdown_selection.click()

# Throw an 'Itinerary' on it
def insert_iten_title(driver):

    driver.find_element_by_id("tour_tabs_meta[tabs][0][title]").find_element_by_class_name("vp-input").send_keys("Itinerary")

# Make a big chunk of HTML using the itinerary list, and then do a bunch of 
def insert_day_by_day(itinerary, driver):

    big_ass_string = "<p>[timeline]<br />"

    n = 1

    for day in itinerary:

        day_string = '[timeline_item item_number="' + str(n) + '" title="Day ' + str(n) + '"]' + day + '[/timeline_item]<br />'

        big_ass_string = big_ass_string + day_string

        n+=1

    big_ass_string = big_ass_string + '[/timeline]</p>'

    print(big_ass_string)

    driver.execute_script("window.scrollBy(0,250)")

    time.sleep(NAP)

    driver.find_element_by_id("mceu_174-open").click()

    time.sleep(NAP)

    driver.find_element_by_id("mceu_211").click()

    time.sleep(NAP)

    driver.find_element_by_id("mceu_214").send_keys(big_ass_string)

    time.sleep(REST)

    driver.find_element_by_id("mceu_216").find_element_by_xpath("./button").click()


def insert_ship_info(driver, ship_info):

    time.sleep(NAP)

    add_more_tab = driver.find_element_by_id("wpa_loop-[tabs]").find_element_by_class_name("vp-wpa-group-add")

    add_more_tab.click()

    time.sleep(NAP)

    title_bar = driver.find_element_by_id("tour_tabs_meta[tabs][1]").find_element_by_class_name("vp-input")

    title_bar.send_keys("THE BEST CRUISE SHIP IN THE WORLD")

    time.sleep(NAP)

    #click tools on top bar
    driver.find_element_by_id("mceu_252-open").click()

    time.sleep(NAP)

    #click "Source Code" under tools
    driver.find_element_by_id("mceu_289").click()

    time.sleep(REST)

    text_area = driver.find_element_by_id("mceu_292")

    text_area.click()

    text_area.send_keys("Testing Testing 1,2,3")

    time.sleep(NAP)

    submit_button = driver.find_element_by_id("mceu_294").find_element_by_xpath("./button")

    submit_button.click()

    

def get_individual_result_info(driver):

    #**********************
    # SAMPLE TESTING DATA
    #**********************

    cruise_title = "4 sample title"

    cruise_title_text = "4 sample title"

    cruise_duration = int(cruise_title.split()[0])

    cruise_ship = "sample ship"

    departure_location_text = "leaving location"

    port_text_list = ["Port 1","Port 2","Port 3","Port 4","Port 5"]

    port_tag_list = ["Tag 1","Tag 2","Tag 3","Tag 4","Tag 5"]

    price_text = "400"

    sale_price_text = "40"

    learn_more_url = "not important"

    cruise_subtitle = "Port 1 -> Port 2 -> Port 3 -> Port 4 -> Port 5"

    itinerary = ["Depart from Cape Testing, NJ", "Day at Sea", "Day at Sea", "Docked at San Test, Puerto Rico", "Docked at Testburg, St. Maarten", "Docked at St. Test, Antigua", "Tendered at Fort de Test, Martinique", "Docked at Testtown, Barbados", "Docked at Basseterre, St. Test", "Day at Sea", "Day at Sea", "Day at Sea", "Return to Cape Testing, NJ"]

    unformatted_departure_dates = []

    formatted_departure_dates = ["2017-01-01","2017-02-01","2017-03-01"]

    formatted_return_dates = ["2017-01-05","2017-02-05","2017-03-05"]


    #*****************************
    # RUN INTERACTION FUNCTIONS
    #*****************************

    #Insert Title
    insert_cruise_title(cruise_title,driver)

    #Insert Departure, port, features HTML
    insert_cruise_main_info(departure_location_text,driver)

    #Select Badge (Starting From:)
    select_badge_dropdown(driver)

    #Insert 'Itinary' Title
    insert_iten_title(driver)

    #Insert HTML chunk for day by day locations
    insert_day_by_day(itinerary, driver)

    #
    insert_ship_info(driver, "test info")

    time.sleep(HIBERNATE)






if __name__ == "__main__":

    drive = init_driver()

    link = "file:///home/chris/Downloads/blank_input.html"

    drive.get(link)

    time.sleep(NAP)

    get_individual_result_info(drive)

    drive.close()




from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from tinydb import TinyDB, Query
import time
import os
from datetime import datetime, timedelta
from Cruise_Details import create_port_list, test_HTML_input

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
    textarea.send_keys(info_html)

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

    driver.find_element_by_id("tour_tabs_meta[tabs][0][content]_ce").send_keys(big_ass_string)

    time.sleep(REST)


def insert_ship_info(driver, ship_info):

    time.sleep(NAP)

    add_more_tab = driver.find_element_by_id("wpa_loop-[tabs]").find_element_by_class_name("vp-wpa-group-add")

    add_more_tab.click()

    time.sleep(NAP)

    title_bar = driver.find_element_by_id("tour_tabs_meta[tabs][1]").find_element_by_class_name("vp-input")

    title_bar.send_keys("THE BEST CRUISE SHIP IN THE WORLD")

    time.sleep(NAP)

    text_area = driver.find_element_by_id("tour_tabs_meta[tabs][1][content]_ce")

    text_area.send_keys(ship_info)

    time.sleep(NAP)


def complete_header_information(subtitle, ship_img, driver):

    image_radio = driver.find_element_by_id("header_section_meta_metabox").find_element_by_class_name("input").find_elements_by_xpath("./*")[1].find_element_by_xpath("./input")

    image_radio.click()

    time.sleep(SLUMBER)

    #Enter subtitle

    sub_input = driver.find_element_by_id("header_section_meta[banner_subtitle]")

    sub_input.click()

    sub_input.send_keys(subtitle)

    time.sleep(NAP)

    #Will input image here

    image_add_button = driver.find_element_by_id("header_section_meta[banner_image]").find_element_by_class_name("buttons").find_elements_by_xpath("./*")[0]

    image_add_button.click()

    time.sleep(NAP)

    #"Insert from URL" button

    insert_url_link = driver.find_element_by_id("__wp-uploader-id-0").find_element_by_class_name("media-menu").find_elements_by_xpath("./*")[6]

    insert_url_link.click()

    time.sleep(NAP)

    #Insert URL

    url_box = driver.find_element_by_id("embed-url-field")

    url_box.click()

    url_box.send_keys("")

    url_box.send_keys(ship_img)

    time.sleep(NAP)

    #Click submit button

    submit_button = driver.find_element_by_class_name("media-frame-toolbar").find_element_by_class_name("media-button-select")

    submit_button.click()

    time.sleep(REST)
    

def get_individual_result_info(driver):

    #**********************
    # SAMPLE TESTING DATA
    #**********************

    cruise_title = "4 sample title"

    cruise_title_text = "4 sample title"

    cruise_duration = int(cruise_title.split()[0])

    cruise_ship = "sample ship"

    img_source = "http://7eb.8aa.myftpupload.com/wp-content/uploads/2017/02/anthem2.jpg"

    departure_location_text = "leaving location"

    arrival_location_text = "arriving location"

    port_text_list = ["Port 1","Port 2","Port 3","Port 4","Port 5"]

    port_tag_list = ["Tag 1","Tag 2","Tag 3","Tag 4","Tag 5"]

    price_text = "400"

    sale_price_text = "40"

    learn_more_url = "not important"

    cruise_subtitle = "Cape Liberty → Puerto Rico → St. Maarten → Antigua → Martinique → Barbados → St. Kitts"

    itinerary = ["Depart from Cape Testing, NJ", "Day at Sea", "Day at Sea", "Docked at San Test, Puerto Rico", "Docked at Testburg, St. Maarten", "Docked at St. Test, Antigua", "Tendered at Fort de Test, Martinique", "Docked at Testtown, Barbados", "Docked at Basseterre, St. Test", "Day at Sea", "Day at Sea", "Day at Sea", "Return to Cape Testing, NJ"]

    unformatted_departure_dates = []

    formatted_departure_dates = ["2017-01-01","2017-02-01","2017-03-01"]

    formatted_return_dates = ["2017-01-05","2017-02-05","2017-03-05"]


    #*****************************
    # RUN INTERACTION FUNCTIONS
    #*****************************

    #Insert Title
    insert_cruise_title(cruise_title,driver)

    port_string = create_port_list(port_text_list)
    html_input = test_HTML_input(departure_location_text, arrival_location_text, port_string, price_text)

    #Insert Departure, port, features HTML
    insert_cruise_main_info(html_input,driver)

    #Select Badge (Starting From:)
    select_badge_dropdown(driver)

    #Insert 'Itinary' Title
    insert_iten_title(driver)

    #Insert HTML chunk for day by day locations
    insert_day_by_day(itinerary, driver)

    #
    insert_ship_info(driver, "test info")

    complete_header_information(cruise_subtitle, img_source, driver)

    time.sleep(HIBERNATE)






if __name__ == "__main__":

    drive = init_driver()

    link = "http://7eb.8aa.myftpupload.com/wp-admin/post-new.php?post_type=product"

    drive.get(link)

    time.sleep(HIBERNATE)

    drive.get(link)

    time.sleep(NAP)

    get_individual_result_info(drive)

    drive.close()




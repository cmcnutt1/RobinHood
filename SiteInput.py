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


def insert_cruise_title(cruise_title,driver):

    driver.find_element_by_id("titlewrap").find_element_by_xpath("./input").send_keys(cruise_title)
    

def insert_cruise_main_info(info_html,driver):

    driver.find_element_by_id("content-html").click()

    time.sleep(2)

    textarea = driver.find_element_by_id("wp-content-editor-container").find_element_by_class_name("wp-editor-area")

    textarea.send_keys(info_html + "\nThis should be a new line\n\n\n\n4 Lines Down")


def select_badge_dropdown(driver):

    # Find dropdownbutton, click it
    dropdown_button = driver.find_element_by_id("tour_tabs_meta[tour_badge]").find_element_by_class_name("select2-choice")    

    driver.execute_script("return arguments[0].scrollIntoView(true);",dropdown_button)

    time.sleep(5)

    driver.execute_script("window.scrollBy(0,-350)")

    time.sleep(3)

    dropdown_button.click()

    time.sleep(3)

    # Once dropdown displayed, click on 'Starting From: ' selection

    dropdown_selection = driver.find_element_by_id("select2-drop").find_element_by_class_name("select2-results").find_elements_by_xpath("./*")[3]

    dropdown_selection.click()

def insert_iten_title(driver):

    driver.find_element_by_id("tour_tabs_meta[tabs][0][title]").find_element_by_class_name("vp-input").send_keys("Itinerary")


def insert_day_by_day(intinerary, driver):

    

def get_individual_result_info(driver):

    i = 0


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


    insert_cruise_title(cruise_title,driver)

    insert_cruise_main_info(departure_location_text,driver)

    select_badge_dropdown(driver)

    insert_iten_title(driver)

    insert_day_by_day(itinerary, driver)

    time.sleep(10)






if __name__ == "__main__":

    drive = init_driver()
    it = 0
    link = "file:///home/chris/Downloads/blank_input.html"
    drive.get(link)
    time.sleep(2)
    get_individual_result_info(drive)
    it += 1

    drive.get("https://www.google.com")
    drive.close()




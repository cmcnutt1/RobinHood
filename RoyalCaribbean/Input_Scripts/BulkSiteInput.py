from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, UnexpectedAlertPresentException, WebDriverException, TimeoutException
from tinydb import TinyDB, Query
import time
import os
from datetime import datetime, timedelta
from Cruise_Details import create_port_list, test_HTML_input
from DBInspect import print_individual_entry
from ShipHTML import switch_ship

#Some globals for sleep time lengths
NAP = 2
REST = 5
SLUMBER = 10
HIBERNATE = 30


#Get Selenium WebDriver
def init_driver():

    driver = webdriver.Chrome(os.getcwd() + "../chromedriver")

    return driver

#Initialize TinyDB for retrieving cruise info
def init_db(ship_name):

    db = TinyDB('../individual_ships/' + ship_name + '.json')

    return db


#************************************************
# INSERT FUNCTIONS (Better description needed)
# ***********************************************


# Cruise Title
def insert_cruise_title(cruise_title,driver):

    driver.find_element_by_id("titlewrap").find_element_by_xpath("./input").send_keys(cruise_title)
    

# Big HTML Chunk, inserted in the textbox below the title
def insert_cruise_main_info(info_html,driver):

    #Switch to text tab
    #driver.find_element_by_id("content-html").click()

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

    time.sleep(REST)

    # Once dropdown displayed, choose 'Starting From: '

    dropdown_selection = driver.find_element_by_id("select2-drop").find_element_by_class_name("select2-results").find_elements_by_xpath("./*")[3]

    dropdown_selection.click()

# Throw an 'Itinerary' on it
def insert_iten_title(driver):

    driver.find_element_by_id("tour_tabs_meta[tabs][0][title]").find_element_by_class_name("vp-input").send_keys("Itinerary")

# Make a big chunk of HTML using the itinerary list, and then do a bunch of 
def insert_day_by_day(itinerary, driver):

    big_ass_string = "[timeline]"

    n = 1

    for day in itinerary:

        day_string = '[timeline_item item_number="' + str(n) + '" title="Day ' + str(n) + '"]' + day + '[/timeline_item]'

        big_ass_string = big_ass_string + day_string

        n+=1

    big_ass_string = big_ass_string + '[/timeline]'

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

    title_bar.send_keys("Ship Details")

    time.sleep(NAP)

    text_area = driver.find_element_by_id("tour_tabs_meta[tabs][1][content]_ce")

    text_area.send_keys(ship_info)

    time.sleep(NAP)


def complete_header_information(subtitle, ship_name, driver):

    image_radio = driver.find_element_by_id("header_section_meta_metabox").find_element_by_class_name("input").find_elements_by_xpath("./*")[1].find_element_by_xpath("./input")

    image_radio.click()

    time.sleep(SLUMBER)

    #Enter subtitle

    sub_input = driver.find_element_by_id("header_section_meta[banner_subtitle]").find_element_by_class_name("vp-input")

    sub_input.click()

    #driver.execute_script("arguments[0].focus();",sub_input)

    time.sleep(NAP)

    sub_input.send_keys(subtitle)

    time.sleep(NAP)

    #Will input image here

    image_add_button = driver.find_element_by_id("header_section_meta[banner_image]").find_element_by_class_name("buttons").find_elements_by_xpath("./*")[0]

    image_add_button.click()

    time.sleep(REST)

    # Search media items
    
    search_media = driver.find_elements_by_id("media-search-input")[1]

    ship_prefix = ship_name.split()[0].lower()

    image_title = ship_prefix + "_image"

    search_media.send_keys(image_title)

    time.sleep(15)

    #Click on result

    target_image = driver.find_elements_by_class_name("attachments-browser")[1].find_element_by_xpath('./ul/li/div/div')

    target_image.click()

    '''
    #"Insert from URL" button

    insert_url_link = driver.find_element_by_id("__wp-uploader-id-0").find_element_by_class_name("media-menu").find_elements_by_xpath("./*")[6]

    insert_url_link.click()

    time.sleep(NAP)

    #Insert URL

    url_box = driver.find_element_by_id("embed-url-field")

    url_box.click()

    url_box.send_keys("")

    url_box.send_keys(ship_img)
    '''

    time.sleep(NAP)

    #Click submit button

    submit_button = driver.find_elements_by_class_name("media-frame-toolbar")[1].find_element_by_class_name("media-button-insert")

    submit_button.click()
    

    time.sleep(REST)

    #Turn off parallax

    lax_button = driver.find_element_by_id("header_section_meta[is_banner_image_parallax]").find_element_by_class_name("vp-input")

    lax_button.click()

    #Turn off image repeat

    '''repeat_dropdown = driver.find_element_by_id("header_section_meta[banner_image_repeat]").find_element_by_class_name("select2-choice")

    repeat_dropdown.click()

    no_repeat_choice = driver.find_element_by_id("select2-drop").find_elements_by_xpath("./ul/*")[1].find_elements_by_xpath("./*")[0]
    
    no_repeat_choice.click()'''

def set_product_image(driver, ship_name):

    ship_prefix = ship_name.split()[0].lower()

    image_title = ship_prefix + "_image"

    set_image_button = driver.find_element_by_id("set-post-thumbnail")

    set_image_button.click()

    time.sleep(SLUMBER)

    image_search = driver.find_element_by_id("media-search-input")

    image_search.click()

    image_search.send_keys(image_title)

    time.sleep(15)

    #Click on result

    target_image = driver.find_element_by_class_name("attachments-browser").find_element_by_xpath('./ul/li/div/div')

    target_image.click()

    time.sleep(NAP)

    #Click submit button

    submit_button = driver.find_element_by_class_name("media-frame-toolbar").find_element_by_class_name("media-button-select")

    submit_button.click()

    time.sleep(NAP)
    


#port list should not include depart port. 
def check_boxes(port_list, departure_loc, ship_name, driver):

    usa_state_list = ['Alaska', 'California', 'Florida', 'Hawaii', 'Maine', 'Maryland', 'Massachusetts', 'New Jersey', 'New York', 'Oregon', 'Rhode Island', 'South Carolina', 'Texas', 'Washington']

    ca_province_list = ['British Columbia', 'New Brunswick', 'Newfoundland', 'Nova Scotia', 'Prince Edward Island', 'Quebec']    

    check_boxes = driver.find_element_by_id("tour_categorychecklist")

    usa_dep_checkbox = check_boxes.find_element_by_id("in-tour_category-344")
    usa_dest_checkbox = check_boxes.find_element_by_id("in-tour_category-498")
    ca_dep_checkbox = check_boxes.find_element_by_id("in-tour_category-332")
    ca_dest_checkbox = check_boxes.find_element_by_id("in-tour_category-431")

    usa_dep_clicked = False
    usa_dest_clicked = False
    ca_dep_clicked = False
    ca_dest_clicked = False

    cruise_box = check_boxes.find_element_by_id("in-tour_category-710")

    cruise_box.click()

    for item in port_list:
        if(len(item.split(', ')) > 1):
            state = item.split(', ')[1].strip()
        else:
            state = item.split(', ')
        print(state)
        if (state in usa_state_list and usa_dest_clicked == False):
            usa_dest_checkbox.click()
            usa_dest_clicked = True
        if (state in ca_province_list and ca_dest_clicked == False):
            ca_dest_checkbox.click()
            ca_dest_clicked = True

    if(len(departure_loc.split(', ')) > 1):
        if(departure_loc.split(', ')[1].strip() in usa_state_list):
            usa_dep_checkbox.click()
        if(departure_loc.split(', ')[1].strip() in ca_province_list):
            ca_dep_checkbox.click()
    else:
        irrelevant_string = "suck a dick"

    royal_caribbean_section = check_boxes.find_element_by_id("tour_category-185")
    royal_caribbean_box = check_boxes.find_element_by_id("in-tour_category-185")

    royal_caribbean_box.click()

    rc_ships = royal_caribbean_section.find_elements_by_xpath('./ul/*')

    for element in rc_ships:
        list_item = element.find_element_by_xpath('./label')        
        list_text = list_item.text
        list_box = list_item.find_element_by_xpath('./input')

        if(ship_name in list_text):
            list_box.click()


    departures = check_boxes.find_element_by_id("tour_category-326")

    departure_children = departures.find_elements_by_xpath('.//label')

    destinations = check_boxes.find_element_by_id("tour_category-216")  
    
    destination_children = destinations.find_elements_by_xpath(".//label")

    checked_country = []
    checked_city = []

    for item in port_list:
        text = item.split(', ')
        if(len(text) > 1):
            city = text[0].strip()
            if('(' in city):
                city = city.split('(')[0].strip()
            state = text[1].strip()
            print("Finding " + city + ", " + state + " in checkboxes")
        else:
            city = 'Something that would never be in the checklist'
            state = text[0].strip()
            print("Finding " + state + " in checkboxes")
        for element in destination_children:
            if (city in element.text and city not in checked_city):
                element.find_element_by_xpath('./input').click()
                checked_city.append(city)
            if (state in element.text and state not in checked_country):
                element.find_element_by_xpath('./input').click()
                checked_country.append(state)
    
    dep_text = departure_loc.split(', ')
    if(len(dep_text) > 1):
        dep_city = dep_text[0].strip()
        if('(' in dep_city):
            dep_city = dep_city.split('(')[0].strip()
        dep_state = dep_text[1].strip()
    else:
        dep_city = "My neck, my back"
        dep_state = dep_text[0].strip()

    for item in departure_children:
        if(dep_city in item.text):
            item.find_element_by_xpath('./input').click()
        if(dep_state in item.text):
            item.find_element_by_xpath('./input').click()
    


def change_product_data(driver):
    dropdown = driver.find_element_by_id("product-type")
    dropdown.click()

    tour_button = dropdown.find_elements_by_xpath("./optgroup/option")[4]

    tour_button.click()

def insert_prices(driver, regular_price, sales_price):

    price_parent = driver.find_element_by_id("general_product_data")
    price_parent = price_parent.find_elements_by_xpath('./div')[1]

    regular = price_parent.find_elements_by_xpath("./p")[0]
    sales = price_parent.find_elements_by_xpath("./p")[1]

    regular_field = regular.find_element_by_xpath('./input')
    sales_field = sales.find_element_by_xpath('./input')

    regular_field.send_keys(str(regular_price))
    sales_field.send_keys(str(sales_price))

def click_tour_booking(driver):

    button_list = driver.find_element_by_id("woocommerce-product-data").find_element_by_class_name('product_data_tabs').find_elements_by_xpath('./li')

    for button in button_list:
        target_button = button.find_element_by_xpath('./a')
        button_text = target_button.text
        if("Tour Booking" in button_text):
            target_button.click()


def enter_keyword(driver, cruise_title):

    focus_keyword = driver.find_element_by_id("yoast_wpseo_focuskw_text_input")

    #Scroll to it
    driver.execute_script("return arguments[0].scrollIntoView(true);",focus_keyword)
    driver.execute_script("window.scrollBy(0,-350)")

    time.sleep(NAP)

    focus_keyword.send_keys(cruise_title)

def enter_dates(driver, departure_dates, return_dates):

    i = 0
    add_period_button = driver.find_element_by_id("tour_booking_tab").find_element_by_class_name("add_row_btn")


    for depart in departure_dates:
        #Scroll to it
        driver.execute_script("return arguments[0].scrollIntoView(true);",add_period_button)
        driver.execute_script("window.scrollBy(0,-350)")

        add_period_button.click()
        time.sleep(NAP)

        booking_row = driver.find_element_by_id("tour_booking_rows_cont").find_elements_by_xpath('./tr')[i]
        
        day_checks = booking_row.find_elements_by_class_name("tour-booking-row__days__column")

        for col in day_checks:
            days = col.find_elements_by_xpath('./div')
            for mon in days:
                mon.find_element_by_xpath('./input').click()

        dates_available = booking_row.find_elements_by_class_name("tour-booking-row__date-wrapper")

        start_date_available = dates_available[0].find_element_by_xpath('./input')

        end_date_available = dates_available[1].find_element_by_xpath('./input')

        start_date_available.send_keys(departure_dates[i])

        end_date_available.send_keys(return_dates[i])

        #Click something after so calendar go away
        limit_button = booking_row.find_element_by_name("tour-booking-row[" + str(i) + "][limit]")

        limit_button.click()

        time.sleep(NAP)

        i+=1

    #driver.find_element_by_class_name("save_ranges_btn").click()

    time.sleep(NAP)

def insert_short_description(driver, cruise_title, cruise_ship, port_tags):

    short_desc = driver.find_element_by_id("excerpt")

    desc_string = ""
    new_title = ""

    split_title = cruise_title.split()

    for word in split_title:
        if("-" not in word):
            new_title = new_title + word + " "

    new_title = new_title.strip()

    if(len(port_tags) > 1):
        new_title = new_title + ", aboard the " + cruise_ship + ", that visits "
        
        last_port = port_tags[(len(port_tags)-1)]
        port_tags = port_tags[:(len(port_tags)-1)]

        for port in port_tags:
            if('(' in port):
                state = port.split('(')[0].strip()
            else:
                state = port.strip()

            new_title = new_title + state + ", "

        new_title = new_title[:(len(new_title) - 2)]

        new_title = new_title + " and " + last_port

        short_desc.send_keys(new_title)

    else:
        new_title = new_title + ", aboard the " + cruise_ship + ", that visits "

        if('(' in port_tags[0]):
            port_name = port_tags[0].split('(')[0].strip()
        else:
            port_name = port_tags[0]
        new_title = new_title + port_name

        short_desc.send_keys(new_title)

def fill_out_product_tags(driver, port_tags, cruise_ship):

    new_title = ""    

    for port in port_tags:
        if('(' in port):
            state = port.split('(')[0].strip()
        else:
            state = port.strip()

        new_title = new_title + state + ", "

    tag_input = driver.find_element_by_id("new-tag-product_tag")

    new_title = new_title + cruise_ship + ", Royal Caribbean, Cruises"

    tag_input.send_keys(new_title)

    time.sleep(NAP)

    tag_submit = driver.find_element_by_id("product_tag").find_element_by_class_name('tagadd')
    
    time.sleep(NAP)

    add_media = driver.find_element_by_id("setting-error-tgmpa")

    #Scroll to it
    driver.execute_script("return arguments[0].scrollIntoView(true);",add_media)
    driver.execute_script("window.scrollBy(0,400)")

    time.sleep(NAP)

    tag_submit.click()

    time.sleep(NAP)

def publish_ship(driver):

    publish_button = driver.find_element_by_id("publish")

    add_media = driver.find_element_by_id("setting-error-tgmpa")

    #Scroll to it
    driver.execute_script("return arguments[0].scrollIntoView(true);",add_media)
    driver.execute_script("window.scrollBy(0,200)")

    time.sleep(NAP)

    publish_button.click()

    time.sleep(7)
    try:
        publish_button.click()
    except StaleElementReferenceException:
        pass

    

        
        

def get_individual_result_info(driver, ship_name):

    #**********************
    # SAMPLE TESTING DATA
    #**********************

    db = init_db(ship_name)

    db_len = len(db.all())

    not_written = []

    #Change for index to start at in input
    i = 1

    while(i < (db_len + 1)):

        entry = db.get(eid=i)

        try:

            cruise_title = entry['cruise_name']

            port_text_list = entry['port_list']
    
            if not ("Sampler" in cruise_title or len(port_text_list)<2):

                cruise_duration = int(cruise_title.split()[0])

                cruise_ship = entry['ship_name']

                cruise_html_chunk = switch_ship(cruise_ship)

                departure_location_text = entry['departure_loc']

                arrival_location_text = entry['return_loc']

                check_port_list = port_text_list[1:]

                port_tag_list = entry['port_tags']

                price_text = entry['regular_price']

                sale_price_text = entry['sale_price']

                cruise_subtitle = entry['cruise_sub']

                itinerary = entry['cruise_itin']

                departure_dates = entry['available_departure_dates']

                return_dates = entry['available_return_dates']


                #*****************************
                # RUN INTERACTION FUNCTIONS
                #*****************************

                #Insert Title
                insert_cruise_title(cruise_title,driver)

                if(arrival_location_text == departure_location_text):
                    port_string = create_port_list(port_text_list[1:])
                    
                else:
                    port_string = create_port_list(port_text_list[1:(len(port_text_list) - 1)])

                html_input = test_HTML_input(departure_location_text, arrival_location_text, port_string, price_text)


                fill_out_product_tags(driver, port_tag_list, cruise_ship)

                #Insert Departure, port, features HTML
                insert_cruise_main_info(html_input,driver)

                #Select Badge (Starting From:)
                select_badge_dropdown(driver)

                #Insert 'Itinary' Title
                insert_iten_title(driver)

                #Insert HTML chunk for day by day locations
                insert_day_by_day(itinerary, driver)

                insert_ship_info(driver, cruise_html_chunk)

                set_product_image(driver, cruise_ship)

                complete_header_information(cruise_subtitle, cruise_ship, driver)

                check_boxes(check_port_list, departure_location_text, cruise_ship, driver)

                change_product_data(driver)

                time.sleep(2)

                insert_prices(driver, price_text, sale_price_text)

                time.sleep(2)

                click_tour_booking(driver)

                time.sleep(2)

                enter_dates(driver, departure_dates, return_dates)

                time.sleep(2)

                enter_keyword(driver, cruise_title)

                time.sleep(2)

                try:
                    insert_short_description(driver, cruise_title, cruise_ship, port_tag_list[1:])
                except IndexError:
                    insert_short_description(driver, cruise_title, cruise_ship, check_port_list)

                time.sleep(2)

                publish_ship(driver)
                print("Finished index: " + str(i))

                time.sleep(REST)

            else:
                not_written.append("Index " + str(i) + " was not written: " + cruise_title)

                print("Index " + str(i) + " was not written: " + cruise_title)

        except(WebDriverException) as e:
            i -= 1
            pass
    
        i += 1

        try:
            drive.get("http://7eb.8aa.myftpupload.com/wp-admin/post-new.php?post_type=product")
        except (UnexpectedAlertPresentException) as e:
            alert = drive.switch_to_alert()
            alert.accept()
            time.sleep(NAP)
            drive.get("http://7eb.8aa.myftpupload.com/wp-admin/post-new.php?post_type=product")
        except(TimeoutException) as e:
            drive.get("http://7eb.8aa.myftpupload.com/wp-admin/post-new.php?post_type=product")

        time.sleep(REST)

    if(len(not_written) > 0):
        print("Indexes not written: ")
        for item in not_written:
            print(item)
    else:
        print("All indexes written. Nice.")



if __name__ == "__main__":

    ship_list = ['radiance', 'rhapsody', 'serenade', 'vision']

    drive = init_driver()

    #link = "file:///home/chris/Downloads/Add%20New%20Product%20%E2%80%B9%20Interline%20Advantage%20%E2%80%94%20WordPress.html"

    link = "http://7eb.8aa.myftpupload.com/wp-admin/post-new.php?post_type=product"

    drive.get(link)

    time.sleep(HIBERNATE)

    drive.get(link)

    time.sleep(NAP)

    for ship in ship_list:
        get_individual_result_info(drive, ship)

    drive.close()




from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tinydb import TinyDB, Query
import time
import os
from datetime import datetime, timedelta
from LearnMoreScrape import get_itin_learn_more


#Initialize TinyDB for storing cruise info
def init_db():

    db = TinyDB('cruise.json')
    return db


def print_individual_entry():

    db = init_db()

    i = 1

    incorrect_list = []

    db_len = len(db)

    while(i < (db_len + 1)):

        entry = db.get(eid=i)

        #*************************************
        # Print Results (For Testing Purposes)
        #*************************************

        print("\n\n**************************************************************\n" + entry['cruise_name'] + "\n**************************************************************")

        print("\nCruise Title: " + entry['cruise_name'])

        print("\nDeparture Location: " + entry['departure_loc'])

        print("\nReturn Location: " + entry['return_loc'])

        print("\nShip Name: " + entry['ship_name'])

        print("\nPort Locations:")
        for item in entry['port_list']:
	        print(item)
 
        print("\nPort Tags:")       
        for item in entry['port_tags']:
            print(item)

        print("\nCruise Subtitle: " + entry['cruise_sub'])

        print("\nDates:")

        n = 0

        for item in entry['available_departure_dates']:
            print(item + " - " + entry['available_return_dates'][n])
            n += 1


        print("\nPrices:")

        print("Regular Price: " + entry['regular_price'])

        print("Sale Price: " + entry['sale_price'])

        print("\nItinerary:")
        for item in entry['cruise_itin']:
            print(item)

        len_trip = int(entry['cruise_name'].split()[0]) + 1
        itin_len = len(entry['cruise_itin'])

        if(len_trip != itin_len):
            incorrect_list.append(entry['cruise_name'])
        

        print("\n\n**************************************************************\n**************************************************************")

        i += 1

    print("Incorrect Entries (" + str(len(incorrect_list)) + "):\n")
    for item in incorrect_list:
        print(item)

        

if __name__ == "__main__":

    print_individual_entry()

    

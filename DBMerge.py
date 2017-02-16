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

def get_dbs():
    
    db1 = TinyDB('cruise1.json')
    db2 = TinyDB('cruise2.json')

    dbList = []
    dbList.append(db1)
    dbList.append(db2)

    return dbList


def print_individual_entry():

    mainDb = init_db()

    i = 1

    incorrect_list = []

    db_len = len(mainDb)

    dbList = get_dbs()

    for db in dbList:
        
        i =1

        while(i < (len(db) + 1)):

            entry = db.get(eid=i)

        #********************************************
        # Get information to write to merged database
        #********************************************

            cruise_name = entry['cruise_name']

            departure_loc = entry['departure_loc']

            return_loc = entry['return_loc']

            ship_name = entry['ship_name']

            port_list = entry['port_list']
 
            port_tags = entry['port_tags']

            cruise_sub = entry['cruise_sub']

            available_departure_dates = entry['available_departure_dates']
            available_return_dates = entry['available_return_dates']
            

            regular_price = entry['regular_price']

            sale_price = entry['sale_price']

            cruise_itin = entry['cruise_itin']
        
            i += 1

            mainDb.insert({'cruise_name': cruise_name, 'ship_name': ship_name, 'departure_loc': departure_loc, 'return_loc': return_loc, 'port_list': port_list, "cruise_sub": cruise_sub, 'port_tags': port_tags, 'cruise_itin': cruise_itin, 'available_departure_dates': available_departure_dates, 'available_return_dates': available_return_dates, 'regular_price': regular_price, 'sale_price': sale_price})
        

if __name__ == "__main__":

    print_individual_entry()

    

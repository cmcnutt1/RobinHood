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

def get_dbs(ship_name):
    
    db1 = TinyDB('cruise.json')
    db2 = TinyDB('individual_ships/' + ship_name + '.json')

    dbList = []
    dbList.append(db1)
    dbList.append(db2)

    return dbList


def print_individual_entry(ship_prefix):

    two_dbs = get_dbs(ship_prefix.lower())

    mainDb = two_dbs[0]

    shipDb = two_dbs[1]

    i = 1

    db_len = len(mainDb)


    while(i < (db_len + 1)):

        entry = mainDb.get(eid=i)

    #********************************************
    # Get information to write to merged database
    #********************************************
        ship_name = entry['ship_name']
 
        if(ship_prefix in ship_name):

            cruise_name = entry['cruise_name']

            departure_loc = entry['departure_loc']

            return_loc = entry['return_loc']



            port_list = entry['port_list']
     
            port_tags = entry['port_tags']

            cruise_sub = entry['cruise_sub']

            available_departure_dates = entry['available_departure_dates']
            available_return_dates = entry['available_return_dates']
                

            regular_price = entry['regular_price']

            sale_price = entry['sale_price']

            cruise_itin = entry['cruise_itin']

            shipDb.insert({'cruise_name': cruise_name, 'ship_name': ship_name, 'departure_loc': departure_loc, 'return_loc': return_loc, 'port_list': port_list, "cruise_sub": cruise_sub, 'port_tags': port_tags, 'cruise_itin': cruise_itin, 'available_departure_dates': available_departure_dates, 'available_return_dates': available_return_dates, 'regular_price': regular_price, 'sale_price': sale_price})
            
        i += 1

if __name__ == "__main__":

    ship_list = ['Harmony', 'Oasis', 'Freedom', 'Independence', 'Liberty', 'Adventure', 'Explorer', 'Mariner', 'Navigator', 'Brilliance', 'Jewel', 'Radiance', 'Serenade', 'Enchantment', 'Grandeur', 'Legend', 'Rhapsody', 'Vision', 'Majesty']

    for item in ship_list:
        print(item + "Working...")
        print_individual_entry(item)
        print(item + "Done")

    

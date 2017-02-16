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

    

    dating_errors = []

    more_days_errors = []

    #Don't think this is a problem. But I'll test for it anyways
    less_days_errors = []

    pricing_errors = []

     
    i =1

    while(i < (db_len + 1)):

        entry = mainDb.get(eid=i)

    #********************************************
    # Get information to write to merged database
    #********************************************

        cruise_name = entry['cruise_name']

        cruise_len = cruise_name.split()[0]

        departure_loc = entry['departure_loc']

        return_loc = entry['return_loc']

        ship_name = entry['ship_name']

        port_list = entry['port_list']
 
        port_tags = entry['port_tags']

        cruise_sub = entry['cruise_sub']

        available_departure_dates = entry['available_departure_dates']
        available_return_dates = entry['available_return_dates']

        if(len(available_departure_dates) < 1):
            dating_errors.append(cruise_name)
            

        regular_price = entry['regular_price']

        if(int(regular_price) < 100):
            pricing_errors.append(cruise_name)

        sale_price = entry['sale_price']

        cruise_itin = entry['cruise_itin']

        i += 1

        if((int(cruise_len) + 1) != len(cruise_itin)):
            more_days_errors.append(cruise_name)

    #************************
    # Testing Print Outs
    #************************
    print("\n\nMore/Less Days Errors:\n**********************\n")
    
    if(len(more_days_errors) == 0):
        print("\nNo difference in expected cruise lengths. Nice")

    else:
        
        for err in more_days_errors:
            print(err)

    print("\n\nNo Dates Available Errors:\n**************************\n")

    if(len(dating_errors) == 0):
        print("\nNo dating errors. Nice")
    else:
        for err in dating_errors:
            print(err)

    print("\n\nPricing Errors:\n***************\n")

    if(len(pricing_errors) == 0):
        print("\nNo pricing errors. Nice\n\n")

    else:
        for err in pricing_errors:
            print(err)
        print("\n\n")
            
        

if __name__ == "__main__":

    print_individual_entry()

    

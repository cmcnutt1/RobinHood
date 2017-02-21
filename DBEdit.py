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

def fix_depart(db_list, list_search, list_entry):

    new_itin = []
    db = init_db()
    for item in db_list:
        index_item = db.get(eid=item)
        itin_list = index_item['cruise_itin']
        return_loc = index_item['return_loc']
        for yo_momma in itin_list:
            if(list_search in yo_momma):
                if("Tendered" in yo_momma):
                    new_itin.append("Tendered at " + list_entry)
                elif("Docked" in yo_momma):
                    new_itin.append("Docked at " + list_entry)
                elif("Depart" in yo_momma):
                    new_itin.append("Depart from " + list_entry)
                elif("Disembark" in yo_momma):
                    new_itin.append("Disembark at " + list_entry)
            else:
                new_itin.append(yo_momma)
        
        db.update({'return_loc': list_entry}, eids = [item])
        db.update({'cruise_itin': new_itin}, eids = [item])        

        print("New Itin:")
        print(db.get(eid=item)['cruise_itin'])

        print("New Return:")
        print(db.get(eid=item)['return_loc'])
        new_itin = []

def fix_city(db_list, list_search, list_entry, tag_search, tag_entry):

    new_list = []
    new_tags = []
    new_itin = []
    db = init_db()
    for item in db_list:
        index_item = db.get(eid=item)
        port_list = index_item['port_list']
        port_tags = index_item['port_tags']
        itin_list = index_item['cruise_itin']
        for yo_momma in port_list:
            if(list_search in yo_momma):
                new_list.append(list_entry)
            else:
                new_list.append(yo_momma)

        for yo_daddy in port_tags:
            if(tag_search in yo_daddy):
                addition = tag_entry
            else:
                addition = yo_daddy
            if not (addition in new_tags):
                new_tags.append(addition)

        for yo_granny in itin_list:
            if(list_search in yo_granny):
                if("Tendered" in yo_granny):
                    new_itin.append("Tendered at " + list_entry)
                elif("Docked" in yo_granny):
                    new_itin.append("Docked at " + list_entry)
                elif("Depart" in yo_granny):
                    new_itin.append("Depart from " + list_entry)
                elif("Disembark" in yo_granny):
                    new_itin.append("Disembark at " + list_entry)
            else:
                new_itin.append(yo_granny)
                    
        db.update({'port_list': new_list}, eids = [item])
        db.update({'port_tags': new_tags}, eids = [item])
        db.update({'cruise_itin': new_itin}, eids = [item])
        print("\nEntry: " + str(item) + "\n")
        print("New List:")
        print(db.get(eid=item)['port_list'])
        print("New Tags:")
        print(db.get(eid=item)['port_tags'])
        print("New Itin:")
        print(db.get(eid=item)['cruise_itin'])
        new_list = []
        new_tags = []
        new_itin = []


def get_individual_entry(query):

    mainDb = init_db()

    i = 1

    incorrect_list = []

    db_len = len(mainDb)

    

    dating_errors = []

    more_days_errors = []

    #Don't think this is a problem. But I'll test for it anyways
    less_days_errors = []

    pricing_errors = []

    diff_depart = []

    diff_arrive = []

    same_depart = []

    all_ports = []

    target_items = []

     
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

        '''if (query in return_loc):
            target_items.append(i)'''

        ship_name = entry['ship_name']

        port_list = entry['port_list']

        for item in port_list:
            word_list = item.split(', ')
            city = word_list[0]
            if(len(word_list) > 1):
                state = word_list[1]
                if ( '(' in state):
                    target_items.append(i)
 
        port_tags = entry['port_tags']

        

        cruise_sub = entry['cruise_sub']

        available_departure_dates = entry['available_departure_dates']
        available_return_dates = entry['available_return_dates']

        regular_price = entry['regular_price']

        sale_price = entry['sale_price']

        cruise_itin = entry['cruise_itin']

        i += 1

    #************************
    # Testing Print Outs
    #************************
    '''print("\n\nMore/Less Days Errors:\n**********************\n")
    
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
        print("\n\n")'''

    '''print("\n\nWhere departure/return location is same:\n*****************************************")
    for item in same_depart:
        print(item)

    print("\n\nWhere departure/return locations are different:\n************************************************")

    print("\nDepartures:\n")

    for item in diff_depart:
        if(item in same_depart):
            something = 0

        else:
            print(item)

    print("\nArrivals:\n")

    for item in diff_arrive:
        if(item in same_depart or item in diff_depart):
            something = 0

        else:
            print(item)

    print("\n\nAll unique ports (Excluding arrival/departures):\n*************************************************")

    for item in all_ports:
        if(item in diff_depart or item in diff_arrive or item in same_depart):
            something = 0
        else:
            print(item)
    '''

    print(target_items)
    for item in target_items:
        print(mainDb.get(eid=item))
    return target_items        
        

if __name__ == "__main__":
    
    list_query = "Canada"
    list_entry = "Gibraltar"

    tag_query = "United Kingdom"
    tag_entry = "Gibraltar"

    print(list_query + "\n")

    a_list = get_individual_entry(list_query)

    #fix city (db_list, list_search, list_entry, tag_search, tag_entry)
    # zadqwfix_city(a_list, list_query, list_entry, tag_query, tag_entry)

    #fix_depart(a_list, list_query, list_entry)
    

#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests_html,time,yahoo_fin,collections,csv
from datetime import datetime as dt,time as t
from yahoo_fin import stock_info as si

#Setup Working Dir., lists, and Dicts. Replace * with your current user file path. 
wd = "C://Users//*//Desktop//"

stocks = {}

# Add tickers that you want to track live price for to Tockers
tockers = ["aapl","amzn","^gspc"]


# In[ ]:


#Function to setup necessarry dictionaries.
def make_dicts(tockers = []):
    for x in tockers:
        stocks[x]= {}
make_dicts(tockers)
print (stocks)
print ("Dictionaries Created Successfully!")

# Function to check that the time is during market hours. 
def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current sys time
    check_time = check_time or dt.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time
# Should return True if the time is correct.   
is_time_between(t(9,30), t(16,0))

#Funtion to get live price from Yahoo Finance
def get_price(a_ticker):
    return(si.get_live_price(a_ticker))
print("Function: get_price Defined Successfully!")

#Function to write a dictionary key values into .csv file
def write_to_file(k,v):
    fname = wd+"{}_{}.csv".format(k,dt.now().strftime("%m.%d.%y"))
    with open(fname, 'w') as f:
        w = csv.writer(f, delimiter = ',')
        for (key, value) in v.items():
            w.writerow([key, value])
        print("File {}_{}.csv successfully created".format(k,dt.now().strftime("%m.%d.%y")))
print("Function: write_to_file Defined Successfully!")

#Function to update the dictionaries with the live price associated with the ticker
def update_stocks_dict(a_dict):
    print("Updating")
    for (k, v) in a_dict.items():
        v.update({dt.now().strftime("%H:%M") : get_price(k)})
        print("Got {}".format(k.upper()))  
        write_to_file(k,v)
print("Function: update_stocks_dict Defined Successfully!")

#Update passes all previous functions to get the live price and timestamp it, then write it to the appropriate
#csv fiile on the desktop. Only works during Market Hours. Will quit otherwise. 
def update():
    print ("Lets get some stocks!")
    try:
        while is_time_between(t(9,30), t(16,0)) is True:
            for i in range(1):
                update_stocks_dict(stocks)
                print ("\nSleeping zzz...")
                time.sleep(20)
                # time.sleep is in seconds. 300 = 5min, 600 = 10 min.
                #If the trading day ends while it is asleep, it must finish the sleep period
                #prior to terminating the script. 
        print("The trading day has ended.")      
    except KeyboardInterrupt:
            print('\nProcess stopped by user.')
           # Handle the Ctrl-C exception to keep its error message from displaying.
print("Function: update Defined Succesffully!")


# In[ ]:


#Run this cell to run the program!
update()


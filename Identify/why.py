from bs4 import BeautifulSoup as BS
from bs4 import SoupStrainer

import urllib.request
from urllib.request import urlopen as request
import time
import re 
import requests
import datetime
import os 

from multiprocessing import Pool 
import threading
from multiprocessing.pool import ThreadPool

from retrieve import pull_reddit_data, pull_facebook_data, pull_twitter_data

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

def get_data():
    data = []
    # facebook_data = pull_facebook_data()
    reddit_data = pull_reddit_data()
    # twitter_data = pull_twitter_data()
    for sheet in reddit_data:
        for entries in sheet:
            data.append(entries)
    # for sheet in facebook_data:
    #     for entries in sheet:
    #         data.append(entries)
    # for sheet in twitter_data:
    #     for entries in sheet:
    #         data.append(entries)
    return data

# svg_data = []
# def open_url(entry):
#     url_entry = entry['Post URL']
#     print("Trying to open", url_entry)
#     if(url_entry):
#         # try:
#             op = webdriver.ChromeOptions()
#             op.add_argument('headless')        
#             driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
#             driver.implicitly_wait(10)
#             driver.get(url_entry)
#             driver.refresh()

#             try:
#                 custom_strainer = SoupStrainer(["svg","g"])
#                 page_soup = BS(driver.page_source, 'html.parser', parse_only=custom_strainer)

#                 if(page_soup is not None):
#                     svg_data.append(entry)
#                     return page_soup
#             except (RuntimeError, TypeError, NameError):
#                     print("Error with", url_entry)
                    # driver.close()
        # except (RuntimeError, TypeError, NameError):
        #     print("Something went wrong when opening this url", url_entry)

    

# def thread_task(lock,data_set):
#     lock.acquire()
#     open_url(entry)
#     lock.release()

# if __name__ == "__main__":
#     start = time.time()

#     entries = get_data()
#     # guess a thread pool size which is a tradeoff of number of cpu cores,
#     # expected wait time for i/o and memory size.
#     pool = Pool[2]
#     results = pool.map(open_url(entry), entries)

#     # with ThreadPool(50) as pool:
#     #     pool.map(open_url, entries, chunksize=1)
#     print("Elapsed Time: %s" % (time.time() - start))





#This function pulls 
# def inspect():
#     svg_data = []
#     data = get_data()
#     for entry in data:
        
#         url_entry = entry['Post URL']
#         if url_entry:
#             contents = open_url(url_entry)
#             if(contents is not None):
#                 svg_data.append(entry)

#         else:
#             continue
            #THIS IS USEFUL. THIS IS HOW WE GET THE SVG AND SAVE IT LOCALLY
            #WE CAN LEVERAGE THE INDEX OF THE SHEET TO CONNECT THE POST TO THE DENSITY SCORE

            # svg = contents[int(start):(int(end)+6)]
            # filename = file_name(url_entry)
            # path = ""
            # write_text(svg, path, filename)


    # print(svg_data)
    # push_to_svg_sheet(svg_data)



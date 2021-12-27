from bs4 import BeautifulSoup as BS
import urllib.request
import time
import re 
import requests
import datetime
import os 

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
    facebook_data = pull_facebook_data()
    reddit_data = pull_reddit_data()
    twitter_data = pull_twitter_data()
    for sheet in reddit_data:
        for entries in sheet:
            data.append(entries)
    for sheet in facebook_data:
        for entries in sheet:
            data.append(entries)
    for sheet in twitter_data:
        for entries in sheet:
            data.append(entries)
    return data
  

def file_name(link: str):
    raw_company = link.split("www.")
    date = datetime.datetime.now().strftime("%m/%d/%y")
    filename = date +  "_" + raw_company[1]
    final = filename.replace(".html", "")
    final = filename.replace("/", "-")
    return final


def write_text(data: str, path: str, filename: str):
    print("%s.svg" % filename)
    data_bytes = data.encode(encoding='UTF-8')
    with open("../data/%s.svg" % filename, "wb") as f:
        f.write(data_bytes)

def push_to_svg_sheet(df):
    credentials = {
        "type": "service_account",
        "project_id": "reddit-334418",
        "private_key_id": "dbc7344c3125d43531babfcee6706a230f58f675",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQClgTpRDRNajJuJ\nsdw+QtludCube8RbOpc4Ea+w/w+rG+ll6dOnnG67b9mI6NWwty8GtsA1GZ0xIdJ+\nh+6NPqL5ZPp92J/eQnhIZNLC0r3QZxRs5eNRxkJnAzTHo085MAMWZbB0Vdwm4O5n\nebDYnV+gliktgm3vrhgwafC3ecR2NgwonuQ/Ib1DYNjpR/OTG8vD0fu2zFoFZRU/\nqRy1rsKwizzDJgh/ifQ9yRMZ90mOos9CMrcT+TSCi43o3Hqj/L7Bnsv5XZ3qi/sg\nPurakZJMQbsMZOUl0NqkMKONIZ5qY37Q896FtvqKJl1df1ntJMI31siyAGFfxaAa\nWlBk3JmZAgMBAAECggEABOACT+JNJOzzEscakB7uizulEAtBG49liuf5UZU4n6Tz\nQlQ+LsooHNhxTFvQh5FSWAFIpGMzMJJNeR88MJ7mIlUOHrFsrBl42LEOcoXOVmOZ\nw/5DPuSt/FQ7tHra2dVipC6txcZW0MSkztBUZV0J66IFQw/FL80tbYMTpD9UHJD0\nRv3Ktv5jx1FtaaZkME/zJnyejgCQ/rerVcGs1pjjU8zdMhtSvTa1s9sYAvlzu/8k\n1pefkLsZuVP/pO4GrVN7d5v3TjF8nv6Y7Ira//5h1ke7a9VaZjQwGskQbT2wji30\nxyTrw3B1WieHbnkgyAkZg9m63aDijGF4dVi+qIRrjQKBgQDY593pE8SSCLRYQ1gG\nKtU8+un+9bz/NuTJXBKLafzP2s0J43ZfSjn0QNxh6FBeVb+XaaxXVM6wh+NXAsh/\nyUolU0YIzsuRkIZIksw9Z9IyzKWzNvIVcQHYu6KH7fmwhKFMhotVEpqWoXD8cQvP\nI2KG6b7j5iCOkIU/HAhHQVUCBwKBgQDDVbKQtaWC1JdggffeHs7+PEqIQaQDqUMx\nWQtIasgkkXqMM7aFPJ9Z/sBXWVsCER6rbLTEhgkEjpOMpuwT3xc0Sr+8/PXRGsF9\nA+G3ZTB1I+X+E/ofH9z3eTHRqLBNKzyfdK0SfGIibjpK92coC6UxMfdAcPkD9G/9\nRhM2394fXwKBgDzxuSo6Aas+gt2h3mOtOUju/zxB856J3/KryhId74i/Y4j5vlK7\n2ljEuKdRzPMUiMaUTHYlQAXdyIS0JX2yIwElyrHC2PPHddOCW5yNRUQ8t/oI4DAi\nFnC9F8e1l8h/G4sS6qc2mPTl24cyhCzpNk/N8XK7QD6OYMIAsFrFAouVAoGBAINZ\nTAK88rfgBo6xtqBZLS2OEzw+j3Ca0AEN9GVU0JKudK50U6aSVkEo6eOSxXzFUE9L\ngN6plsTGrvckg5j1KeBS503I9+8NQ9Cx3IT6+TO72PsaKdXmEisjBtoJycuKaHB8\n/6hvlXm7j107sdUex40mITHnBbugEfJIvcDnlrCXAoGAcJmYYZB3IMn9/yEduBeu\nBIWM9IgOLBf/PIle15QSZmydPmTZAAFCHSa828qhrrvXPd/r1V2cJKmyihuNylCR\n1HBhn56BdMqvqXPfBFArL4fsgttEejBsZGD0bvsnLdBPiLg8SN9BD4w8qVVs+EpO\n1CvQnHOeuo6UctJX/snnRc0=\n-----END PRIVATE KEY-----\n",
        "client_email": "reddit@reddit-334418.iam.gserviceaccount.com",
        "client_id": "106682552318210817559",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/reddit%40reddit-334418.iam.gserviceaccount.com"
    } 
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open("svg_data")
    # date_string = datetime.now().strftime("%m/%d/%y")
    worksheet = sh.add_worksheet(title="data", rows="1700", cols="15")
    set_with_dataframe(worksheet, df)


#This function pulls 
def inspect():
    svg_data = []
    data = get_data()
    # Loop over entire structure here instead
    for entry in data:
        url_entry = entry['Post URL']
        #ALL MUST BE IN LOOP:
        op = webdriver.ChromeOptions()
        op.add_argument('headless')        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
        driver.implicitly_wait(10)
        driver.get(url_entry)
        driver.refresh()
        contents = driver.page_source
        start = contents.find("<svg")
        end = contents.find("</svg>")
        print ("Substring found at indexes:", start, end)
        if(start is not "-1" and end is not "-1"):
            svg_data.append(entry)

            #THIS IS USEFUL. THIS IS HOW WE GET THE SVG AND SAVE IT LOCALLY
            #WE CAN LEVERAGE THE INDEX OF THE SHEET TO CONNECT THE POST TO THE DENSITY SCORE

            # svg = contents[int(start):(int(end)+6)]
            # filename = file_name(url_entry)
            # path = ""
            # write_text(svg, path, filename)


        driver.close()
        print(svg_data)
        # push_to_svg_sheet(svg_data)


#We need to find a way to connect data details to their data entry
#I think instead of saving svgs immediately we need to push everything into a sheet that has useful data 
#Therefore instead of saving as svgs immediately we should write data struct details to sheet and read/save urls from there

inspect()
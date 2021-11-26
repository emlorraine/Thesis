from bs4 import BeautifulSoup as BS
import urllib.request
import time
import re 
import requests
import datetime
import os 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



BASE_URL = "https://www.cnn.com/interactive/2019/business/us-minimum-wage-by-year/index.html"



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
    with open("%s.svg" % filename, "wb") as f:
        f.write(data_bytes)

def inspect(link: str):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.implicitly_wait(10)
    driver.get(BASE_URL)
    driver.refresh()
    contents = driver.page_source
    start = contents.find("<svg")
    end = contents.find("</svg>")
    print ("Substring found at indexes:", start, end)
    if(start is not "-1" and end is not "-1"):
        svg = contents[int(start):(int(end)+6)]
        filename = file_name(link)
        path = ""
        write_text(svg, path, filename)
    driver.close()


inspect(BASE_URL)

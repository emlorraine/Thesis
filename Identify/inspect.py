from bs4 import BeautifulSoup as BS
import urllib.request
import time
import re 
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



BASE_URL = "https://www.washingtonpost.com/graphics/2018/politics/whos-getting-outspent/?utm_term=.793f3c3d43a5"

def inspect(link):
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
        print(svg)
        write_text(svg, './test.svg')
    driver.close()


# def download(svg_string):
#     svg2png(bytestring=svg_code,write_to='output.png')

def write_text(data: str, path: str):
    with open(path, 'w') as file:
        file.write(data)

inspect(BASE_URL)
import os

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re



def scrape_image(url):
    html = urlopen('https://en.wikipedia.org/wiki/Peter_Jeffrey_(RAAF_officer)')
    bs = BeautifulSoup(html, 'html.parser')
    images = bs.find_all('img', {'src':re.compile('.jpg')})
    for image in images: 
        print(image['src']+'\n')


def open(url):
    os.system("open \"\" "+url)
    scrape_image(url)
    


open("https://www.studlife.com")
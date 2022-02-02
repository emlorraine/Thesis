from random import sample
from matplotlib import image
import scrapy 
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

import pandas as pd
import random

import base64
import matplotlib
# from PIL import Image
# from urllib.request import urlopen


def pull_reddit_data():
    data = []
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
    sh = gc.open("filtered_data")
    for wk in sh:
        wh_data = wk.get_all_records()
        data.append(wh_data)
    return data[0]

def determine_sample_size(raw_data_size):
    #  fidence level of 95%
    p = 0.05 
    z_score = 1.96	
    std = .5
    margin_of_error = .05
    sample_size = (pow(1.96, 2) * std * (1-std))/(pow(margin_of_error,2))
    return round(sample_size)

# def get_data():
#     data = []
#     reddit_data = pull_reddit_data()
#     for sheet in reddit_data:
#         for entries in sheet:
#             data.append(entries)

#     sample_size = determine_sample_size(len(data))
#     random_sample_size = random.sample(data, sample_size)
#     return random_sample_size

def push_to_svg_sheet(df):
    data = pd.DataFrame(df)
    print(data.shape)
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
    sh = gc.open("filtered_data")
    worksheet = sh.add_worksheet(title="analyzed_filter_data", rows="500", cols="15")
    set_with_dataframe(worksheet, data)

svg_data = []

script = """
 -- Arguments:
 -- * url - URL to render;
 -- * css - CSS selector to render;
 -- * pad - screenshot padding size.

 -- this function adds padding around region
 function pad(r, pad)
 return {r[1]-pad, r[2]-pad, r[3]+pad, r[4]+pad}
 end

-- main script
function main(splash)

-- this function returns element bounding box
local get_bbox = splash:jsfunc([[
function(css) {
  var el = document.querySelector(css);
  var r = el.getBoundingClientRect();
  return [r.left, r.top, r.right, r.bottom];
}
]])

assert(splash:go(splash.args.url))
assert(splash:wait(0.5))

-- don't crop image by a viewport
splash:set_viewport_full()

local region = pad(get_bbox(splash.args.css), splash.args.pad)
return splash:png{region=region}
end
"""


# Terminal command: "scrapy crawl url"

class Url(scrapy.Spider):
    name = 'url'        
    def start_requests(self):
        http_user = 'user'
        http_pass = 'userpass'
        data = pull_reddit_data()

        splash_args = {
            'lua_source': script,
            'pad': 32,
            'css': 'body'
        }

        # for entry in data:
            # url = entry['Post URL']
        url = "https://www.cnn.com/interactive/2019/business/us-minimum-wage-by-year/index.html"
        # request = SplashRequest(url=url, args=splash_args, callback=self.parse, meta={'entry_item':entry}, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'},  splash_headers={'Authorization': basic_auth_header('user', 'userpass')})
        request = SplashRequest(url=url, args=splash_args,endpoint='execute', callback=self.parse, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'},  splash_headers={'Authorization': basic_auth_header('user', 'userpass')})
        yield request

        
    def parse(self, response):
        # "class": "g_svelte" is specifically for the NYTimes 
        custom_strainer = SoupStrainer(["svg","g", {"class": "g_svelte"}])
        entry = response.meta.get('entry_item')
        key_words = ['chart', 'charts', 'interactive', 'interatives', 'viz', 'visualization','visualizations', ' graph ', 'graphs']
        # if any(key in response.text for key in key_words):
            # page_soup = BeautifulSoup(response.body, parse_only=custom_strainer)
            # page_soup_str = (str(page_soup))[0:50000]
 
        # image_data = base64.b64decode(response.body)

        with open("image.png", "wb") as img:
            img.write(response.body)

        # filename = 'output/some_image.png'
        # with open(filename, 'wb') as f:
        #     f.write(image_data)

            # if(page_soup_str):
            #     print("Successfully found at", response.url)
            #     d = {"Raw":page_soup_str}
            #     entry.update(d)
            #     svg_data.append(entry)
            #     yield {
            #         "url": response.url, 
            #     }

    # def closed(self, reason):
    #     print("FINISHED", svg_data)
    #     push_to_svg_sheet(svg_data)





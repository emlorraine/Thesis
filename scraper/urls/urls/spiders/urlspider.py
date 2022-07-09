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


def push_to_svg_sheet(df):
    data = pd.DataFrame(df)
    print(data.shape)
    credentials = {
        # TODO: https://docs.gspread.org/en/latest/oauth2.html#for-end-users-using-oauth-client-id
    } 
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open("filtered_data")
    worksheet = sh.add_worksheet(title="march_analyzed_filter_data", rows="500", cols="15")
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
        key_words = ['chart', 'charts', 'interactive', 'interatives', 'viz', 'visualization','visualizations', ' graph ', 'graphs']
        month_data = pull_reddit_data()
        for day in month_data:
            for row in day:
                url = row["Post URL"]
                if any(key in url for key in key_words):
                    request = SplashRequest(url=url, args=splash_args, callback=self.parse, meta={'entry_item':row}, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'},  splash_headers={'Authorization': basic_auth_header('user', 'userpass')})
                    request = SplashRequest(url=url, args=splash_args,endpoint='execute', meta={'entry_item':row,'url':url}, callback=self.parse, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'},  splash_headers={'Authorization': basic_auth_header('user', 'userpass')})
                    yield request

    def parse(self, response):
        # "class": "g_svelte" is specifically for the NYTimes 
        custom_strainer = SoupStrainer(["svg","g", {"class": "g_svelte"}])
        entry = response.meta.get('entry_item')
        url = response.meta.get('url')
        filename = "./output/"+entry['ID'] + ".png"
        # if any(key in url for key in key_words):
        if(response.body):
            with open(filename, "wb") as img:
                img.write(response.body)
                print("Successfully screenshotted", response.body)

    def closed(self, reason):
        print("FINISHED", svg_data)
        push_to_svg_sheet(svg_data)





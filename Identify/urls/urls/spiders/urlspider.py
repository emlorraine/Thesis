import scrapy 
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# Terminal command: "scrapy crawl url"

from retrieve import pull_reddit_data, pull_facebook_data, pull_twitter_data

def get_data():
    data = []
    reddit_data = pull_reddit_data()
    for sheet in reddit_data:
        for entries in sheet:
            data.append(entries)
    return data


svg_data = []
class Url(scrapy.Spider):
    name = 'url'

    def start_requests(self):
        http_user = 'user'
        http_pass = 'userpass'

        data = get_data()

        for entry in data:
            url = entry['Post URL']
            request = SplashRequest(url=url, callback=self.parse, meta={'entry_item':entry}, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'},  splash_headers={'Authorization': basic_auth_header('user', 'userpass')})
            yield request

    def parse(self, response):
        custom_strainer = SoupStrainer(["svg","g"])
        # html = response.body
        entry = response.meta.get('entry_item')
        key_words = ['chart', 'charts', 'interactive', 'interatives', 'viz', 'visualization','visualizations', 'graph', 'graphs']
        if any(key in response.text for key in key_words):
            page_soup = BeautifulSoup(response.body, parse_only=custom_strainer)
            if(page_soup):
                d = {"Raw":page_soup}
                entry.update(d)
                print("NEW ENTRY", entry)
                # svg_data.append(entry)
                yield {
                    "url": response.url, 
                    # "content": response.body,
                }



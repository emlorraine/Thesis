import scrapy 
from scrapy_splash import SplashRequest

from bs4 import BeautifulSoup
from bs4 import SoupStrainer


class Url(scrapy.Spider):
    name = 'url'
    def start_requests(self):
        url = "https://www.cnn.com/interactive/2019/business/us-minimum-wage-by-year/index.html"
        yield SplashRequest(url=url, callback=self.parse)
    def parse(self, response):
        custom_strainer = SoupStrainer(["svg","g"])
        page_soup = BeautifulSoup(response.text, 'html.parser', parse_only=custom_strainer)
        # soup = BeautifulSoup(response.text, 'lxml')
        print(page_soup)
        # html = response.body
        # yield {
        #     "url": response.url
        # }

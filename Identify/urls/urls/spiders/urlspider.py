import scrapy 
from scrapy_splash import SplashRequest


class Url(scrapy.Spider):
    name = 'url'
    def start_requests(self):
        url = "https://www.cnn.com/interactive/2019/business/us-minimum-wage-by-year/index.html"
        yield SplashRequest(url=url, callback=self.parse)
    def parse(self, response):
        html = response.body
        for prop in html:
            yield {
                'html':prop
            }
        return html
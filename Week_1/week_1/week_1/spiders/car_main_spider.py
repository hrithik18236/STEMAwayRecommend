import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import json
import os

START_PAGE = 1
MAX_PAGES = 1000

class CarMainSpider(scrapy.Spider):
    name = "car-main-spider"
    base_url = 'https://community.cartalk.com/latest.json?no_definitions=true&page={}'
    curr_page = START_PAGE
    max_pages = MAX_PAGES
    start_urls = [
        base_url.format(curr_page),
    ]
    download_delay = 2.5

    def parse(self, response):
        for quote in response.xpath("//tbody"):
            yield {'ID' : quote.xpath(".//tr[@id]").extract_first(), 
                    ''
                    }

        # next_content = response.xpath("//li[@class='next']/a/@href").extract_first()
        # if next_content != None:
        #     next_link = response.urljoin(next_content)
        #     yield scrapy.Request(url = next_link, callback = self.parse)
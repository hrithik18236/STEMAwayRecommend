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

    # Standard parsing function
    def parse(self, response):
        data = json.loads(response.body)
        for topic in data['topic_list']['topics']:
            yield { 
                'topic_id'       : topic.get('id'),
                'title'          : topic.get('title'),
                'created_at'     : topic.get('created_at'),
                'last_posted_at' : topic.get('last_posted_at'),
                'views'          : topic.get('views'),
                'like_count'     : topic.get('like_count'),
                'category_id'    : topic.get('category_id'),
                'total_replies'  : topic.get('reply_count'),
                'total_posts'    : topic.get('posts_count'),
                'topic_slug'     : topic.get('slug'),
                'tags'           : topic.get('tags'),
            }

        # Move onto the next request
        if data['topic_list']['more_topics_url'] and self.curr_page < self.max_pages:
            self.curr_page += 1
            yield scrapy.Request(self.base_url.format(self.curr_page))
import pandas as pd
import scrapy
import json

START_PAGE = 1
MAX_PAGES = 50

class CarTalkPostSpider(scrapy.Spider):
    name='car-post-spider'
    base_url = 'https://community.cartalk.com/latest.json?no_definitions=true&page={}'
    post_url = 'https://community.cartalk.com/t/{}/posts.json'
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
            curr_url = self.post_url.format(topic.get('id'))
            yield scrapy.Request(curr_url, callback=self.parse_post)
            
        if data['topic_list']['more_topics_url'] and self.curr_page < self.max_pages:
            self.curr_page += 1
            yield scrapy.Request(self.base_url.format(self.curr_page))

    # Parsing a particular post from the JSON
    def parse_post(self, response):
        data = json.loads(response.body)    
        for post in data['post_stream']['posts']:
            yield {
                'post_id'           : post.get('id'),
                'username'          : post.get('username'),
                'created_at'        : post.get('created_at'),
                'cooked'            : post.get('cooked'),
                'post_num'          : post.get('post_number'),
                'updated_at'        : post.get('updated_at'),
                'reply_count'       : post.get('reply_count'),
                'reply_to_post_num' : post.get('reply_to_post_number'),
                'reads'             : post.get('reads'),
                'topic_id'          : post.get('topic_id'),
                'user_id'           : post.get('user_id'),
                'topic_slug'        : post.get('topic_slug'),
             }
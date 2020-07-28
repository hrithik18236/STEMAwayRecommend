import scrapy

class CarSpider(scrapy.Spider):
    name = "CarSpider"
    start_urls = ['https://community.cartalk.com/']

    def start_requests(self):
        urls = [
            'https://community.cartalk.com/'
        ]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {'quote' : quote.xpath(".//span[@class='text']").extract_first()}

        next_content = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_content != None:
            next_link = response.urljoin(next_content)
            yield scrapy.Request(url = next_link, callback = self.parse)
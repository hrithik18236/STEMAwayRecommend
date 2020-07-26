import scrapy
# from first_scrapy.items import FirstScrapyItem
# from scrapy.loader import ItemLoader

class firstSpider(scrapy.Spider):
	name = 'first'

	start_urls = ['http://quotes.toscrape.com/']

	def parse(self, response):
		for quote in response.xpath("//div[@class='quote']"):
			yield {'quote' : quote.xpath(".//span[@class='text']").extract_first()}

		next_content = response.xpath("//li[@class='next']/a/@href").extract_first()
		if next_content != None:
			next_link = response.urljoin(next_content)
			yield scrapy.Request(url = next_link, callback = self.parse)
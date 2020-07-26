import requests
from bs4 import BeautifulSoup
from collections import defaultdict

tags = defaultdict(int)
base = "https://quotes.toscrape.com/"

frontier = ['page/1', 'page/2', 'page/3', 'page/4', 'page/5', 'page/6', 'page/7', 'page/8', 'page/9', 'page/10']

for page in frontier:
	response = requests.get(base + page)
	soup = BeautifulSoup(response.content, 'html.parser')
	for link in soup.find_all('a', {'class': 'tag'}):
		tags[link.text] += 1

for k, v in sorted(tags.items(), key = lambda item: item[1], reverse = True):
	print(k, ':', v)
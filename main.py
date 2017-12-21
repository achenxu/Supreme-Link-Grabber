import requests
import re
import webbrowser
from time import localtime, strftime, sleep, time

def find_between(soup, first, last):
	try:
	    start = soup.index( first ) + len( first )
	    end = soup.index( last, start )
	    return soup[start:end]
	except ValueError:
	    return ''

print '\nSupreme Bot by @DefNotAvg\n'

import requests
from bs4 import BeautifulSoup
import re
import webbrowser
from time import localtime, strftime, sleep, time

def find_between(soup, first, last):
	try:
	    start = soup.index( first ) + len( first )
	    end = soup.index( last, start )
	    return soup[start:end]
	except ValueError:
	    return ''

print '\nSupreme Bot by @DefNotAvg\n'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}

categories = ['jackets', 'shirts', 'tops/sweaters', 'sweatshirts', 'pants', 'hats', 'bags', 'accessories', 'shoes', 'skate']
choices = list(range(1,len(categories) + 1))

print 'Choose a category by entering the corresponding number\n'
for choice in choices:
	print '({}) {}'.format(choice, categories[choice - 1].title())

category = categories[int(raw_input('\nChoice: ')) - 1]
if category == 'tops/sweaters':
	category = category.replace('/', '_')
	category_link = 'http://www.supremenewyork.com/shop/all/{}'.format(category)
else:
	category_link = 'http://www.supremenewyork.com/shop/all/{}'.format(category)
print ''
new = raw_input('New Items Only? (y/n): ').lower()
keywords = raw_input('Keyword(s): ').split(',')
keywords = [x.replace(' ', '').lower() for x in keywords]
browser = raw_input('Open Link(s) in Browser? (y/n): ').lower()
print ''

matching_titles = []

response = requests.get(category_link, headers=headers)
separator = find_between(response.content, '</a><h1>', '/shop')

if new == 'y':
	initial_links = re.findall(separator + r'(.*?)"', response.content)
	initial_links = ['http://www.supremenewyork.com{}'.format(s) for s in initial_links]
	initial_links = initial_links[::2]
	initial_titles = [find_between(requests.get(initial_link).content, '<title>', '</title>') for initial_link in initial_links]
else:
	initial_links = []
	initial_titles = []

while matching_titles == []:
	response = requests.get(category_link, headers=headers)
	links = re.findall(separator + r'(.*?)"', response.content)
	links = ['http://www.supremenewyork.com{}'.format(s) for s in links]
	links = links[::2]
	links = [s for s in links if s not in initial_links]
	titles = [find_between(requests.get(link).content, '<title>', '</title>') for link in links]
	titles = [s for s in titles if s not in initial_titles]
	for title in titles:
		if all(keyword in title.lower() for keyword in keywords):
			matching_titles.append(title)
	if matching_titles != []:
		matching_links = [links[titles.index(s)] for s in matching_titles]
		print 'Item(s) matching keywords found...\n'
		for i in range(0,len(matching_titles)):
			if i != len(matching_titles) - 1:
				print '{}\n{}\n'.format(matching_titles[i], matching_links[i])
			else:
				print '{}\n{}'.format(matching_titles[i], matching_links[i])
			if browser == 'y':
				print 'Opening link in browser...'
				webbrowser.open(matching_links[i])
	else:
		print 'No items matching keywords found. [{}]'.format(str(strftime('%m-%d-%Y %I:%M:%S %p', localtime())))
	sleep(1)
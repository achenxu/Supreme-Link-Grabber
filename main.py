import requests
import re
import webbrowser
from time import localtime, strftime, sleep, time

DELAY = 1 # Delay in seconds between each "refresh" of the category page

def find_between(soup, first, last):
	try:
	    start = soup.index( first ) + len( first )
	    end = soup.index( last, start )
	    return soup[start:end]
	except ValueError:
	    return ''

def config():
	print '\nSupreme Link Grabber by @DefNotAvg\n'

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
	keywords = [keyword.replace(' ', '').lower() for keyword in keywords]
	browser = raw_input('Open Link(s) in Browser? (y/n): ').lower()
	print ''

	main(headers, category_link, new, keywords, browser)

def main(headers, category_link, new, keywords, browser):
	matching_titles = []

	if new == 'y':
		response = requests.get(category_link, headers=headers)
		initial_links = re.findall(r'href="(.*?)"', response.content)
		initial_links = ['http://www.supremenewyork.com{}'.format(initial_link) for initial_link in initial_links if initial_link.count('/') == 4 and '//' not in initial_link]
		initial_links = list(set(initial_links))
	else:
		initial_links = []

	while matching_titles == []:
		response = requests.get(category_link, headers=headers)
		links = re.findall(r'href="(.*?)"', response.content)
		links = ['http://www.supremenewyork.com{}'.format(link) for link in links if link.count('/') == 4 and '//' not in link and link not in initial_links]
		links = list(set(links))
		titles = [find_between(requests.get(link).content, '<title>', '</title>') for link in links]
		for title in titles:
			if all(keyword in title.lower() for keyword in keywords):
				matching_titles.append(title)
		if matching_titles != []:
			matching_links = [links[titles.index(matching_title)] for matching_title in matching_titles]
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
		initial_links = initial_links + links
		sleep(DELAY)

while True:
	config()
	raw_input('\nHit enter to run again')
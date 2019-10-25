import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

page = requests.get('http://jon.luini.com/thelist/date.html')
soup = BeautifulSoup(page.text, 'html.parser')


shows = {}
for month in soup.find_all('table'):
	headers = month.find_all('th')
	if len(headers) == 0:
		# First couple <TABLE> tags on the page aren't show listings
		continue
	month_name = headers[0].get_text()
	# print "month: %s" % month_name
	day_num = None
	for day in month.find_all('tr'):
		cells = day.find_all('td')
		bands = []
		if len(cells) == 0:
			# This is the TH row, we already have the month name
			continue
		if len(cells) == 4:
			# This is a row with the date number
			day_text = cells[0].get_text().strip()
			day_num = day_text[3:]
			cells.pop(0)

		day_str = '%02d %s' % (int(day_num), month_name)
		t = datetime.strptime(day_str, '%d %B %Y')
		# print "%s" % repr(t)
		if not shows.has_key(t):
			shows[t] = []
		# Now this is a row with only a show listing
		shows[t].append({
			'bands': filter(None, cells[0].get_text().split('\n')),
			'venue': cells[1].get_text(),
			'notes': cells[2].get_text()
			})
		# print "%s\t%s" % (t.ctime(), repr(shows[t]))

num_days = len(shows.keys())
num_shows = len([item for sublist in shows.values() for item in sublist])

print "%d days comprising %d shows" % (num_days, num_shows)

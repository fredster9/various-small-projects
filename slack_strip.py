'''
This takes Slack history copied into text file and writes to a spreadsheet with the title of the URL in the next row
Written to pull all the YouTube links that had been posted over time in a group chat and organize them into one doc
'''

import os, re, urllib2, csv
from urllib2 import Request, URLError
from bs4 import BeautifulSoup

f = open('slack_export.txt', 'r')

hist = f.read()

urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', hist)

print len(urls)

songs = {}

for url in urls:
	
	try: 
		request = urllib2.urlopen(url)

	except URLError as e:
		print e.reason

	else:

		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
	
		html = request.read()
		
		soup = BeautifulSoup(html)
		title = soup.html.head.title.contents
		print title
		
	songs[url] = title

print "SONG LIST", songs

writer = csv.writer(open('song_list.csv', 'wb'))
for k,v in songs.items():
	writer.writerow([k,v])






from bs4 import BeautifulSoup
import requests
import re
import urllib2
import sys

def get_data(link):
	headers = {"Accept-Language": "en-US"}
	typ = 'success'
	try:
		page = requests.get(link, headers=headers)
	except Exception as e:
		title = 'Error fetching url'
		desc = 'No Description'
		typ = 'error'
		return title, desc, typ
	html = page.content
	soup = BeautifulSoup(html)
	title = soup.title.string.encode('utf-8','ignore')
	desc = soup.findAll(attrs={"name":"description"}) 
	if desc is not None and len(desc)>0:
		desc =  desc[0]['content'].encode('utf-8')
	else:
		desc = 'No Description found.'
	return title, desc, typ

if __name__=='__main__':
	title, desc, typ = get_data(sys.argv[1])
	print(title)
	print(desc)
	print(typ)
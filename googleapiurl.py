'''
	Used to fetch seeding data from google api
'''
import urllib
import urllib2
import sys
import json
import re
from HTMLParser import HTMLParser
from urlparse import *

def api_url_calculator(search_query):
	try:
		ini_url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&" + search_query
		print 'Your Query', ini_url
		opener = urllib.FancyURLopener({})
		page_response = opener.open(ini_url)

	except Exception:
		print "Sorry could not connect to Google servers"
		sys.exit(0)

	json_data = page_response.read()
	#print json_data
	raw_data = json.loads(json_data)
	#print raw_data
	top_results = raw_data['responseData']['results']
	#print top_results[0]['url']
	api_url_list = {}
	count = 0
	for temp_list in top_results:
		api_url_list[count] = temp_list['url']
		#print temp_list['url']
		count = count + 1		
	return api_url_list

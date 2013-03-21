#the spyder

#import statements
import urllib
import urllib2
import sys
import json
import re
from HTMLParser import HTMLParser
from urlparse import *

#import modules
import googleapiurl
import URLFetcher
import URLProvider
import SiteHandler
import AttributeExtraction
import utils
import pagestoragehandler
import infologger

count=0
mime_whitelist=['text/cmd','text/cmd','text/csv','text/html','text/plain','text/vcard','text/xml']
protocol_whitelist=['http','https','ftp', 'file','news']
search_max_depth =1
#functions
def initial_seeding(url_list):
	count = 0
	for url in url_list:
		URLProvider.add_URL(url_list[count])
		count += 1

def valid_protocol_request(url):
	return (protocol_whitelist.__contains__(url))

def valid_mime_type(mymime):
	global mime_whitelist
	for valid_mime in mime_whitelist:
		if valid_mime in mymime:
			return True
	return False

def initiate():
	global count,  search_max_depth
	while(URLProvider.isIncomplete()):
		curr_url = URLProvider.get_URL()
		if(int(curr_url[1]) <= int(search_max_depth) ):
			#Print can be removed
			print curr_url, count
			my_tuple=('00000',{'customError':'NO ACCESS'},None,None,0,0)
			if(SiteHandler.is_Valid(curr_url[0])):
					#Process further
					response_data=URLFetcher.getURL(curr_url[0])
					if(response_data==1):
						my_tuple=('2222',{'customError':'Unable to Fetch Correctly'}, None, None,0, curr_url[1])
					else:
						myMime =response_data.headers.get('Content-Type')
						if(valid_mime_type(myMime)):
							base_url=utils.getBaseUrl(curr_url[0])
							mystring = response_data.read()
							links = AttributeExtraction.extract_Links(base_url,mystring)
							stored_tup = pagestoragehandler.write_log(curr_url[0],mystring)
							my_tuple = (response_data.code, response_data.headers, stored_tup, len(links), len(mystring),curr_url[1])
							#links or None
							for link in set(links):
								if(valid_protocol_request(urlsplit(link)[0])):
									if(infologger.not_in_list(link)):
										URLProvider.add_URL(link)
						else:
							#We need to keep a log of Data-Stored. If a log of data downloaded is required
							#We can put the response object's data to find its size. 
							#Ideally headers do provide the size in headers, but we found some cases
							#it was not provided. So implemented it in this fashion.
							my_tuple=('1111',{'customError':'Unsupported Mime'}, None, None,0, curr_url[1])
						
			infologger.write_summary(curr_url[0], my_tuple )
			count += 1
						
	# Force writes and commits
	pagestoragehandler.store_log()
	infologger.store_log()
	


def main():
	global count,search_max_depth
	print "Welcome \n"
	search_keys =raw_input("Enter the initial search query: ")
	search_max_depth = raw_input("Enter the depth of search (default:10): ")
	print search_keys
	search_query = urllib.urlencode({'q': search_keys})
	print search_query
	test_url_list = googleapiurl.api_url_calculator(search_query)
	initial_seeding(test_url_list)
	infologger.log_start_time()
	initiate()
	print 'Done '
	print count
	

if __name__ == "__main__":
	main()

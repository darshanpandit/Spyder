#This module accepts the data to be stored into system 
#and stores them in a compressed format for every 100 records.s  

#import statements
import urllib
import urllib2
import sys
import json
import re
from HTMLParser import HTMLParser
from urlparse import *
import zlib

#global variables
record_count = 0
file_count = 0
record_buffer = []


def write_log(url,page_response):
	'''
		Used to write the data into the system. Calls store_log for every 100 records.
		Returns file_count and record_number
	'''
	global record_count
	global record_buffer
	new_rec = page_response
	record_buffer.append(new_rec)
	if record_count == 100:
		record_count = 0
		store_log()
	record_count = record_count + 1
	#print "write"
	return (file_count,record_count)


def store_log():
	'''
	Flushes the records into a file. Handles the multiple files
	'''
	global file_count
	global record_buffer
	compressed_record_buffer = zlib.compress(str(record_buffer), 9)
	fp = open( 'data'+str(file_count) + '.dat', "ab+")
	fp.write(compressed_record_buffer)
	fp.close();
	#print "store"
	record_buffer = []
	file_count = file_count + 1



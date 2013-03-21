'''
	Used to record the map in the end.
	Generates the details of the file. 
	URLRequest time, size, etc for individual data are available here.
'''
import urllib
import urllib2
import sys
import json
import re
from HTMLParser import HTMLParser
from urlparse import *
from time import time


total_data_size=0
total_page_count=0
error_dictionary = {}
start_time=0

#global variables
summ_rec = {}
buff_count = 0

def log_start_time():
	global start_time
	start_time = time()
	

def not_in_list(url):
	global summ_rec
	if summ_rec.has_key(url):
		return False
	else:
		return True

def write_summary(url, infoTuple):
	global buff_count
	global summ_rec
	if not_in_list(url):
		summ_rec[url] = infoTuple
		buff_count += 1

def store_log():
	global summ_rec, buff_count, total_data_size, total_page_count, error_dictionary
	global start_time
		
	fp = open("log.txt", "w+")
	for url in summ_rec:
		my_tuple= summ_rec[url]
		fp.write(url+'\t')
		
		#writing response code
		fp.write(str(my_tuple[0])+'\t')
		if(error_dictionary.has_key(my_tuple[0])):
			error_dictionary[my_tuple[0]]= (error_dictionary[my_tuple[0]]+1)
		else:
			error_dictionary[my_tuple[0]]= 1
		
		#writing file size
		fp.write(str(my_tuple[4]) +'\t')
		total_data_size+=my_tuple[4]
		
		
		#writing file location properties
		file_write_details = my_tuple[2]
		if(file_write_details!=None):
			fp.write(str(file_write_details[0])+'\t'+str(file_write_details[1])+'\t')
		
		headers = my_tuple[1]
		if(headers.get('HTTPMessage')!=None):
			fp.write(headers.get('HTTPMessage')+'\t')
		else:
			fp.write('None \t')
		if(headers.get('Content-Type')!=None):
			fp.write(headers.get('Content-Type')+'\t')
		else:
			fp.write('None \t')
		if(headers.get('Server')!=None):
			fp.write(headers.get('Server')+'\t')
		else:
			fp.write('None \t')
		
		#writing total links present in the document
		if(my_tuple[3]!=None):
			fp.write(str(my_tuple[3]))
		
		fp.write('\n')
	fp.close();
	statwriter = open("statistics.txt",'w+')
	statwriter.write('Total Files Crawled and Saved	:	'+str(summ_rec.__len__())+'\n')
	statwriter.write('Total Size of Data Stored	:	'+ str(total_data_size)+' bytes\n')
	statwriter.write('The total data downloaded is greater, as responses are filtered by MimeTypes and even empty responses are actual transimissions'+'\n')
	statwriter.write('Total Time taken to execute	:	'+str((time()-start_time))+' seconds'+'\n')
	statwriter.write('The Error counts for URLs	( 0000,1111 are special application generated errors.):	'+'\n')
	statwriter.write(str(error_dictionary))
	statwriter.close()
	
	buff_count = 0


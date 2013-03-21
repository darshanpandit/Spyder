'''
Fetches a given url
'''
import urllib
from formatter import NullFormatter
    
def getURL(Url, Crawl_Post_Data={}):
    '''
        Gets the requested URL
    '''
    opener = MyOpener()
    try:
        page_response = opener.open(Url)
        return page_response
    except IOError:
        return 1
    except Exception:
        return 1

class MyOpener(urllib.FancyURLopener):
    version='PolyCrawler'
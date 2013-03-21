'''
Used to consult Robots.txt for a site
Maintains a cache using base-urls as key.
Cache flushed when filled. Robots.txt updated if it expires
'''

import RobotExclusionParser
import utils
from urlparse import urljoin

cache = {}
cache_MAX_SIZE = 500
agent = 'PolyCrawler'#'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

def __init__(self):
    pass
    
def add_To_Cache(baseURL):
    global cache,cache_MAX_SIZE, agent
    if(cache.__len__() >= cache_MAX_SIZE):
        cache.clear()
    temp=RobotExclusionParser.RobotExclusionRulesParser()
    temp.fetch(urljoin(baseURL,'robots.txt'))
    cache[baseURL] = temp


def keep_Fresh(baseURL):
    global cache,cache_MAX_SIZE, agent
    rerp = cache.get(baseURL)
    if(rerp.is_expired):
        cache.pop(baseURL)
        temp=RobotExclusionParser.RobotExclusionRulesParser()
        temp.fetch(urljoin(baseURL,'robots.txt'))
        cache[baseURL]= temp
    
    
           
def is_Valid(url):
    global cache,cache_MAX_SIZE, agent
    try:
        baseURL=utils.getBaseUrl(url)
        if(cache.has_key(baseURL)):
            #keep_Fresh(baseURL)
            #print cache.get(baseURL).is_allowed(agent, url)
            return cache.get(baseURL).is_allowed(agent, url)
        else:
            add_To_Cache(baseURL)
            return cache.get(baseURL).is_allowed(agent, url)
    except Exception:
        return False    
 
def get_Crawl_Delay(url):
    global cache,cache_MAX_SIZE, agent
    baseURL=utils.getBaseUrl(url)
    cache=cache
    if(cache.has_key(baseURL)):
        rerp = cache.get(baseURL)
        if(rerp.get_crawl_delay(agent)!=None):
            return rerp.get_crawl_delay(agent)
        else:
            return 0
    else:
        add_To_Cache(baseURL)
        return get_Crawl_Delay(url)
          
                


'''
Util methods.
More methods to be added as required
'''
from urlparse import *


def getBaseUrl(url):
    parsed_url=urlparse(url)
    domain_url = '{}://{}/'.format( parsed_url[ 0 ], parsed_url[ 1 ] )
    return domain_url


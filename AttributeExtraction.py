'''
We are extracting information from hyperlinks, area tags, frames, iframes.
We are also using <base> tag to get additional relative url functionality
We are using <meta> tags to indicate if the page has to be accessed as well.

For HyperLinks,     rel attribute holds the following meanings:
alternate          Links to an alternate version of the document (i.e. print page, translated or mirror)
author             Links to the author of the document
bookmark           Permanent URL used for bookmarking
help               Links to a help document
license            Links to copyright information for the document
next               The next document in a selection
nofollow           Links to an unendorsed document, like a paid link. HERE WE ARE IGNORING THEM. LINKS IN COMMENTS ARE MANY TIME nofollow LINKS
                    ("nofollow" is used by Google, to specify that the Google search spider should not follow that link)
noreferrer         Specifies that the browser should not send a HTTP referer header if the user follows the hyperlink
prefetch           Specifies that the target document should be cached
prev               The previous document in a selection
search             Links to a search tool for the document
tag                A tag (keyword) for the current document
stylesheet         Stylesheet

FOR META TAGS
noindex        Do not show this page in search results and do not show a "Cached" link in search results.
nofollow       Do not follow the links on this page
none           Equivalent to noindex, nofollow
'''


import urllib, htmllib, formatter
import urlparse


class LinksExtractor(htmllib.HTMLParser):
    
    
    
    def __init__(self, formatter):
        htmllib.HTMLParser.__init__(self, formatter)
        self.links = []
        self.Rel_Tag_Blacklist= ['alternate','bookmark','nofollow','stylesheet']
        self.Base_URL=None
        self.Include_Links = True
        
    
        
        
    def get_Status(self, base):
        final_links=[]
        for relUrl in self.links :
            if(self.Base_URL!=None):
                final_links.append(urlparse.urljoin(self.Base_URL,relUrl))
            else:
                final_links.append(urlparse.urljoin(base,relUrl))
            
        if(self.Include_Links):
            return final_links
        else:
            return []
                
        
    def get_links(self) :     # return the list of extracted links
        return self.links
    
    def start_a(self, attrs) :  # override handler of <A ...>...</A> tags
        # process the attributes
        mylink=''
        include = True
        
        if len(attrs) > 0 :
            for attr in attrs :
                if attr[0] == 'rel' :
                    if (self.Rel_Tag_Blacklist.__contains__(attr[1])==True)    :
                        include = False
                        
                if attr[0] == 'href' :  # ignore all non HREF attributes
                    mylink = attr[1]
#              
            if(include):
                    self.links.append(mylink)# save the link info in the list
                
    def start_area(self,attrs) :# override handler of <Area ...>...</Area> tags
        # process the attributes
        mylink=''
        include = True
        
        if len(attrs) > 0 :
            for attr in attrs :
                if attr[0] == 'rel' :
                    if (self.Rel_Tag_Blacklist.__contains__(attr[1])==True)    :
                        include = False
                        
                if attr[0] == 'href' :  # ignore all non HREF attributes
                    mylink = attr[1]
#              
            if(include):
                    self.links.append(mylink)# save the link info in the list
                    
    def start_frame(self,attrs):# override handler of <frame ...>...</frame> tags
        # process the attributes
        mylink=''
        include = True
        
        if len(attrs) > 0 :
            for attr in attrs :
                if attr[0] == 'rel' :
                    if (self.Rel_Tag_Blacklist.__contains__(attr[1])==True)    :
                        include = False
                        
                if attr[0] == 'src' :  # ignore all non HREF attributes
                    mylink = attr[1]
#              
            if(include):
                    self.links.append(mylink)# save the link info in the list
        
    def start_meta(self,attrs):# override handler of <meta robot ...>...</meta> tags
        # process the attributes
        Directive_Present=False
        
        if len(attrs) > 0 :
            for attr in attrs :
                if attr[0] == 'name' :
                    if (attr[1].lower()=='robots')    :
                        Directive_Present = True
                        
        if Directive_Present :
            if len(attrs) > 0 :
                for attr in attrs :
                    if attr[0].lower() == 'content' :
                        a=False
                        b=False
                        if 'nofollow' in attr[1].lower():
                            a=True
                            
                        if 'none' in attr[1].lower():
                            b=True
                        
                        if(a or b):
                            self.Include_Links=False
                        
    def start_base(self, attrs):# override handler of <base ...>...</base> tags 
        # process the attributes
        if len(attrs) > 0 :
            for attr in attrs :
                if attr[0] == "href" :          # ignore all non HREF attributes
                    self.Base_URL= attr[1]      # set the base url for the page
              
    def start_iframe(self,attrs):# override handler of <frame ...>...</frame> tags
        # process the attributes
        mylink=''
        include = True
        
        if len(attrs) > 0 :
            for attr in attrs :
                if attr[0] == 'rel' :
                    if (self.Rel_Tag_Blacklist.__contains__(attr[1])==True)    :
                        include = False
                        
                if attr[0] == 'src' :  # ignore all non HREF attributes
                    mylink = attr[1]
#              
            if(include):
                    self.links.append(mylink)# save the link info in the list
                    
def extract_Links(base_url,page_data):
    a=['empty']
    try:
        My_Format = formatter.NullFormatter()           # create default formatter
        htmlparser = LinksExtractor(My_Format)           # create new parser object
        htmlparser.feed(page_data)                            # parse the file saving the info about links
        links = htmlparser.get_Status(base_url)              # get the hyperlinks list
        return links   # print all the links
    except Exception:
        return a
*******************Spyder v6 - Darshan Pandit, Manas Pawar*******************
Refer to explain.txt for the flow and implementation details for this code.

*LIST OF FILES AND DESCRIPTION
1. spydermain.py - The core module which initializes other modules.
2. googleapiurl.py - The Google custom search api handling module which returns the initial URLs.
3. URLProvider - Maintains the queue of valid urls in a BFS manner.
4. URLFetcher - Requests the page for the passed URL using FancyUrlOpener.
5. SiteHandler - Retrieves and caches the robots.txt for the particular domian.
6. RobotExclusionParser (from Nikita Parser)
7. AttributeExtraction.py - Parses for all valid URL links in the page.
8. utils.py - Extracts the domain URL forn the passed URL.
9. pagestoragehandler.py - Stores and writes response page data into files.
10.infologger.py - Stores and writes the execution log of URLS in the exxecution order.



*COMPLILING  AND RUNNING PROGRAM
1. After extracting all files, run spidermain.py inside Spyder v6 folder
2. The output files will be stored in ./Output/
3. execution_log.txt contains the list of all Urls including  the return code, time of crawling, size of page.
4. statistics.txt contains statistics like number of files, total size,  total time taken, number of 404 errors
5. dataXXX.dat contains the page data retrieved from each Url per 100 Urls.



*LIMITATIONS
1. I/O error caused due to force termination of connection from the server side.
2. The crawl delays are not incorporated.
3. In the statistics file, the total size refers to the total length of all the files crawled. We assume that they would be similar.
3. Server timeout.

Baseline: Handles 99% of urls

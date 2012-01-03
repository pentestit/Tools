#!/usr/bin/env python
#
# Queries an IP address on Bing and returns all the domains associated - currently limited to 50
#
import sys
from BeautifulSoup import BeautifulSoup
import urllib2
import urlparse

# Check we've got an argument
if len(sys.argv) < 2:
	print "usage: %s <IP Address>" % sys.argv[0]
	sys.exit(1)

# Set some variables
ipaddr = sys.argv[1] # The IP address we want to query
cookie = "SRCHHPGUSR=NEWWND=0&NRSLT=50&SRCHLANG=&AS=1&ADLT=DEMOTE" # We set this so we get up to 50 results per page
domains = set() # Where we store the results

# Perform the HTTP request to Bing
url = 'http://www.bing.com/search?q=ip%3A'+ipaddr+'&go=&qs=n&sk=&sc=8-26&form=QBRE&filt=all'
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', cookie))
response = opener.open(url)
html = response.read()

# Parse it with BeautifulSoup....hmmm, beautiful
soup = BeautifulSoup(html)
divs = soup.findAll('div', attrs={'class':'sb_tlst'})

# Loop through all the divs with class="sb_tlst" and find links
for div in divs:
	url = BeautifulSoup(str(div)).find('a')['href']
	hostname = urlparse.urlparse(url).hostname
	domains.add(hostname) # add the domain to the set

# Print out our list of domains
for i in domains:
	print i

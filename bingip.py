#!/usr/bin/env python
#
# Queries an IP address on Bing and returns all the domains associated - currently limited to 50
#
import sys
from BeautifulSoup import BeautifulSoup
import urllib2
import urlparse

ipaddr = sys.argv[1]
cookie = "SRCHHPGUSR=NEWWND=0&NRSLT=50&SRCHLANG=&AS=1&ADLT=DEMOTE" # We set this so we get up to 50 results per page

url = 'http://www.bing.com/search?q=ip%3A'+ipaddr+'&go=&qs=n&sk=&sc=8-26&form=QBRE&filt=all'
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', cookie))
response = opener.open(url)
html = response.read()

soup = BeautifulSoup(html)
divs = soup.findAll('div', attrs={'class':'sb_tlst'})
domains = set()

for div in divs:
	url = BeautifulSoup(str(div)).find('a')['href']
	hostname = urlparse.urlparse(url).hostname

	domains.add(hostname)

for i in domains:
	print i

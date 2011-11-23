#!/usr/bin/env python

import os
import sys
import argparse
import urllib2
import cookielib

# Now parse the command line arguments
parser = argparse.ArgumentParser(description='Command line web page fetcher', epilog="Set http_proxy to http://<proxy>:<port> to use a proxy")
parser.add_argument('--target', '-t', action="store", dest="url", help='The target url to scrape', required=True)
parser.add_argument('--headers', '-x', action='store_true', dest="headers", help='Print the HTTP headers')
parser.add_argument('--cookies', '-c', action='store_true', dest="cookies", help='Display received cookies')
parser.add_argument('--user-agent', '-u', action='store', dest="useragent", help='Send this User Agent')
args = parser.parse_args()

# Set some values
url = args.url
headers = args.headers
cookies = args.cookies
txdata = None
if args.useragent: 
	useragent = args.useragent
else: 
	useragent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1"

txheaders = {'User-agent' : useragent }

# Set up the cookie handling
COOKIEFILE = '/tmp/cookies.lwp'
cj = None
urlopen = urllib2.urlopen
Request = urllib2.Request
cj = cookielib.LWPCookieJar()

if cj is not None:
	if os.path.isfile(COOKIEFILE):
		# load any existing cookies
		cj.load(COOKIEFILE)	
	
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)
	

# We're ready to try this out
try:
	# create the request object
	req = Request(url, txdata, txheaders)
	
	# open a handle on the url
	#if args.proxy:
	#	handle = urlopen(req, proxies=proxies)
	#else:
	handle = urlopen(req)

except IOError, e:
	print 'Failed to open "%s"' % url
	sys.exit(1)

else:
	if headers:
		print handle.info()

	if cookies:
		print "Cookies received: "
		for index, cookie in enumerate(cj):
			print index, ' : ', cookie
		cj.save(COOKIEFILE)

	print handle.read()	
	handle.close()

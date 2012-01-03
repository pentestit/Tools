#!/usr/bin/env python
#
# Simple thing which should probably be written in bash
# but just returns whois data for a domain and its network
#
import sys
import argparse
import socket
import subprocess
import re

# Parse command line arguments
parser = argparse.ArgumentParser(description='Simple WHOIS fetcher')
parser.add_argument('--target','-t', action="store", dest="host", help='The host to retrieve data for', required=True)
args = parser.parse_args()

# Set some vars
host = args.host
domain = re.sub("^www\.", "", host) # Remove www if specified, we might need for IP lookup but not for WHOIS

try: 
	ipaddr = socket.gethostbyname(host) # Need to fix to use getaddinfo as this does not support IPv6
except socket.gaierror:
	print "unable to resolve address for", host
	sys.exit(1)

# Define functions
def whois(target):
	p = subprocess.Popen('whois "%s"'%target, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
	p.wait()
	return(p.stdout.read())

# Finally, retrieve WHOIS data using the OS whois command for both the domain and network
for data in domain, ipaddr:
	print "WHOIS data for", data
	print whois(data)

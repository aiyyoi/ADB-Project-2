'''
	Main business logic implementation 
	For ADB Project2 part 1
	Reads in API key, parse inputs
	Delegate to suitable classes for analysis
'''

import urllib2
import urllib
import base64
import json
import argparse
import QProberClass


#################### New Search and Classification Session #################################
parser = argparse.ArgumentParser(prog='ADB Project 2', description = 'how to use the script')
parser.add_argument('-host', help = 'URL to the database to be classified', required = True)
#queries will be read from rule files
#parser.add_argument('-q', help = 'Single quoted search query', required = True)
parser.add_argument('-spec', help = 'Specificity threshold', required = True)
parser.add_argument('-cov', help = 'Coverage threshold', required = True)
args = parser.parse_args()

site = args.host
#query = args.q
tSpecificity = args.spec
tCoverage = args.cov

#instantiate QProber
qProber = QProberClass.QProber(tSpecificity, tCoverage, site, 'key.json')
category = qProber.classify('rules/root.txt', 'Root')
print category



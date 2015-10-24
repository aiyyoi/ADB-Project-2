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

bingUrlBase = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Composite?'
bingParams = {'$top': '10', '$format': 'json'}
#save your own key as key.json under the save path as this script
with open('key.json') as key_file:
	data = json.load(key_file)
accountKey = data['accountKey']
# authentications
accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}
print headers



#################### New Search and Feedback Session #################################
parser = argparse.ArgumentParser(prog='ADB Project 2', description = 'how to use the script')
parser.add_argument('-s', help = 'URL to the site', required = True)
parser.add_argument('-q', help = 'Single quoted search query', required = True)
parser.add_argument('-spec', help = 'Specificity threshold', required = True)
parser.add_argument('-cov', help = 'Coverage threshold', required = True)
args = parser.parse_args()

site = args.s
query = args.q
tSpecificity = args.spec
tCoverage = args.cov
bingParams['Query'] = "'site:"+site+" "+query+"'"

# test search
bingUrl = bingUrlBase+urllib.urlencode(bingParams)
print bingUrl
req = urllib2.Request(bingUrl, headers = headers)
response = urllib2.urlopen(req)
content = json.loads(response.read())

print tSpecificity
print tCoverage
print content['d']['results'][0]['WebTotal']


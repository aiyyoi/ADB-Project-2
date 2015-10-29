import HashListClass
from RulesReaderClass import *
import urllib2
import urllib
import base64
import json
import time

class DocumentSummary:

	def __init__(self,classification,host):
		self.docFreqs = {}
		self.nodeList = classification.split('/')
		self.nodeList = list(reversed(self.nodeList))  
		self.host = host
                self.bingUrlBase = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Composite?'
                self.bingParams = {'$top': '4', '$format': 'json'}
                #save your own key as key.json under the save path as this script
                with open("./key.json") as key_file:
                        data = json.load(key_file)
                accountKey = data['accountKey']
                # authentications
                accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
                self.headers = {'Authorization': 'Basic ' + accountKeyEnc}










	def generateSummaries(self):
		for n in self.nodeList:
			path = "./rules/" + n + ".txt"
			queries = RulesReader(path).getRules()
		



	def search(self,query_string):
		self.bingParams['Query'] = "'site:"+self.host+" "+query_string+"'" 
	        bingUrl = self.bingUrlBase+urllib.urlencode(self.bingParams)
                #wait
                #time.sleep(1)
		print(bingUrl)
                req = urllib2.Request(bingUrl, headers = self.headers)
                response = urllib2.urlopen(req)
                content = json.loads(response.read())
		print(content)









## TEST
c = DocumentSummary("root","diabetes.org")
c.generateSummaries()
c.search()

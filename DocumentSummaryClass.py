from HashListClass import *
from RulesReaderClass import *
import urllib2
import urllib
import base64
import json
import time
import subprocess
import re

class DocumentSummary:

	def __init__(self,classification,host):
		self.fileHash = HashList()
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
			path = "./rules/" + n.lower() + ".txt"
			queries = RulesReader(path).getRules()
			for q in queries:
				res = self.search(q[1])
				docs = self.getDocumentText(res)
				
				for d in docs:
					for w in d:
						if(d in self.docFreqs.keys()):
							self.docsFreqs[w] += 1
						else:
							self.docFreqs[w] = 1
			
			f = open(n + "-" + self.host + ".txt", 'w')
			f.write(str(self.docFreqs))

								 
				
		



	def search(self,query_string):
		self.bingParams['Query'] = "'site:"+self.host+" "+query_string+"'" 
	        bingUrl = self.bingUrlBase+urllib.urlencode(self.bingParams)
                #wait
                #time.sleep(1)
		print(bingUrl)
                req = urllib2.Request(bingUrl, headers = self.headers)
                response = urllib2.urlopen(req)
                content = json.loads(response.read())['d']['results'][0]['Web']
		content = map(lambda x : str(x['Url']), content)
		return content

	
	def getDocumentText(self,url_list):
		docs = []
		for u in url_list:
			doc_dump = subprocess.check_output("lynx --dump " + u, shell=True)			
			index = doc_dump.find("\nReferences\n")
			doc_dump = doc_dump[:index].lower()
			doc_dump = re.sub(r'\[.*?\]',r'',doc_dump)

			final_text = ''			
			for i in range(0,len(doc_dump)):
				char = doc_dump[i]
				if(char.isalpha() and ord(char) < 128):
					final_text += char.lower()
				else:
					final_text += ' '
	
			if(not self.fileHash.isDuplicate(final_text)):		
				final_text = set(final_text.split())
				docs.append(list(final_text))
				
		return docs




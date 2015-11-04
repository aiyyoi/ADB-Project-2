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
		for c in classification:
			i = 0        
                        for n in c:
				if(n in self.docFreqDict.keys()):
					continue
				if( i > 2):
					path = "./rules/" + c[i-1].lower() + ".txt"
					queries = RulesReader(path).getRules()
					queries = filter(lambda x : x[0] == n.lower(),queries)
				else:
					path = "./rules/" + n.lower() + ".txt"
					queries = RulesReader(path).getRules()

				for q in queries:
					res = self.search(q[1])
					docs = self.getDocumentText(res)  
                                        docFreqs = {}
                                        for d in docs:
                                                for w in d:
                                                        if(w in docFreqs.keys()):
                                                                docsFreqs[w] += 1
                                                        else:
                                                                docFreqs[w] = 1
							p = 0
							while p < i:
								if(w in self.docFreqDict[c[p]].keys()):
									self.docFreqDict[c[p]][w] += 1
								else:
									self.docFreqDict[c[p]][w] = 1 
                                        self.docFreqDict[n] = docFreqs
                		i += 1

		for k in self.docFreqDict.keys():
				f = open(k + "-" + self.host, 'w')
				for w in self.docFreqDict[k]:
					f.write(w + "#" + self.docFreqDict[k][w])



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
			try:
				doc_dump = subprocess.check_output("lynx --dump " + u, shell=True)		
			except Exception, e:
				pass	
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




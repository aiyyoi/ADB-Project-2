'''
	Implementation of QProber mechanism
	for classifying database
	For ADB Project2 Part1
'''

import urllib2
import urllib
import base64
import json
import time
import RulesReaderClass

class QProber:
	def __init__(self, tSpec, tCov, host, keyPath):
		self.tSpec = tSpec
		self.tCov = tCov
		self.host = host
		self.bingUrlBase = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Composite?'
		self.bingParams = {'$top': '10', '$format': 'json'}
		#save your own key as key.json under the save path as this script
		with open(keyPath) as key_file:
			data = json.load(key_file)
		accountKey = data['accountKey']
		# authentications
		accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
		self.headers = {'Authorization': 'Basic ' + accountKeyEnc}


	def classify(self, rulePath, supCat):
		rootRules = RulesReaderClass.RulesReader(rulePath)
		rootSets = rootRules.getRules()
		categoryCts = {}
		for eachRule in rootSets:
			self.bingParams['Query'] = "'site:"+self.host+" "+eachRule[1]+"'"
			# Search and get counts for matched docs
			if eachRule[0] in categoryCts:
				categoryCts[eachRule[0]] += self.search()
			else:
				categoryCts[eachRule[0]] = self.search()
		#check against with predefined spec and cov
		tDocCts = 0 # total number of document counts
		for eachCat in categoryCts.keys():
			tDocCts += categoryCts[eachCat]

		for eachCat in categoryCts.keys():
			cCov = categoryCts[eachCat]
			cSpec = float(categoryCts[eachCat])/tDocCts
			print 'Database has Coverage '+str(cCov)+' with Specificity '+ str(cSpec)+ ' in Category '+eachCat
			if (cSpec >= float(self.tSpec) and cCov >= int(self.tCov)):
				if (eachCat != 'Health' and eachCat!='Computers' and eachCat!='Sports'):
					parent = rulePath[6:-4].capitalize() # extract the parent category from rule file path
					for i in range(0, len(supCat)):
						if parent in supCat[i]:
							if len(supCat[i].split('/')) == 2:
								supCat[i] = supCat[i]+'/'+eachCat
							else:
								supCat.append('Root/'+parent+'/'+eachCat)

				else:
					if len(supCat[0].split('/')) == 1:
						supCat[0] = supCat[0]+'/'+eachCat
					else:
						supCat.append('Root/'+eachCat)
					supCat = self.classify('rules/'+eachCat.lower()+'.txt', supCat)
					
		return supCat	

			

	def search(self):
		bingUrl = self.bingUrlBase+urllib.urlencode(self.bingParams)
		#wait 
		#time.sleep(1)
		req = urllib2.Request(bingUrl, headers = self.headers)
		response = urllib2.urlopen(req)
		content = json.loads(response.read())
		return int(content['d']['results'][0]['WebTotal'])


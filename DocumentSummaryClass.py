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

	def __init__(self,classification,urlDict,host):
		self.host = host
		self.urlDict = urlDict
		self.urlHash = []	
		self.docFreqDict = {}
		self.classification = map(lambda x : list(reversed(x.split("/"))),classification)	


	def generateSummaries(self):
		for c in self.classification:	
			if(len(c) > 2):
				curr_path = c[1:]
			else:
				curr_path = c
			for n in curr_path:	
				if(n in self.docFreqDict.keys()):
					continue
			
				counter = 0	
				curr_list = self.urlDict[n]
				print '\nSampling and Summary for '+n+' with '+str(len(curr_list))+ ' URL:\n'
				x = 0
				while x < len(curr_list):
					print(str(x/4+1) + "/" + str(len(curr_list)/4)) 

					if(x + 4  > len(curr_list)):	
						docs = self.getDocumentText(curr_list[x:len(curr_list)])
					else:
						docs = self.getDocumentText(curr_list[x:x+4]) 
					x += 4
                                	
					for d in docs:
						for w in d:	
							temp = self.docFreqDict.keys()
							if(w in temp):
								self.docFreqDict[w] += 1
							else:
								self.docFreqDict[w] = 1
		
				f = open(n.capitalize() + "-" + self.host + ".txt", 'w')
				for w in sorted(self.docFreqDict.keys()):
					f.write(w + "#" + str(self.docFreqDict[w]) + "\n")
				f.close()


	
	def getDocumentText(self,url_list):
		docs = []
		for u in url_list:
			if(u in self.urlHash or u.split('.')[-1] == "pdf" or u.split('.')[-1] == "ppt"):
				continue
			else:
				self.urlHash.append(u)
			try:
				print(u)
				doc_dump = subprocess.check_output("lynx --dump " + u, shell=True)		
			except Exception, e:
				pass	
			index = doc_dump.find("\nReferences\n")
			final_text = ''	
			recording = True 
			wrotespace = False#True
			
			for i in range(0,index):
				if(recording):
					if(doc_dump[i] == '['):
						recording = False
						if(not wrotespace):
							final_text += ' '
							wrotespace = True
						continue
					else:
						if(doc_dump[i].isalpha() and ord(doc_dump[i]) < 128):
							final_text += doc_dump[i].lower()
							wrotespace = False
						else:
							if(not wrotespace):
								final_text += ' '
								wrotespace = True
				else:
					if(doc_dump[i] == ']'):
						recording = True
						continue


			final_text = set(final_text.split())
			docs.append(final_text)
		
		return docs




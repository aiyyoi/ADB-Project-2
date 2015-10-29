import HashListClass
from RulesReaderClass import *

class DocumentSummary:

	def __init__(self,classification):
		self.docFreqs = {}
		self.nodeList = classification.split('/')
		self.nodeList = list(reversed(self.nodeList))	


	def generateSummaries(self):
		for n in self.nodeList:
			path = "./rules/" + n + ".txt"
			queries = RulesReader(path).getRules()	
			print(queries)	







## TEST
c = DocumentSummary("root")
c.generateSummaries()

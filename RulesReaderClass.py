'''
	Utility class for ADB project2 part1
	For reading probing rules into memory
'''


class RulesReader:
	def __init__(self, filePath):
		'''
		Read rules from filePath line by line into list of tuples
		'''
		self.rules = []
		inFile = open(filePath, 'r').readlines()
		for i in range(len(inFile)):
			sub = inFile[i].split(None, 1)
			if len(sub) == 2:
				self.rules.append((sub[0], sub[1]))
		#print 'Classification rules '+filePath+ ' in use'


	def getRules(self):
		return self.rules
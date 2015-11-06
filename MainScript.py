'''
	Main business logic implementation 
	For ADB Project2
	Reads in API key, parse inputs
	Delegate to suitable classes for analysis
'''

import argparse
import QProberClass
import DocumentSummaryClass

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
print '\n\nClassifying...'
category, urlSet = qProber.classify('rules/root.txt', ['Root'], {'Root':[]})
print '\n\nClassification Result: \n'
for each in category:
	print each

#for each in urlSet.keys():
#	print '\n' + each + ': '+str(len(urlSet[each]))


# to summarize database
c = DocumentSummaryClass.DocumentSummary(category,urlSet,site)
c.generateSummaries()



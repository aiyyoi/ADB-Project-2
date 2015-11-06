# ADB-Project-2
###COMS 6111 Advanced Database Systems Project 2: 
######Deep-Web Database Classification, Sampling and Content Summary


By:

Xuejun Wang, UNI: xw2355

Akshaan Kakar, UNI: ak3808

## Essential Information

### List of Files in Submission
<pre><code>
Xuejuns-MacBook-Pro:ADB-Project-2 AmyWang$ tree
.
├── DocumentSummaryClass.py
├── DocumentSummaryClass.pyc
├── HashListClass.py
├── HashListClass.pyc
├── MainScript.py
├── QProberClass.py
├── QProberClass.pyc
├── README.md
├── RulesReaderClass.py
├── RulesReaderClass.pyc
├── key.json
└── rules
    ├── computers.txt
    ├── health.txt
    ├── root.txt
    └── sports.txt
</code></pre>

### Compile/ Run Instructions
1. <code>key.json</code> is the file that stores Bing Search API accountKey. Make sure it is under the same file path as <code>MainScript.py</code>. The file is in following format:<pre><code>{"accountKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}</code></pre>The provided classification rules are saved in folder <code>./rules</code> under project root folder.
2. From terminal, change file path to the project root folder
3. To run:<pre><code>python MainScript.py -host fifa.com -spec 0.6 -cov 100</code></pre>
4. Database summary files will be produced in the project root folder after termination of the script in the naming convention specified in requirements.

## Internal Design
**MainScript.py** : The main script starts by parsing input arguments: URL of the database to be classified, specificity and coverage threshold value for QProber algorithm implementation, and delegates to **QProberClass** along with Bing Search API key file path and other initial parameters to kick start query probing classification process at root level. It then takes the returned categories list and list of sampling results associated with every category evaluated in the probing process, and pass onto **DocumentSummaryClass** to produce the required database summary files at different category levels. 

**QProberClass** : This class is the implementation according to [1] where the query probing and evaluation of each level of categories is a recursive process of Depth First Search. Upon instantiation of QProber instance, it takes specificity and coverage threshold, database URL, and authenticate Bing Search API. The recursive process happens in <code>classify(self, rulePath, supCat, urlSet)</code> method, where <code>rulePath</code> is the file path of parent node of categorization tree, <code>supCat</code> is the intermediate categorization results list where parent node was a child. <code>urlSet</code> is the dictionary that maintains all the URLs of sampled documents that are extracted when issuing probing queries and access Bing Search API in <code>search()</code> method. Each children of Root node is compared against specificity and coverage threshold before deciding which child node to go into as parent level, so that recuring process of probing, sampling and classification happens at leaf level categories. The <code>urlSet</code> and <code>supCat</code> would have the following data structure respectively:
<pre><code>urlSet = 
{
 Root: [url1, url2, ...], 
 Health: [url3, url4, ...], 
 Computers: [url5, url6, ...], 
 Sports: [url7, url8, ...]
 }
</code></pre>
<pre><code>
supCat = 
[
 Root/Health/Fitness
 Root/Health/Disease
 .
 .
 .
]
</code></pre>

**DocumentSummaryClass** : This class was instantiated after query probing and sampling processes are finished and category results are presented in terminal. It takes final categorization result list, and the dictionary of sampled URLs associated with each category that has been evaluated. For each category result, <code>generateSummaries()</code> method retrieves URLs associated with each node accordingly and process them. This process starts from the second level category in a bottom up fashion (as leaf level summary is not required). The word - document_counts association is then recorded in <code>docFreqDict</code> dictionary in the following format:
<pre><code>
docFreqDict = 
{
 'a': 92
 'aa': 3
 .
 .
 .
}
</code></pre>
After producing the second level summary file, the method interates to parent level (root level) for additional documents retrieving and processing, where it keeps adding document counts and new words on top of <code>docFreqDict</code> from previous iteration, such that the parent level summary includes subcategory summary. 

Duplicated of URLs are checked and skipped to avoid processing same document multiple times.

**RulesReaderClass** : This is a utility class that is used to parse classification rule file into list of tuples. It takes file path for reading, spliting each line by the first <code>Space</code> character and construct a tuple for each line. Such tuple is added to a list which would be used by **QProberClass** for query probing. The <code>rules</code> list has the following format:
<pre><code>
rules = 
[
 ("Computers", "cpu")
 ("Computers", "java")
 ("Computers", "module")
 ("Computers", "multimedia")
 ("Computer", "perl")
 ("Computers", "vb")
 ("Computers", "agp card")
 ("Computers", "application windows")
 .
 .
 .
]
</code></pre>

**HashListClass** : To be written

######Important Remark:
The query probling and sampling processes are done side by side in **QProberClass** to avoid unnecessary access to Bing Search API twice at two different steps, so as to save execution time even when caching is not implemented.



## Benchmark Test 
######Against Reference Implementation


<pre><code>Code segments</code></pre>



## Reference
1. Ipeirotis, Panagiotis, and Luis Gravano. "QProber: A system for automatic classification of hidden-web databases." (2003).

# coding: utf-8

# In[1]:

doc = open('Seattle_Reports.txt', 'rb')
text = doc.read()
head = '''CONTRACTORS QUALITY CONTROL REPORT (QCR)
DAILY LOG OF CONSTRUCTION - MILITARY'''


# In[2]:

contents = {}
fileNum_reptNum = {}
fileNum_date = {}
start = 0

import re

fileNum = 0

curPos = text.find(head, start)
for i in range(0, 2027):
    start = curPos + 1
    nextPos = text.find(head, start)
    content = text[curPos+len(head) : nextPos] #get content of reports
    curPos = nextPos
    
    #re_page = re.compile(r'Page [\d] of')
    if r'Page 1 of' in content:
        fileNum += 1
        repNum = text[text.find(r'Page 1 of', start)-7 : text.find(r'Page 1 of', start)-2].replace('\n','').replace('R','')
        fileNum_reptNum[fileNum] = repNum
        
        date = text[text.find(r'DATE', start)+4 : text.find(r'PROJECT', start)].replace('\n', '')
        fileNum_date[fileNum] = date  
        
        contents[fileNum] = content
    else:
        contents[fileNum] = contents.get(fileNum)+content
        
    #print contents[fileNum]
print len(contents), '\n', fileNum


# In[3]:

doc = open('classification.txt', 'rb')
classification2_text = doc.readlines()


# In[4]:

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()

# head of HTML file
f = open('HTML/search_keywords.html', 'w')
f.write("<html>\n")
f.write("<head> Search Keywords\n")
f.write("    <script type=\"text/javascript\" src=\"mktree.js\"></script>\n")
f.write("    <link rel=\"stylesheet\" href=\"mktree.css\" type=\"text/css\">\n")
f.write("</head>\n\n")
f.write("<body>\n")
f.write("<ul class=\"mktree\">\n")

has_subdir = False
has_record = False

#f.write("Search Keywords")

for line in classification2_text:
    line = line.strip()
    
    if re.match(r'^(\d{5})(.+)', line):
        if not has_subdir:
            has_subdir = True
            f.write("    <ul>\n")
        f.write("    <li>"+line+"\n")
        
        pattern = re.compile(r'"(.+?)"') #not greedy match
        element = pattern.findall(line)
        if len(element) > 0:
            #f.write("    <ul>\n")
            for keywords in element:
                keywords = keywords.split(' + ')  #extract keywords
                for i in range(1,881):
                    for line in contents[i].split('\n'):
                        line = line.decode('utf-8')
                        #print line
                        l = set([])
                        k = set([])
                        for w1 in line.split():
                            l.add(ps.stem(w1))
                        for w2 in keywords:
                            k.add(ps.stem(w2))
                        #if not [False for word in keywords if ps.stem(word) not in l]:
                        if k < l:
                            if not has_record:
                                has_record = True
                                f.write("\n        <ul>")
                            f.write("    <li> Report Number: "+fileNum_reptNum[i]+"\t Date: "+fileNum_date[i]+"\n    "+line.encode('utf-8')+"</li>\n")
            if has_record:
                has_record = False
                f.write("        </ul>\n")
        f.write("    </li>")
        
    elif re.match(r'[A-Z](\d{4})(.+)', line):
        if has_subdir:
            has_subdir = False
            f.write("\n</ul>")
        f.write("\n</li>")
        f.write("\n<li>"+line+"\n")
    
    else:
        f.write("\n</li>")
        f.write("\n<li>"+line+"\n")
#f.write("\n</ul></li>")
    
f.write("</ul>\n")
f.write("</body>\n")
f.write("</html>\n")
f.close()


# In[ ]:




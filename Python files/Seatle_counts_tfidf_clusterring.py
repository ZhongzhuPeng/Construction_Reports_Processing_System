
# coding: utf-8

# # 1. Extract whole textual file to daily contents

# In[1]:

doc = open('Seattle_Reports.txt', 'rb')
text = doc.read()
head = '''CONTRACTORS QUALITY CONTROL REPORT (QCR)
DAILY LOG OF CONSTRUCTION - MILITARY'''


# In[2]:

contents = {} #a dict to store the reports. key: file number; value: contents of the corresponding report
fileNum_reptNum = {} #key: file number, value: report number
fileNum_date = {} #key: file number, value: date of the report
start = 0

import re

fileNum = 0

curPos = text.find(head, start)# get the position of the start of a report
for i in range(0, 2027): #2027 pages
    start = curPos + 1
    nextPos = text.find(head, start)
    content = text[curPos+len(head) : nextPos] #get contents of reports
    curPos = nextPos
    
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


# # 2. Obtain the set of stop words

# In[3]:

ehab_stop_words = []

for word in open(r"ehabs_stop_words.txt",'r'):
    ehab_stop_words.append(word.strip())

from sklearn.feature_extraction import text 

my_stop_words = text.ENGLISH_STOP_WORDS.union(ehab_stop_words) # union the ehab's stop words and the stop words in the pachage


# # 3. Convert reports into a matrix. This step results in a matrix of 6782 words by 881 reports. 

# In[4]:

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer(stop_words=my_stop_words, analyzer='word')
X_train_counts = count_vect.fit_transform(contents.values()) # counting the words in every reports
#X_train_counts.shape 


# In[5]:

inv_dic = {v: k for k, v in count_vect.vocabulary_.iteritems()}


# # 4. Re-represent reports with a matrix with word importance. 

# In[6]:

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words=my_stop_words, analyzer='word') 
X_train_tfidf=tfidf.fit_transform(contents.values())


# In[7]:

from sklearn.cluster import KMeans
kmeans_word_tfidf = KMeans(n_clusters=10, init='random').fit(X_train_tfidf.transpose()) #clustering words


# # 5. Save the matrix of word frequency to a file words_counts_doc.csv

# In[8]:

import csv
import numpy
import re

with open('words_counts_doc.csv', 'wb') as f:
    writer = csv.writer(f)
    counts_toarray = X_train_counts.transpose().toarray()
    counter = 0
    writer.writerow(['word_number', 'word_label', 'word'])
    for word_num in range(0,6782):
        if not re.match(r'[a-z]*[\d]+[a-z]*', inv_dic[counter]): #exclude the words containing numbers
            counts_row = counts_toarray[word_num].ravel()
            writer.writerow(numpy.append([counter, kmeans_word_tfidf.labels_[counter], inv_dic[counter].encode('utf-8')], counts_row))
        counter += 1
    f.close()


# # 6. Save the matrix of TF-IDF to a file words_tfidf.csv

# In[9]:

with open('words_tfidf.csv', 'wb') as f:
    writer = csv.writer(f)
    tfidf_toarray = X_train_tfidf.transpose().toarray()
    counter = 0
    writer.writerow(['word_number', 'word_label', 'word'])
    for word_num in range(0,6782):
        if not re.match(r'[a-z]*[\d]+[a-z]*', inv_dic[counter]): #exclude the words containing numbers
            tfidf_row = tfidf_toarray[word_num].ravel()
            writer.writerow(numpy.append([counter, kmeans_word_tfidf.labels_[counter], inv_dic[counter].encode('utf-8')], tfidf_row))
        counter += 1
    f.close()


# In[27]:

#print counts_toarray[1408].ravel()


# In[29]:

#print tfidf_toarray[1408].ravel()


# In[ ]:




# In[ ]:




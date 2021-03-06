#### Code:

I do not upload the all the latest code files since my collaborators do not want to make them public. 
The available code is written in python2 in the ipynb files(which can be run by jupyter notebook).
And three python files are generated by those three ipynb files.
Might not be compatible with python 3.
Path in the programs need to be edited as the form of Windows system if they are run on Windows system.

The programs depend on pdfminer.six. Please install pdfminer.six(for py2 and py3) on your computer before running. 
website(original version of pdfminer for Python 2): https://github.com/euske/pdfminer
pdfminer.six download: https://pypi.python.org/pypi/pdfminer.six/20160614

Some links for the syntax of PDF:
Introduction to PDF: https://web.archive.org/web/20141010035745/http://gnupdf.org/Introduction_to_PDF
PDF REFERENCE: http://www.adobe.com/devnet/pdf/pdf_reference.html

Seatle_counts_tfidf_clusterring.py : Output the matrix of word frequency and the matrix of TF-IDF;
Seatle_parser.py : Output the tree structure of reports;
Seatle_work_search_keywords.py: Output the results of searching key words.

Two documents of previous documents included: "Text Mining for Daily Reports of Construction" and "Tree Structure".

**Update:** upload one more ipynb file: Information Extraction and database manipulation.ipynb

#### Results:
The results of word frequency, TF-IDF and visualization saved in CSV and XLSX flies.
The results of tree structure of reports and searching key words are saved in the HTML files in the folder HTML.


# 1.Introduction
Currently, for the traditional convention, most reports of construction are saved as PDF files. A daily report of construction usually records many things on this day, including the weather, activities, labors, and equipment. To analyze the situation of construction of a project, it is common to find the useful information from a large amount of PDF files of construction reports. However, though those reports contain very detailed information about project, it is not easy for human readers to quickly capture the key information from such large volume of data. Therefore, we develop a system of Python programs to help user to process those reports. 
The information in the reports is very detailed and fractional, and is recorded in natural language, which is relatively unstructured. In some cases, the records in daily reports are in form of tables. The information of different categories is mixed together and hard for Python program to process, which increase the difficulty of retrieving useful information. Moreover, PDF files are not user-friendly for user to explore and extract organized information. A PDF file with clean and concise outlook might have complex data structure inside. Therefore, to efficiently exploit the information from the report of construction, it is necessary to parse the contents in daily reports and store them in a well-organized data structure with user-friendly interface. 
In our project, we develop a system, which can inspect the objects containing the textual information in a PDF file’s internal structure and extract the context and its layout and font from it. With human intervention through user-friendly interface, the information extracted is reorganize into a tree structure with difference categories. The structured reorganized data obtained from previous steps can be stored in a MySQL database for further analysis.
With part of structure data obtained from the PDF files of daily reports, we analyze its temporal features by unsupervised machine learning. At first, we clean the textual data by removing the stop words and some relatively meaningless words. Then all the reports are converted to a matrix of word frequency and TF-IDF. Based on the matrices, K-means algorithm is applied to cluster both words and reports. By analyzing and visualizing the clusters of words and reports, several temporal features of the reports can be easily observed, and more information might be revealed by further research.

# 2.Background
In most construction projects, the managers or labors use daily reports to record various things happening during the day. Some of contents are just about some general information of this day, like the project name, report number, weather, temperature and so on. This part is usually written in the report’s header. Some things happen regularly, like the list of labors and equipment, so they can be organized a little bit better and are often written in tables. Meanwhile, Other things is recorded in pure narrative text, including the general description of this day and accident reporting. Therefore, a daily report usually has the information of this day, or several days in some cases, mixed together. While a construction project may span over month or years, hundreds or even thousands daily reports are generated during the projects. A sample page of daily report is shown in Figure 1.

##### Figure 1. A page of a daily report
![](https://github.com/ZhongzhuPeng/Construction_reports_processing_system_phase1/blob/master/README_IMG/1.jpg?raw=true)



In some circumstances, specific information needs to be retrieved information from the daily reports. For example, the project is delayed for some reason, and the manager need to find out what causes that. Considering the large volume and mixed structure of the daily reports, it would be a tedious and time consuming tedious job. Since the reports are in form of PDF, only some simple method like key words search can be used. Furthermore, because of unstructured information in PDF files, it is difficult to directly implement some methods of data analysis on the daily reports. Thus, it is very important for further data retrieving and analysis to reorganize the data in PDF files of daily reports.

# 3.Information Extraction from PDF files
At the first step, we need to extract the necessary information from the PDF files of construction reports. Considering the basic format of construction reports, daily reports usually only contain textual contents, including narrative records and tables. Images are rarely used in most construction reports. Thus, our program focuses on how to extract necessary textual contents without losing much useful information.
The internal structure of PDF files is very complicated, because PDF file format was originally designed for printing and presentation rather than data retrieving. General speaking, the majority of PDF file consists of a sequence of objects, which are basically organized as a tree structure, while some objects from different subtrees are related with reference. Most information, including text, font and images presented in a PDF file is stored in those objects.  Since we only focus on textual contents, only the objects containing information about text are interesting, which are called text boxes. By processing the text boxes and their references to other objects, we can extract the following information from the PDF file: text, text’s positions on pages, and text’s font name. The text contains the most straightforward information, while text’s positions and font names imply its function and importance in a construction reports.
Since the format of each daily report from the same construction project is similar, some phrases, like the title of the reports and some categories, appear repeatedly in the reports. To save the memory and storage space, we choose to use the dictionary data structure to store the information of text. An example of one item in the dictionary is show as following:
Project:
[(21.000000000000057, 734.1432, 'AAAAAA+SegoeUISemibold,Bold', 0), (21.000000000000057, 734.1432, 'AAAAAA+SegoeUISemibold,Bold', 1), …]
“Project:” is a key in this dictionary, and its corresponding value is a list. The list contains a sequence of tuples, which have the information of each appearance of the text “Project:”.  The first two items in a tuple, “21.000000000000057, 734.1432” for example, are the coordination of the text “Project:”. The third item, 'AAAAAA+SegoeUISemibold,Bold' for example, is the font name of the text. And the last item is the page number. With this data structure, all the text and its position and font information can be well organized.

##### Figure 2 is the image regenerated from the extracted data. We can find except the border lines, all the text is placed in proper position, which means our data structure does successfully store the information.

![](https://github.com/ZhongzhuPeng/Construction_reports_processing_system_phase1/blob/master/README_IMG/2.png?raw=true)
Figure 2. Image regenerated from the extracted data.
# 4.Reorganization of the extracted data
### 4.1	Tree Structure for hierarchical data
A regular construction report usually consists of two parts, the report header and the body. The report header has some general information of this day, like the date, weather, and report number. More detailed information is recorded in the body part, which includes the categories like construction activities, labors, equipment and so on. If we have a PDF file with all reports of the construction project, we can find that the categories’ titles appear in almost every report. Under the categories’ title are the detailed contents. The contents under the same categories are often similar while those under different parts are various. Thus, it is good to group the contents under the same categories together.
Category titles have some features for our Python program to identify. The categories title usually appears in each report. And in some companies’ reports, the categories’ fonts are always in bold. However, there might be many exceptions that would be mistakenly regard as a category title. So, identifying category titles with human’s help is a more reliable method. By inspecting the frequency and font name of each string in the dictionary we got in previous work, the strings with bold font and appearing in almost every report can be selected as the candidates for category titles. The program displays them in a selecting menu interface for user to select the real category titles. The interface is shown in Figure 3.
 
##### Figure 3. Categories selecting menu interface
![](https://github.com/ZhongzhuPeng/Construction_reports_processing_system_phase1/blob/master/README_IMG/3.png?raw=true)
Then, the Python program needs to know which parts are corresponding to the categories titles. It pops out another interface for user to help program to get the position information of the contents. It uses a sample report to define the relationships between the categories and its contents. For the contents in the header, the positions are usually fixed, so the program use the mode “find by position” to get content’s position. User need to select the categories and its contents. For the contents in the body part, the mode “find by area” works better. User needs to select a category and the next one categories, so the program can scan the get the contents between those two categories. The interface is shown in Figure 4.
 
##### Figure 4. Setting pairs interface
![](https://github.com/ZhongzhuPeng/Construction_reports_processing_system_phase1/blob/master/README_IMG/4.png?raw=true)

### 4.2 Table recognition
Daily reports usually contain many tables. Unlike narrative text, tables are more structured, and the contents in same row or same column should be related. It is better to treat a table as an integral entity rather than a bunch of independent fractional text.
A table in a construction reports usually has two features. The text boxes in a table are aligned in rows or columns, which means the text boxes share the same horizontal or vertical indexes, and a table header is the first row with several columns, while usually in bold font. We implement dictionaries to store a table. The keys of the dictionary are the table headers, while its values are a list of its column. The Figure 5 shows a sample that the data extracted and reorganized from a table.
     
##### Figure 5. Convert from a table (left) to data (right) 
![](https://github.com/ZhongzhuPeng/Construction_reports_processing_system_phase1/blob/master/README_IMG/51.png?raw=true)
![](https://github.com/ZhongzhuPeng/Construction_reports_processing_system_phase1/blob/master/README_IMG/52.png?raw=true)

### 4.3 Tree Structure
After finishing the previous work, we can get a tree structure to store the extracted data. The tree structure basically consists of the dictionary data structure in Python (Figure 6). With proper operation, it can transfer into the tables in MySQL database. Figure 7 shows a table in MySQL database.
 
##### Figure 6. Tree structure
 ![](https://github.com/ZhongzhuPeng/Construction_reports_processing_system_phase1/blob/master/README_IMG/6.png?raw=true)
##### Figure 7. shows a table in MySQL database.
![](https://github.com/ZhongzhuPeng/Construction_reports_processing_system_phase1/blob/master/README_IMG/7.png?raw=true)

# 5.	Data analysis
After extracting and reorganizing the information in the daily reports, it is more convenient to do data analysis with well-structured data. Based on the data we have, we did some temporal analysis and clustering on the daily report CONTRACTORS QUALITY CONTROL REPORT (QCR) DAILY LOG OF CONSTRUCTION – MILITARY.

### 5.1 Data preprocessing
Since the reports are written in natural language, punctuations and many words which are relatively meaningless, namely stop words like “the”, “is” and “that”, can be eliminated from our analysis. Considering many words have different tense and voice form in natural language, it is also necessary to convert them to the basic form. For example, the word “working”, “worked” and “worked” would be converted to “work”. Then we have a dictionary containing the remaining words. Although the numbers in daily reports play an important role for construction management, analyzing with them needs more domain knowledge of construction knowledge is required, so we eliminate the word containing number this time to simplify the problem.

### 5.2 Convert reports into a matrix of word frequency
We use every single word as a token, because if we use 2-gram the sample size would be too small. So every report can be converted to n-dimension vector, while n is the number of word in our dictionary, and the whole data can be converted into a matrix(i,j) where i represents report and j represents a word. Part of a sample matrix is shown in the Table 1.

##### Table 1: Part of the matrix of word frequency
word|	Report 1|	Report 2|	Report 3|	Report 4       
---|---|---|---|---
aai|	2|	1|	1|	1
aat|	0|	0|	0|	0
ab|	0	|0	|0	|0
abatement|	1|	1|	1|	1
absence|0	|0	|0	|0
...|...|...|...|...

				

### 5.3 Re-represent reports with a matrix with TF-IDF
TF-IDF is short for term frequency-inverse & inverse document frequency, which can reflect the importance of a word in a document.
5.3.1 Term frequency(TF)
Term frequency (TF) is define as the number of a word appears in a document. For example, “abatement” occurs in the first reports once, so the TF of “abatement” in the first report is 1. The high value of TF may imply the higher importance of the word in the report. 
5.3.2 Inverse document frequency(IDF)
Since some words in language occur so common that they exist almost everywhere. Obvious that kind of words are usually not so important and provide less information comparing to their frequency. So IDF is designed to diminish that effect. The inverse document frequency(IDF) can tell us if a word is rare in all documents, so it can filter the words appearing too commonly. Inverse document frequency 
IDF = log[1+N/(1+DF)],
DF is the document frequency, which means the number of document that a specific word appears. N is the total number of documents.
5.3.3 TF-IDF
For every word in a document, we can compute its TF-IDF, which is the product of its TF and IDF. By computing the TF-IDF, a matrix of TF-IDF can generated, too. Part of the matrix of TF-IDF is shown in Table 2.

##### Table 2: Part of the matrix of TF-IDF
word|	Report 1|	Report 2|	Report 3|	Report 4
---|---|---|---|---
aai|0.153782421|0.059501269|0.084724144|0.084510682
aat|0|	0|	0|	0
ab|	0|	0|	0|	0
abatement|	0.07502449|	0.058056731|	0.08266726|	0.082458981
Absence|0|0|0|0
…	|…	|…	|…	|…

### 5.4 Clustering
We use K-means to cluster words and documents. K-means clustering is an unsupervised algorithm for clustering to partition items into k clusters, each of which has the nearest mean to its items. Based on the TF-IDF matrix obtained above, K-means clustering is applied on both words and reports.
Following is the results of implementing K-means methods to analyze the daily report CONTRACTORS QUALITY CONTROL REPORT (QCR) DAILY LOG OF CONSTRUCTION – MILITARY, which includes the daily reports from 01 Nov 2004 to 17 Oct 2007, recorded the information about construction activities and events for every workday
For the words clustering, because most of words only occur for several times or even once in such many reports, the matrix of word frequency is sparse. So, we can find in the result of words clustering that such words are grouped in the same cluster. Since it is not easy to extract more specific information from a such large cluster, we exclude that cluster from the following analysis. Meanwhile, some clusters contain few words and have little information, so they are also excluded from the analysis. 
In the remaining four clusters of words, we find some words in the same cluster share some similarities. For example, many words in cluster 1 are related to transportation and loading. The words in cluster 2 are imply some relationships about wall foot, foundation, sewer and pipe. The cluster 3 contains relatively more words. It seems to contain many words about facilities indoor.
##### Table 3: Words Clusters
cluster|	words
---|---
1	|na	roman	truck	quantum	crusher	load	se	sl cat	hole	dec	hauli service	debris	driver	trench	update group	rfp	status	jd	rfi	demo	link	belt	samsung	aai       main	abatement	asbestos
2	|survey	pour	foundation	mains	narrative	layout	patio	excavation genuine	slab	backfill	jun		written	ir	lot	arauco foot	strip	porch	tie	density	forms	roller	sewer	rebar dust	receiv	spaces	unit	jcb	axelsen	form	pour	place    craw	grade	meet	layer	garage	pipe	attach            	water   mti
3	|overhead	bldg	roughin	sand	vanities	ceil	phon	blow    appliance	fire	oct	shingle	hvac	distribut	jan	nov      pass	nail	street	mold	cable	complete	kx	kobelco	marble discuss	west	insulate	texture	installation	tape	steer	hang drain	walk	skid	ways	kabota	misc	generator	review	interior nutek	pick	porches	temp	install	trusses	sideway	cabinet           storm	check	electrical	pressure	custom	rock	kitchen	plumb  specific	wall	pip	gas	heater	repairs	shingle	soil      driveway	critical	floors	test	way	observ	mcgahey	jack     contra    carpentry	base	conversations	backhoe	apprentice	stone door       sheetrock	dry	umc	build	dingo	dump	mason	hang       roof	paint	tap	taper	issues	set	gradall	forklift	west	roofer  installer	soffit	fascia
4	|forrest	lebaron	apr	jul	sep	aug	mar	common work	reports	repair	saturday	inspect	maintance	touch	loop   landscap	monday	friday	tuesday	wednesday	thursday         hardware	carpet	units	coe	doors	paint	perform

### 5.5 Visualization
We sum up the frequency of words in a same cluster and plot them with temporal order (Figure 7), and plot the reports cluster as well (Figure 8). The figures show that the peak periods of words frequencies are obviously corresponding to certain clusters of reports. 

 
##### Figure 8: words frequency for different cluster of words
![](https://github.com/ZhongzhuPeng/Construction_reports_processing_system_phase1/blob/master/README_IMG/8.png?raw=true)

From the Figure 6 we can find that there are three period during the project. The first period is from 15 Nov 2004 to 03 Mar 2005. In the first period, the words in cluster 1 appear with high frequency. That implies the activities of this period may be about transportation and loading. Second one is from 04 Mar 2005 to 10 Aug 2005, and the third one is from 11 Aug 2005 to 09 Feb 2007. Similarly, the second period and third period may be about construction of foundation and installation of facilities.
  
Figure 9: the clustering results of reports
![](https://github.com/ZhongzhuPeng/Construction_reports_processing_system_phase1/blob/master/README_IMG/9.png?raw=true)

For the clustering of reports, we found the results are apparently related to the date of the reports. For example, most reports from 15 Nov 2004 to 03 Mar 2005 are grouped into a same group. So we infer that the activities in that period recorded in the reports are probably similar.

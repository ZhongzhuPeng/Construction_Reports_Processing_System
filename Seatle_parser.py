
# coding: utf-8

# In[5]:

doc = open('Seattle_Reports.txt', 'rb')
text = doc.read()
head = '''CONTRACTORS QUALITY CONTROL REPORT (QCR)
DAILY LOG OF CONSTRUCTION - MILITARY'''


# In[6]:

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
        
print len(contents), '\n', fileNum


# In[7]:

weather = {}
activities_in_progress = {}
general_comments = {}
safety = {}
prep_init_date = {}
activity_start_finish = {}
qc_requiremnets = {}
qa_qc_punch_list = {}
contractors_on_site = {}
labor_hours = {}
equipment_hours ={}
accident_reporting = {}
for i in range(1, 882):
    report = contents[i]
    weather[i] = report[report.find('L.C.')+5 : report.find('QC NARRATIVES')] #find weather
    activities_in_progress[i] = report[report.find('Activities in Progress:')+24 : report.find('General Com m ents:')]
    general_comments[i] = report[report.find('General Com m ents:')+20 : report.find('Safety Inspection / Safety Meetings:')]
    safety[i] = report[report.find('Safety Meetings:')+17 : report.find('PREP/INITIAL')]
    prep_init_date[i] = report[report.find('PREP/INITIAL DATES')+19 : report.find('ACTIVITY START/FINISH')]
    activity_start_finish[i] = report[report.find('ACTIVITY START/FINISH')+22 : report.find('QC REQUIREMENTS')]
    qc_requiremnets[i] = report[report.find('QC REQUIREMENTS')+16 : report.find('QA/QC PUNCH LIST')]
    qa_qc_punch_list[i] = report[report.find('QA/QC PUNCH LIST')+17 : report.find('CONTRACTORS ON SITE')] 
    contractors_on_site[i] = report[report.find('CONTRACTORS ON SITE')+20 : report.find('LABOR HOURS')] 
    labor_hours[i] = report[report.find('LABOR HOURS')+12 : report.find('EQUIPMENT HOURS')] 
    equipment_hours[i] = report[report.find('EQUIPMENT HOURS')+16 : report.find('ACCIDENT REPORTING')] 
    accident_reporting[i] = report[report.find('ACCIDENT REPORTING')+19 : report.find('CONTRACTOR CERTIFICATION')] 


# In[8]:

import re
f = open('HTML/seatle_parsed.html', 'w')
f.write("<html>\n")
f.write("<head> TreeView\n")
f.write("    <script type=\"text/javascript\" src=\"mktree.js\"></script>\n")
f.write("    <link rel=\"stylesheet\" href=\"mktree.css\" type=\"text/css\">\n")
f.write("</head>\n\n")

f.write("<body>\n")

f.write("<ul class=\"mktree\">\n")

f.write("<li>weather<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+weather[i]+"</li>\n")
f.write("</ul></li>\n")

f.write("<li>activities_in_progress<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+activities_in_progress[i]+"</li>\n")
f.write("</ul></li>\n")

f.write("<li>general_comments<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+general_comments[i]+"</li>\n")
f.write("</ul></li>\n")

f.write("<li>safety<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+safety[i]+"</li>\n")
f.write("</ul></li>\n")

f.write("<li>prep_init_date<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+prep_init_date[i]+"</li>\n")
f.write("</ul></li>\n")

f.write("<li>activity_start_finish<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+activity_start_finish[i]+"</li>\n")
f.write("</ul></li>\n")

f.write("<li>qc_requiremnets<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+qc_requiremnets[i]+"</li>\n")
f.write("</ul></li>\n")

f.write("<li>contractors_on_site<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+contractors_on_site[i]+"</li>\n")
f.write("</ul></li>\n")

f.write("<li>labor_hours<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+labor_hours [i]+"</li>\n")
f.write("</ul></li>\n")

f.write("<li>equipment_hours<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+equipment_hours[i]+"</li>\n")
f.write("</ul></li>\n")

f.write("<li>accident_reporting<ul> \n")
for i in range(1, 882):
    f.write("    <li>"+"date: "+fileNum_date[i]+"\n"+accident_reporting[i]+"</li>\n")
f.write("</ul></li>\n")

    
f.write("</ul>\n")
f.write("</body>\n")
f.write("</html>\n")
   


# In[ ]:




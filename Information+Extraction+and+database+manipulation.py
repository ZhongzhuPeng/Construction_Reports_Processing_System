
# coding: utf-8

# # Extract text and its position

# In[1]:

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

class pdfPositionHandling:

    def parse_obj(self, lt_objs, pageNum, contents):
        # loop over the object list
        for obj in lt_objs:
            if isinstance(obj, pdfminer.layout.LTTextLine):
                text = obj.get_text().replace('\n','')
                fontname = self.parse_obj(obj._objs, pageNum, contents)
                if text in contents:
                    contents[text].append((obj.bbox[0], obj.bbox[1], fontname, pageNum))
                else:
                    contents[text] = [(obj.bbox[0], obj.bbox[1], fontname, pageNum)]
                
            if isinstance(obj, pdfminer.layout.LTChar):
                return obj.fontname
            
            # if it's a textbox, also recurse
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                self.parse_obj(obj._objs, pageNum, contents)

            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                self.parse_obj(obj._objs, pageNum, contents)

    def parsepdf(self, filename, startpage, endpage):

        # Open a PDF file.
        fp = open(filename, 'rb')

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Create a PDF device object.
        device = PDFDevice(rsrcmgr)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        contents = {}
        i = 0
        # loop over all pages in the document
        for page in PDFPage.create_pages(document):
            if i >= startpage-1 and i <= endpage-1:
                # read the page into a layout object
                interpreter.process_page(page)
                layout = device.get_result()

                # extract text from this object
                self.parse_obj(layout._objs, i, contents)
            i += 1
        return contents


# # Select file and directory

# In[2]:

#from Tkinter import *
#import tkFileDialog
from tkinter import *
import tkinter.filedialog

def select_file(title = 'Select the file'):
    win = Tk()
    win.title(title)
    var = StringVar()
    w = Label(win, text="File Path:")
    e = Entry(win, textvariable=var)
    b = Button(win, text="Browse",command=lambda:var.set(tkinter.filedialog.askopenfilename()))
    w.pack(side=LEFT)
    e.pack(side=LEFT)
    b.pack(side=LEFT)
    win.mainloop()
    return var.get()

def select_dir(title = 'Select the direnctory'):
    win = Tk()
    win.title(title)
    var = StringVar()

    w = Label(win, text="File Path:")
    e = Entry(win, textvariable=var)
    b = Button(win, text="Browse",command=lambda:var.set(tkinter.filedialog.askdirectory()))
    w.pack(side=LEFT)
    e.pack(side=LEFT)
    b.pack(side=LEFT)
    win.mainloop()

    return var.get()+'/'


# In[3]:

path1 = select_file('Select the PDF file') 
path2 = select_dir('Select the output file\'s direnctory')


# # select pages

# In[4]:

# The page number start from 1, not 0

#import Tkinter   
#import tkSimpleDialog    <- for python 2.7
import tkinter
import tkinter.simpledialog

def select_pages(title = 'Select Pages'):
    #root = Tkinter.Tk()
    root = tkinter.Tk()
    root.title(title)
    var1 = tkinter.StringVar()
    var2 = tkinter.StringVar()
    #b1 = Button(root, text="Select start page",command=lambda:var1.set(tkSimpleDialog.askinteger("Select start page", "enter page number", parent = root)))
    #b2 = Button(root, text="Select end page",command=lambda:var2.set(tkSimpleDialog.askinteger("Select end page", "enter page number", parent = root)))
    b1 = tkinter.Button(root, text="Select start page",command=lambda:var1.set(tkinter.simpledialog.askinteger("Select start page", "enter page number", parent = root)))
    b2 = tkinter.Button(root, text="Select end page",command=lambda:var2.set(tkinter.simpledialog.askinteger("Select end page", "enter page number", parent = root)))
    b1.grid(column = 0, row = 0)
    b2.grid(column = 1, row = 0)
    #var = tkSimpleDialog.askstring("Select Pates", "enter your name", parent = root)
    root.mainloop()
    start_page = var1.get()
    end_page = var2.get()
    return  (start_page, end_page)


# In[5]:

record_pos = pdfPositionHandling()
(start_page, end_page) = select_pages()
contents = record_pos.parsepdf(path1, int(start_page), int(end_page))
#for text in contents:
    #print(text)
    #print(contents[text])


# In[6]:

# get the positions of some sample pages
(start_page, end_page) = select_pages(title = 'Select Sample Pages')
first_page_contents = record_pos.parsepdf(path1, startpage=int(start_page), endpage=int(end_page))


# # Select categories

# In[15]:

# get filted contents
filted_contents = {}
for text in contents:
    if len(contents[text]) > 20:  ###set at beginning#####################
        filted_contents[text] = contents[text]
        #print(text + ' ' +str(len(filted_contents[text])))


# In[16]:

#from Tkinter import *
#import Tkinter as tk
import tkinter as tk

class SelectWin(tk.Frame):
     
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.vsb = tk.Scrollbar(self, orient="vertical")
        self.text = tk.Text(self, width=40, height=20, yscrollcommand=self.vsb.set)
        self.vsb.config(command=self.text.yview)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        
        self.temp_contents = {}

        var = []
        c = []
        for i, cat in enumerate(sorted(filted_contents)):
            c.append(cat)
            v = tk.BooleanVar()
            var.append(v)
            cb = tk.Checkbutton(self, text="#%s" % cat, variable=var[i])
            self.text.window_create("end", window=cb)
            self.text.insert("end", "\n") # to force one checkbox per line
                      
        def var_states():
            for i,v in enumerate(var):
                if v.get():
                    #print(c[i])
                    self.temp_contents[c[i]] = filted_contents[c[i]]
        tk.Button(root, text='Select', command=var_states).pack()


# In[18]:

root = tk.Tk()
root.title('selecte categories')
win = SelectWin(root)
win.pack(side="top", fill="both", expand=True)
root.mainloop()

filted_contents = win.temp_contents


# # Search neighbors

# In[19]:

from itertools import product
neighbors = {}
    
for line1, line2 in product(filted_contents, first_page_contents):
    key = line1
    value = line2
    if not key in neighbors:
        neighbors[key] = []
    if(line1 != line2 and line1 in first_page_contents
       and abs(int(first_page_contents[line1][0][0])-int(first_page_contents[line2][0][0]))<500    ###set at beginning
       and abs(int(first_page_contents[line1][0][1])-int(first_page_contents[line2][0][1]))<100): ###set at beginning
        neighbors[key].append(value)


# In[ ]:




# In[20]:

#import Tkinter as tk
#import ttk
import tkinter as tk
import tkinter.ttk

win = tk.Tk()
win.title("Set Pairs")   
 
tkinter.ttk.Label(win, text="Select category:").grid(column=0, row=0)   
pos_or_area = StringVar()
def select():  
    if pos_or_area.get() == 'area':
        ls = list(neighbors.keys())   
        ls += ['#END']
        dropdown2['values'] = ls
    else:
        ls = neighbors[category.get()]
        dropdown2['values'] = ls
    dropdown2.current()    

R1 = tkinter.ttk.Radiobutton(win, text="find by position", variable=pos_or_area, value='pos', command=select)
R1.grid(column = 2, row = 0)
R2 = tkinter.ttk.Radiobutton(win, text="find by area", variable=pos_or_area, value='area', command=select)
R2.grid(column = 3, row = 0)
    
pairs = {}
def bind():   
    #key = contents[category.get()]
    #new_value = contents[content.get()]
    key = category.get()
    if not key in pairs:
        pairs[key] = set([])
    
    if pos_or_area.get()=='pos':
        a = first_page_contents[category.get()][0]
        b = first_page_contents[content.get()][0]
        c = (b[0]-a[0], b[1]-a[1], b[2], pos_or_area.get())
        pairs[key].add(c)
    else:
        c = (content.get(), pos_or_area.get()) 
        pairs[key].add(c)
        
    dropdown2.current()
    
# creat a drop-down list
category = tk.StringVar()
dropdown1 = tkinter.ttk.Combobox(win, width=40, height=20, textvariable=category)
dropdown1['values'] = list(neighbors.keys())   
dropdown1.grid(column=0, row=1)      
#dropdown1.current(0)     


# create another drop-down list
content = tk.StringVar()
dropdown2 = tkinter.ttk.Combobox(win, width=40, textvariable=content)    
dropdown2.grid(column=2, row=1)  
 

# bind button
action = tkinter.ttk.Button(win, text="Bind", command=bind)
action.grid(column=4, row=1) 

win.mainloop()      # window


# In[21]:

body_start = 660    # the starting position of the body part


# In[22]:

def find_content_by_pos(content_map, content_pos):
    content = ()
    for c in content_map:
        m = 1 #### maximal error allowed#########################
        for pos in content_map[c]:
            error = abs(content_pos[0]-pos[0]) + abs(content_pos[1]-pos[1])
            #print error
            if error < m and content_pos[-1]==pos[-1]:
                content = (c, pos[0], pos[1], pos[2])
                break
    return content

def find_content_by_area(content_map, end_cat, start_pos):
    content = {}
    end_pos = (0,0,start_pos[-1]);
    
    if end_cat in content_map:
        for pos in content_map[end_cat]:
            if pos[-1] == start_pos[-1]:
                end_pos = pos
                break
    for c in content_map:
        for pos in content_map[c]:
            #print(pos, start_pos,end_pos)
            if pos[-1]==start_pos[-1] and pos[1] > end_pos[1] and pos[1] < start_pos[1]:
                #content.append((c, pos[0], pos[1], pos[2])) 
                
                if pos[1] in content:
                    content[pos[1]].append((c, pos[0], pos[1], pos[2])) 
                else:
                    content[pos[1]] = [(c, pos[0], pos[1], pos[2])]
                    
    if end_pos[1] == 0 and end_cat in content_map:
        for pos in content_map[end_cat]:
            if pos[-1] == start_pos[-1]+1:
                end_pos = pos
                break
        for c in content_map:
            for pos in content_map[c]:
                #print(pos, start_pos,end_pos)
                if pos[-1]==start_pos[-1]+1 and pos[1] > end_pos[1] and pos[1] < body_start:
                    #content.append((c, pos[0], pos[1], pos[2])) 
                    if pos[1]-1000 in content:
                        content[pos[1]-1000].append((c, pos[0], pos[1], pos[2])) 
                    else:
                        content[pos[1]-1000] = [(c, pos[0], pos[1], pos[2])]
    return content
    
data = {}
content_map = contents

for cat in pairs:
    #print(pairs[cat])
    pages = {}
    for pos in content_map[cat]:
        content = []
        for shift in pairs[cat]:
            if shift[-1] == 'pos':
                content_pos = (pos[0]+shift[0], pos[1]+shift[1], pos[2], pos[-1])
                content.append(find_content_by_pos(content_map, content_pos))
            elif shift[-1] == 'area':
                end_cat = shift[0]
                #if end_cat == '#END':
                    #continue #more?
                content = find_content_by_area(content_map, end_cat, pos)
        pages[pos[-1]] = content
    data[cat] = pages


# # Save data

# In[33]:

import pickle
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


# In[ ]:

#save data
#save_obj(data, 'seatle_all_for_mysql')
#save_obj(pairs, 'paris_seatle_all_for_mysql')
#save_obj(filted_contents, 'filted_all_for_mysql')


# In[ ]:

#pk_data = load_obj('seatle_all_for_mysql')
#pairs = load_obj('paris_seatle_all_for_mysql')


# # database

# In[ ]:

#pk_data = load_obj('seatle_all_for_mysql')
#data = pk_data #load data


# In[23]:

# dict for page number and REPORT NUMBER
report_num = {}
for i in data['REPORT NUMBER']: ###hardcoded. could be implemented by user interface
    report_num[i] = data['REPORT NUMBER'][i][0][0];
print(report_num)


# In[25]:

#group pages by report number
new_data = {}
for cat, content in data.items():
    new_content = {}
    #print(cat)
    #print(content)
    for page_num in content:
        #print(type(page_num))
        p = page_num
        while p >= 0:
            if p in report_num and not report_num[p] in new_content:
                new_content[report_num[p]] = content[page_num]
                break
            p -= 1
    new_data[cat] = new_content
#print(new_data['DATE'])
#save_obj(new_data, 'seatle_all_repnum_for_mysql')


# In[26]:

data = new_data


# In[27]:

header_items = []
body_items = []
for i in pairs:
    if next(iter(pairs[i]))[-1] == 'pos':
        header_items.append(i)
    else:
        body_items.append(i)
#print(header_items)
#print(body_items)


# In[28]:

# create the table header for the part of report header
table_header = ''
for i in header_items:
    table_header += i.replace(' ', '_')+' '+'varchar(200)'
    if i!=header_items[-1]:
        table_header += ', '
print(table_header)


# In[29]:

# row to be inserted into the table REPORT_HEADER
rows = []
for rep_num in set(report_num.values()): 
    row = ''
    for cat in header_items:
        row += "'"
        for t in data[cat][rep_num]:
            ##
            if len(t) == 0:
                row += 'NULL '
            else:
                row += t[0]+' '
        row += "'"
        if cat!=header_items[-1]:
            row += ', '
            #break
    rows.append(row)
    #print(row)
#print(rows)


# # connect to MySQL

# In[35]:

import MySQLdb
#connect to database
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        #passwd='******',
        db ='test',
        )
cur = conn.cursor()


# In[36]:

try:
    cur.execute("create table report_header(%s);" % table_header)
except Exception as err:
    print(err)


# In[37]:

#insert a row
for row in rows:
    print("insert into report_header values(%s);" % row)
    try:
        cur.execute("insert into report_header values(%s);" % row)
    except Exception as err:
        print(err)    


# In[38]:

# avoid encoding errors
conn.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')


# In[39]:

from operator import itemgetter
import sys,traceback

def process(cat_page, cat, rep_num):
    tb_ct = 0
    text = ''
    col_num = 0
    header = ''
    table_name = ''
    for linepos, line in reversed(sorted(cat_page.items())):
        
        if len(line) == 1:
            header = ''
            table_name = cat
            text += line[0][0]+' '
            #print(line[0][0])
        elif len(line) >1:
            line.sort(key=itemgetter(1)) # sorted by y position
            if header == '' or col_num<len(line): # if number of colunms larger than last row, create a table
                header = 'REPORT_NUMBER varchar(20), '
                col_num = len(line)
                
                count = 0
                for i in line:
                    count += 1
                    header += re.sub(r"[^A-Za-z0-9]", '_', i[0])+str(count)+' '+'varchar(200)'
                    if i!=line[-1]:
                        header += ', '
                
                tb_ct += 1
                table = re.sub('[^A-Za-z0-9]','_',table_name)+'_table_'+str(tb_ct)
                try:
                    #print("create table %s(%s);" % (table, header))
                    cur.execute("create table %s(%s);" % (table, header))
                except Exception as err:
                    #print("Exception:")
                    if(err.args[0] != 1050):
                        print(err)
                        #print("create table %s(%s);" % (table, header))
                    #print("\n")
                    
                text += 'TABLE'+str(tb_ct)+'\n '
            elif len(line)==col_num:
                row = rep_num+', '
                for t in line:
                    row += "'"+re.sub(r"'|&|-", "_", t[0])+"'"
                    if t!=line[-1]:
                        row += ', '
                #print("insert into %s values(%s);" % (table, row))
                try:
                    cur.execute("insert into %s values(%s);" % (table, row))
                except Exception as err:
                    #print("Exception:")
                    print(err)
                    #print("insert into %s values(%s);" % (table, row))
                    #print("\n")
                
            else:
                header = ''
                text += line[0][0]+' '
                #print(line[0][0])
    return text
                


# In[40]:

# create tables for categories in MySQL
for cat in body_items:
    h = re.sub(r"[^A-Za-z0-9]", '_', cat)
    if len(h) >= 30:
        h = h[:29]
    try:
        print("create table %s (REPORT_NUMBER varchar(20), %s varchar(10000))" % (h, h))
        cur.execute("create table %s (REPORT_NUMBER varchar(20), %s varchar(10000))" % (h, h))
    except Exception as err:
        print("Exception:")
        print(err)
        print("\n") 


# In[41]:

for rep_num in set(report_num.values()): 
    for cat in body_items:
        h = re.sub(r"[^A-Za-z0-9]", '_', cat)
        if len(h) >= 30:
            h = h[:29]
        
        row = ''
        #print(cat+'-------------')
        if rep_num in data[cat]: 
            s = process(data[cat][rep_num], cat, rep_num.replace(',', '')).replace("'", "_")
            row += "'"+re.sub(r"&", "_", s)+"'" #replace symbols to avoid errors in SQL
        else:
            row += "'"+'NULL'+"'"
        try:
            cur.execute("insert into %s values(%s, %s)" % (h, rep_num.replace(',', ''), row))
        except Exception as err:
            #print("Exception:")
            print(err)
            #print("insert into %s values(%s, %s)" % (h, rep_num.replace(',', ''), row))
            #print("\n")   


# In[42]:

# close the connection to database
cur.close()
conn.commit()
conn.close()


# In[ ]:




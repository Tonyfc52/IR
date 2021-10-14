import re
import xml.etree.ElementTree as XET
import json
import os.path as path
import tkinter as tk
from tkinter import *
from tkinter import Button, filedialog, font

filepath = 'wait...'


def openFile():
    global filepath
    text1.config(state='normal')
    text1.delete('1.0', 'end')
    filepath = filedialog.askopenfilename(
        initialdir=".", title="Open .xml or .json", filetypes=[(".xml or .json", ".xml .json")])
    text1.insert('1.0', filepath)
    text1.config(state='disable')
    display.delete('1.0', 'end')
    display.insert('1.0', 'Parse OK')


def startsearch():
    searchsort = enter1.get().split()
    if filepath.rfind('.xml') != -1:
        _mainxml(filepath, searchsort)

    elif filepath.rfind('.json') != -1:
        _mainjson(filepath, searchsort)


def asciicount(content):
    # ASCII編碼字元數0-127
    counter = 0
    for i in content:
        if ord(i) < 128:
            counter += 1
    return counter


def remark(searchsort, content):    # 文字反白處理
    p = re.split(r'(\b)', content)
    # 拆分文字
    for word in p:
        mark = 0
        display.tag_configure(
            'highlight', background='white', foreground='black')
        display.tag_configure('normal', background='black', foreground='white')
        for searchelem in searchsort:
            if searchelem == word:  # 完全符合
                mark = 1
            elif searchelem.title() == word:  # 句首首字大寫的可能
                mark = 1
        if mark == 0:
            display.insert(END, word, 'normal')
        if mark == 1:
            mark = 0
            display.insert(END, word, 'highlight')


def process(content):
    # 斷句統計
    # 原文在https://newbedev.com/python-regex-for-splitting-text-into-sentences-sentence-tokenizing
    m = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', content)
    return len(m)


def tweetsdisp(tweet, search):
    display.delete('1.0', 'end')
    """try to display tweets in readable condition"""
    tweetobj = []
    tweetobj.append(tweet['username'])
    tweetobj.append(tweet['full_name'])
    tweetobj.append(tweet['tweet_text'])
    tweetobj.append(tweet['tweet_time'])

    display.insert(END, '\nScreenName=@')
    remark(search, tweetobj[0])
    display.insert(END, '\nUsername=')
    remark(search, tweetobj[1])
    display.insert(END, '\nText=')
    remark(search, tweetobj[2])
    display.insert(END, '\nCreated time:'+tweetobj[3])

    display.insert(END, '\n\n************************\n\n')
    display.insert(
        END, '\nThe number of "Complete" sentences in tweet_text is : '+str(process(tweetobj[2])))
    display.insert(END, '\nThe ASCII characters of tweet_text : ' +
                   str(asciicount(tweetobj[2])))
    display.insert(END, '\nWords in tweet_text (encoded by ASCII) : ' +
                   str(len((tweetobj[2].encode(encoding='ascii', errors='ignore')).split())))
    display.insert(END, '\n\n************************\n\n')


def _mainxml(filename, search):
    tree = XET.parse(filename)
    root = tree.getroot()
    paper = []  # 文章list
    paperstructure = []  # 文章標題：有其必要保留
    display.delete('1.0', 'end')

    for child in root.findall('./PubmedArticle'):
        pool = []
        poolstructure = ['TITLE']
        papertitle = child.find('.//ArticleTitle').text
        pool.append(papertitle)
        for grandchild in child.iter(tag='AbstractText'):
            if grandchild.attrib != {}:
                label = grandchild.attrib['Label']
                poolstructure.append(label)
            abstract = ''.join(grandchild.itertext())
            pool.append(abstract)
        paper.append(pool)
        paperstructure.append(poolstructure)

    count = 0  # PAPER編號
    for quantity in paper:
        NumofSentence = 0  # 句數統計
        Numofword = 0      # 字數統計
        Numofascii = 0     # ASCII字元統計
        section = 0  # 段落編號
        display.insert(END, '\n')
        for x in quantity:
            Numofword += len(x.split())
            Numofascii += asciicount(x)
            if section == 0:
                display.insert(
                    END, paperstructure[count][section])  # 列印標題
                display.insert(END, '\n')
                remark(search, x)

                display.insert(END, '\n\n')
                display.insert(END, 'Abstract:\n\n')

            elif section > 0:
                if len(paperstructure[count]) > 1:  # 判斷是否還有短文段落標題
                    display.insert(END, paperstructure[count][section]+'\n')
                NumofSentence += process(x)
                remark(search, x)
                display.insert(END, '\n\n')
            section += 1
        count += 1
        display.insert(
            END, '\n***********************************************************************\n\n')
        display.insert(
            END, 'The number of sentences is (title excluded): '+str(NumofSentence))
        display.insert(END, '\n')
        display.insert(
            END, 'The word number in article  is (label excluded):'+str(Numofword))
        display.insert(END, '\n')
        display.insert(
            END, 'ASCII encoding characters of whole abstrat: '+str(Numofascii))
        display.insert(
            END, '\n***********************************************************************\n\n')


def _mainjson(filename, search):
    # 用UTF-8編碼打開.json檔案
    with open(filename, encoding='UTF-8') as f:
        content = json.load(f, strict=False)

    if type(content) == list:
        for sub in content:
            subdict = dict(sub)
            tweetsdisp(subdict, search)


# GUI starts here!
main = tk.Tk()
main.title("Homework 1 - search in .xml and .json")
main.geometry("840x600+200+200")
main.resizable(FALSE, True)
main.maxsize(840, 1024)

fontsize = font.Font(size=14)

# get filepath and display
button1 = Button(text='Open file', font=fontsize, command=openFile)

text1 = Text(main, state='normal', font=fontsize, width=60, height=1)

# search option
text2 = Label(main, text='Keyword(s):', font=fontsize)
enter1 = Entry(main, relief='groove', width=60, font=fontsize)

# start search
button2 = Button(text='Search', command=startsearch, font=fontsize)

# display area
f = tk.Frame(main)
display = Text(f, background='black', foreground='white',
               width=80, height=50, font=('courier', 12), wrap=WORD)
scrollbar = Scrollbar(f)
scrollbar.config(command=display.yview)
display.config(yscrollcommand=scrollbar.set)
display.pack(side=LEFT)
scrollbar.pack(side=RIGHT, fill=Y)


text1.grid(row=0, column=0, columnspan=5, sticky=E)
button1.grid(row=0, column=5, sticky=E)
text2.grid(row=1, column=0, columnspan=1, sticky=E)
enter1.grid(row=1, column=1, columnspan=4, sticky=W)
button2.grid(row=1, column=5, sticky=E)
f.grid(row=3, column=0, columnspan=7)


main.mainloop()

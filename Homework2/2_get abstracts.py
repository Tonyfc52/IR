import requests
import time
from tkinter import filedialog

pmidlist = []
count = 0
group = []


def readfile(file):
    global pmidlist
    global count
    with open(file) as f:
        for line in f:
            pmidlist.append(line.rstrip('\n'))
    count = len(pmidlist)
    print(count)
    print(pmidlist)


def group100(pmidlist, count):
    global group
    pmid = ''
    for id in range(count):
        pmid += pmidlist[id]+'+'
        if (id+1) % 100 == 0:
            group.append(pmid.rstrip('+'))
            pmid = ''
        elif id == count:
            group.append(pmid.rstrip('+'))
    print(group)


def fetchfile(group):
    for bundle in group:
        i = str(1+group.index(bundle)*100)+'-'+str((group.index(bundle)+1)*100)
        filename = i+'.xml'
        print('dumping to ', filename)
        id = bundle
        wholepath = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=' + \
            id+'&retode=xml&rettype=abstract'
        try:
            r = requests.get(wholepath)
        except:
            break
        xml = open(filename, 'w', encoding='UTF-8')
        xml.write(r.text)
        xml.close()
        print('wait for 10 second....')
        time.sleep(10)


# Start here
filepath = filedialog.askopenfilename(
    initialdir='.', title="Open .txt", filetypes=[("TXT files", ".txt")])
if filepath == '':
    print('Exit!')
else:
    readfile(filepath)
    group100(pmidlist, count)
    fetchfile(group)

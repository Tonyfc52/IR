# Import XML
import re
import xml.etree.ElementTree as XET
import json
import os.path as path


def process(content):
    # 斷句統計
    # 原文在https://newbedev.com/python-regex-for-splitting-text-into-sentences-sentence-tokenizing
    m = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', content)
    return len(m)


def asciicount(content):
    #ASCII編碼字元數0-127
    counter =0
    for i in content:
        if ord(i) < 128:
            counter += 1
    return counter


def remark(searchsort, content):    # 文字反白處理
    p = re.split(r'(\b)', content)
    # 拆分文字
    for word in p:
        mark = 0
        for searchelem in searchsort:
            if searchelem == word:  # 完全符合
                mark = 1
            elif searchelem.title() == word:  # 句首首字大寫的可能
                mark = 1
        if mark == 0:
            print(word+'\033[0m', end='')
        if mark == 1:
            mark = 0
            print('\033[10;30;47m'+word+'\033[0m', end='')


def tweetsdisp(tweet, search):
    """try to display tweets in readable condition"""
    tweetobj = []
    tweetobj.append(tweet['username'])
    tweetobj.append(tweet['full_name'])
    tweetobj.append(tweet['tweet_text'])
    tweetobj.append(tweet['tweet_time'])

    print('ScreenName=@', end='')
    remark(search,tweetobj[0])
    print('\nUsername=', end='')
    remark(search,tweetobj[1])
    print('\nText=')
    remark(search, tweetobj[2])
    print('\nCreated time:', tweetobj[3])

    print('\n'+'************************')
    print('The number of "Complete" sentences in tweet_text is', process(tweetobj[2]))
    print('The ASCII characters of tweet_text:', asciicount(tweetobj[2]))
    print('Words in tweet_text (encoded by ASCII)', len((tweetobj[2].encode(encoding='ascii', errors='ignore')).split()))

    print('-----------------\n')


def _mainxml(filename, search):
    tree = XET.parse(filename)
    root = tree.getroot()
    paper = []  # 文章list
    paperstructure = []  # 文章標題：有其必要保留

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

        for x in quantity:
            Numofword += len(x.split())
            Numofascii += asciicount(x)
            if section == 0:
                print(paperstructure[count][section])  # 列印標題
                remark(search, x)
                
                print('\n')
                print('Abstract:'+'\n')

            elif section > 0:
                if len(paperstructure[count]) > 1:  # 判斷是否還有短文段落標題
                    print(paperstructure[count][section])
                NumofSentence += process(x)
                remark(search, x)
                print('\n')
            section += 1
        count += 1
        print('***********************************************************************')
        print('The number of sentences is (title excluded) ', NumofSentence)
        print('The word number in article  is (label excluded)', Numofword)
        print('ASCII encoding characters of whole abstrat:', Numofascii)
        print('\n')


def _mainjson(filename, search):
    # 用UTF-8編碼打開.json檔案
    with open(filename, encoding='UTF-8') as f:
        content = json.load(f, strict=False)
    
    if type(content) == list:
        for sub in content:
            subdict = dict(sub)
            tweetsdisp(subdict, search)


# Start here!
filename = input('Please enter the filename:').rstrip()
search = input('Please enter the keywords:').split()
searchsort = sorted(search, key=lambda i: len(i), reverse=False)

if path.exists(filename) == False:
    print('File not existed!')

elif filename.rfind('.xml') != -1:
    _mainxml(filename, searchsort)

elif filename.rfind('.json') != -1:
    _mainjson(filename, searchsort)

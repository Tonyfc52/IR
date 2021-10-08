# Import XML
import re
import xml.etree.ElementTree as XET
import json
import os.path as path


def process(content):
    # 斷句分析，統計參數
    # 原文在https://newbedev.com/python-regex-for-splitting-text-into-sentences-sentence-tokenizing
    m = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', content)
    return len(m)


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
    sentence = 0
    tweetobj.append(tweet['username'])
    tweetobj.append(tweet['full_name'])
    tweetobj.append(tweet['tweet_text'])
    tweetobj.append(tweet['tweet_time'])

    print('ScreenName=@'+tweetobj[0])
    print('Username='+tweetobj[1])
    print('Text=\n')
    remark(search, tweetobj[2])

    sentence = process(tweetobj[2])
    print('\n'+'Created at:', tweetobj[3])

    print('\n'+'************************')
    print('The number of "Complete" sentences in Text is', sentence)

    print('-----------------\n')


def _mainxml(filename, search):
    tree = XET.parse(filename)
    root = tree.getroot()
    paper = []  # 文章list
    paperstructure = []  # 文章標題：有其必要保留

    for child in root.findall('./PubmedArticle'):
        pool = []
        poolstructure = ['TITLE']
        labelnum = 0
        papertitle = child.find('.//ArticleTitle').text
        pool.append(papertitle)
        for grandchild in child.iter(tag='AbstractText'):
            if grandchild.attrib != {}:
                label = grandchild.attrib['Label']
                labelnum += 1  # 標籤通常為標題，不算句子，統計之後扣除
                poolstructure.append(label)
            abstract = ''.join(grandchild.itertext())
            pool.append(abstract)
        paper.append(pool)
        paperstructure.append(poolstructure)

    count = 0  # PAPER編號
    for quantity in paper:
        NumofSentence = 0  # 句數統計
        Numofword = 0
        section = 0  # 段落編號
        for x in quantity:
            Numofword += len(x.split())
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
        print('The number of article words is (label excluded)', Numofword)
        print('\n')


def _mainjson(filename, search):
    # 用UTF-8編碼打開.json檔案
    with open(filename, encoding='UTF-8') as f:
        content = json.load(f, strict=False)
    print(content)
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

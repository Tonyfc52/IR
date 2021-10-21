# Import XML
import re
import xml.etree.ElementTree as XET
import os.path as path
from nltk import word_tokenize


def process(content):
    m = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', content)
    return len(m)


def asciicount(content):
    counter = 0
    printable = 0
    for i in content:
        if ord(i) < 128:
            counter += 1
            if ord(i) > 32:
                printable += 1
    return counter, printable


def _mainxml(filename):
    # 這次先把主結構拿出來
    tree = XET.parse(filename)
    root = tree.getroot()
    pool = []
    for child in root.findall('./PubmedArticle'):
        for grandchild in child.iter(tag='AbstractText'):
            abstract = ''.join(grandchild.itertext())
            pool.append(abstract)
    NumofSentence = 0  # 句數統計
    Numofword = 0      # 字數統計
    Numofascii = []    # 呼叫asciiount回傳會是一個list
    totalascii = 0
    totalprintableascii = 0
    for quantity in pool:
        Numofword += len(quantity.split())  # 用whitespace斷字
        Numofascii = asciicount(quantity)
        totalascii += Numofascii[0]
        totalprintableascii += Numofascii[1]
        NumofSentence += process(quantity)

    print('***********************************************************************')
    print('Filename: ', filename)
    print('The number of sentences is ', NumofSentence)
    print('The word number in abstract  is ', Numofword)
    print('ASCII encoding characters of whole abstrat:', totalascii)
    print('ASCII encoding printable characters of whole abstrat:',
          totalprintableascii)
    return pool


def comparison(paperA, paperB):
    print('***********************************************************************')
    if len(paperA) != len(paperB):
        print('\n The paragraph number of article(s) is not matched! \n')
    else:
        print('Method 1: Using split() in whitespace..\n')
        notmatch = 0
        for i in range(len(paperA)):
            wordsA = paperA[i].split()
            wordsB = paperB[i].split()
            wordnumA = len(wordsA)
            wordnumB = len(wordsB)
            if wordnumA != wordnumB:
                print('\n The word number of corresponding paragraph is not matched! \n')
                notmatch = 1
            else:
                for j in range(wordnumA):
                    if wordsA[j] != wordsB[j]:
                        if j < 5:
                            stringA = ' '.join(wordsA[0:j+9])
                            stringB = ' '.join(wordsB[0:j+9])
                        else:
                            stringA = ' '.join(wordsA[j-5:j+6])
                            stringB = ' '.join(wordsB[j-5:j+6])
                        print('fileA: ', stringA)
                        print('fileB: ', stringB)
                        notmatch = 1
                        print(
                            '\"', wordsA[j], '\" is not matched to coressponding to \"', wordsB[j], '\"\n')
        print('\nMethod 1 finished.')
        if notmatch == 0:
            print('\nThe abstrast of PaperA is the same as PaperB\'s')
        else:
            print(
                '\nThe paperA and paperB are not matched!\n')
        print('\n********************************************')
        print('\nMethod 2: using NLTK tokenization to split\n')
        notmatch = 0
        for i in range(len(paperA)):
            tokenA = word_tokenize(paperA[i])
            tokenB = word_tokenize(paperB[i])
            wordnumA = len(tokenA)
            wordnumB = len(tokenB)
            if wordnumA != wordnumB:
                print('\n The word number of corresponding paragraph is not matched! \n')
                notmatch = 1
            else:
                for j in range(wordnumA):
                    if tokenA[j] != tokenB[j]:
                        if j < 5:
                            stringA = ' '.join(tokenA[0:j+9])
                            stringB = ' '.join(tokenB[0:j+9])
                        else:
                            stringA = ' '.join(tokenA[j-5:j+6])
                            stringB = ' '.join(tokenB[j-5:j+6])
                        print('fileA: ', stringA)
                        print('fileB: ', stringB)
                        notmatch = 1
                        print(
                            '\"', tokenA[j], '\" is not matched to coressponding to \"', tokenB[j], '\"\n')
        print('\nMethod 2 finished.')
        if notmatch == 0:
            print('\nThe abstrast of PaperA is the same as PaperB\'s')
        else:
            print(
                '\nThe paperA and paperB are not matched!\n')


# Start here!
# rstrip將多餘右邊空白去掉
filenameA = input('Please enter the xml filenameA:').rstrip()
filenameB = input('Please enter the xml filenameB for comparison:').rstrip()
paperA = []
paperB = []
if path.exists(filenameA) == False:
    print('FileA not existed!')
elif path.exists(filenameB) == False:
    print('FileB not existed!')
else:
    paperA = _mainxml(filenameA)
    paperB = _mainxml(filenameB)
    comparison(paperA, paperB)

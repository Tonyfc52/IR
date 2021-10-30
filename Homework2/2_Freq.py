from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pandas as pd


def generatetable(purpose, listname, table, wordcolumn, freqcolumn):
    tablename = str(table)
    fdist = FreqDist(purpose)
    listname = list(fdist.most_common())
    table = pd.DataFrame(listname, columns=[wordcolumn, freqcolumn])
    table[freqcolumn] = table[freqcolumn].astype(int)
    table.to_csv(tablename+'.csv')


f = open('allwords.txt', encoding='utf-8')
words = f.read().split(' ')
f.close()

# Normal count
generatetable(words, 'freqlist', 'freq_normal', 'word', 'freq')

# Non-stopwords count
stop = set(stopwords.words('english'))
nostopbag = []
for i in words:
    if i in stop:
        pass
    else:
        nostopbag.append(i)
generatetable(nostopbag, 'freqlist', 'freq_nostop', 'word', 'freq')

# Porter stemming
stemmer = PorterStemmer()
afterstem = []
stembag = []
for i in words:
    j = stemmer.stem(i)
    if j != i:
        afterstem.append(j)
        # beforestem.append(i)
    stembag.append(j)

generatetable(stembag, 'freqlist', 'freq_afterstem', 'stemword', 'freq')

changes = pd.Series(afterstem)
counting = changes.value_counts()


changetable = pd.DataFrame(
    {'stemword': counting.index, 'times': counting.values})
changetable.to_csv('list_of_stemwords.csv', index=False)

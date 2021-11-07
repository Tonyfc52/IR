from nltk.stem import PorterStemmer
import pandas as pd


f = open('allwords.txt', encoding='utf-8')
words = f.read().split(' ')
f.close()

# Porter stemming
stemmer = PorterStemmer()

stemdict = {}

for i in words:
    j = stemmer.stem(i)

    if j != i:
        if j in stemdict.keys():
            if i in stemdict.get(j):
                pass
            else:
                stemdict[j] = stemdict.get(j)+' '+i

        else:
            stemdict[j] = i


form = pd.DataFrame.from_dict(
    stemdict, orient='index', columns=['origin words'])
form.index.name = 'stemword'
form.to_csv('list_to_stemwords.csv')

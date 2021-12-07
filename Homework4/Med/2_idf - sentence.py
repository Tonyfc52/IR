import math
import pandas as pd
#from nltk import word_tokenize


paras = pd.read_excel('nostop.xlsx')
paralist = []
list_temp = []
for i in range(len(paras)):
    list_temp = paras.iloc[i][2].split(' ')
    list_temp.pop(0)
    paralist.append(list_temp)


wordset = pd.read_csv('wordset.csv', sep='\n', header=None, names=['token'])
df = []
idf = []
sindex = []

vectorcolumn = [i for i in range(len(paras))]
vectorrow = wordset['token']

vectors = pd.DataFrame(columns=vectorcolumn, index=vectorrow)


for i in range(len(wordset)):
    freq = 0
    index = ''
    s_index = ''
    flag = 0
    for k in range(len(paras)):
        if wordset.iloc[i][0] in paralist[k]:
            s_index = s_index+' '+str(k)
            freq += 1

    df.append(freq)
    idf.append(math.log10(len(paras)/freq))
    sindex.append(s_index)

wordset.insert(1, 'freq', df)
wordset.insert(2, 'idf', idf)
wordset.insert(3, 'd_index', sindex)
wordset.to_excel('df-sentence.xlsx', index=0)

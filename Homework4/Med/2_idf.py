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
dindex = []
sindex = []
parano = paras.iloc[-1][0] + 1
for i in range(len(wordset)):
    freq = 0
    index = ''
    s_index = ''
    flag = 0
    for k in range(len(paras)):
        if wordset.iloc[i][0] in paralist[k]:
            s_index = s_index+' '+str(k)
            if flag == paras.iloc[k][0] and freq != 0:
                pass
            else:
                freq += 1
                flag = paras.iloc[k][0]
                index = index + ' ' + str(paras.iloc[k][0])

    df.append(freq)
    idf.append(math.log10(parano/freq))
    dindex.append(index)
    sindex.append(s_index)

wordset.insert(1, 'freq', df)
wordset.insert(2, 'idf', idf)
wordset.insert(3, 'd_index', dindex)
wordset.insert(4, 's_index', sindex)
wordset.to_excel('df.xlsx', index=0)

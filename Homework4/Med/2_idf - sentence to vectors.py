import math
import pandas as pd


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


vectorcolumn = list(wordset['token'])

vectors = pd.DataFrame(columns=vectorcolumn)


for k in range(len(paralist)):
    sentvector = []
    for term in vectorcolumn:
        sent = paralist[k]
        counter = sent.count(term)
        sentvector.append(counter)
    vectors.loc[k] = sentvector

vectors.to_pickle('sent2vec_xz.pkl', compression='xz', index=False)

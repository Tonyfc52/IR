#tf and idf
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer

from collections import Counter

paratitle = pd.read_excel('para.xlsx')
sent2vec = pd.read_pickle('sent2vec_xz.pkl', compression='xz')
wordset = pd.read_csv('wordset.csv', sep='\n', header=None, names=['token'])

array=[]
for i in range(len(sent2vec)):
    array.append(list(sent2vec.iloc[i]))

transformer=TfidfTransformer()
tfidf=transformer.fit_transform(array)
tfidfarray= tfidf.toarray()

print(len(wordset))
print(len(sent2vec))
print(len(paratitle))

print(tfidfarray.shape)
print('\n')
print(tfidf[0])
print('\n')
print(tfidf[2212])




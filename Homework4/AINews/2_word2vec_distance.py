# word2vec
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import pandas as pd

model=KeyedVectors.load('w2v.model')
vector=model.wv

word= vector.key_to_index

distance=pd.read_csv('wordset.csv', sep='\n', header=None, names=['token'])

distlist=[]
for i in range(len(distance)):
    getvector=vector[distance.iloc[i][0]]
    sqsum=float(0)
    for x in getvector:
        sqsum= (x)**2 + sqsum
    dist=sqsum**0.5
    distlist.append(dist)


distance.insert(1,'distance', distlist)
    
distance.to_excel('nostop2v_distance.xlsx')
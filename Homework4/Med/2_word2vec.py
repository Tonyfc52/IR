# word2vec
from gensim.models import Word2Vec
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

token = pd.read_excel('token.xlsx')

reform = token['sententoken']
tokensent = []
for i in reform:
    i = i.split(' ')
    i.pop(0)
    tokensent.append(i)


model = Word2Vec(sentences=tokensent, window=3, sg=1,
                 vector_size=250, min_count=1, epochs=10, workers=6)
vector = model.wv

model.save('w2v.model')

print(vector['radiation'])

from gensim import models
from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pandas as pd

# 秀鄰近vectors的範例




def w2vallplot(model):

    all_words = list(model.key_to_index)
    X = model[all_words]
    tsne = TSNE(n_components=2)
    X_tsne = tsne.fit_transform(X[:500, :])
    df = pd.DataFrame(X_tsne, index=all_words[:500], columns=['x', 'y'])
    fig = plt.figure(figsize=[8, 8])
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(df['x'], df['y'])
    for word, pos in df.iterrows():
        ax.annotate(word, pos)
    plt.show()


model = Word2Vec.load('w2v.model')
vector = model.wv

w2vallplot(vector)

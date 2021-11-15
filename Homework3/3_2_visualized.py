from gensim import models
from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pandas as pd

# 秀鄰近vectors的範例


def w2vplot(model, word, shape):
    group = np.empty((0, shape), dtype='f')
    labels = [word]
    close_words = model.most_similar(word, topn=20)

    group = np.append(group, np.array([model[word]]), axis=0)
    for score in close_words:
        word_vector = model[score[0]]
        labels.append(score[0])
        group = np.append(group, np.array([word_vector]), axis=0)

    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    X = tsne.fit_transform(group)
    x_coords = X[:, 0]
    y_coords = X[:, 1]

    # display scatter plot
    plt.scatter(x_coords, y_coords, c='green')

    for label, x, y in zip(labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(
            0, 0), textcoords='offset points')
    plt.xlim(x_coords.min(), x_coords.max())
    plt.ylim(y_coords.min(), y_coords.max())
    plt.autoscale(enable=False)
    plt.show()

# Demo前面500字（太多會很亂）


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

# Demo兩個字的標示


def w2v2wordplot(model, word1, word2, word3, word4):
    X1 = model[word1, word2, word3, word4]
    tsne = TSNE(n_components=2)
    X_tsne = tsne.fit_transform(X1)
    df = pd.DataFrame(
        X_tsne, index=[word1, word2, word3, word4], columns=['x', 'y'])
    fig = plt.figure(figsize=[8, 6])
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(df['x'], df['y'])
    for word, pos in df.iterrows():
        ax.annotate(word, pos)
    plt.show()


model = Word2Vec.load('w2vSG5k.model')
vector = model.wv
shape = vector['vaccine'].shape[0]
w2vplot(vector, 'fever', shape)
w2vallplot(vector)
w2v2wordplot(vector, 'chadox1', 'thrombosis',
             'bnt162b2', 'pericarditis')

result = vector.most_similar(
    positive=['bnt162b2', 'chadox1'], negative=['pericarditis'])

for i in result:
    print(i)

# Dumping strings
from nltk.tokenize import word_tokenize
import re

import pandas
import string
from gensim.models import Word2Vec
import time

origin = pandas.read_csv('5ktext.csv')
abstract = str
token = []
#stop_words = stopwords.words('english')

filtered = []
for i in origin['abstract']:
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', i)

    for j in sentences:  # 每句
        word = []
        token = word_tokenize(j)
        for k in token:  # 每字
            if k in string.punctuation:
                pass
            else:
                word.append(k.lower())
        filtered.append(word)


corpus = pandas.Series(filtered)
corpus.to_csv('corpus5k.csv', index=False)

print('CBOW start:', time.ctime())
model = Word2Vec(sentences=filtered, window=5, sg=0,
                 vector_size=100, min_count=2, epochs=10)
print('CBOW end:', time.ctime())

model.save('w2vCBOW5k.model')


print('Skip-Gram start:', time.ctime())
model1 = Word2Vec(sentences=filtered, window=3, sg=1,
                  vector_size=100, min_count=2, epochs=5)
print('Skip-Gram end:', time.ctime())

model1.save('w2vSG5k.model')

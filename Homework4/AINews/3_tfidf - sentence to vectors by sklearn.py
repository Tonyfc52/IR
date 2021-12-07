import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
#import pickle


def tfidfarray(sent2vec):
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(sent2vec)
    result = tfidf.toarray()
    return result


def querytoarray(query, feature):
    queryterm = query.split(' ')
    vector = [0 for i in range(len(feature))]
    for i in queryterm:
        for j in range(len(feature)):
            if i == feature[j]:
                vector[j] += 1
    return vector


# ______________Start from here______________
paras = pd.read_excel('nostop.xlsx')
paralist = []  # 每個句子的token list
for i in range(len(paras)):
    paralist.append(paras.iloc[i][2])


# Sklearn中 tf=頻率, idf= log((n)/(1+df(t)))
# 轉換向量為s2v
vectorizer = CountVectorizer(token_pattern=r"\S+")  # 因為已經先處理過了，所以不再進一步處理
s2v = vectorizer.fit_transform(paralist)
# 獲得sklearn向量化後的字代表編號並且寫入
feature = list(vectorizer.get_feature_names_out())

# ------------檔案處理區------------
#f = open('wordset_sklearn.csv', 'w', encoding='utf-8')
# for word in feature:
#    f.write(word+'\n')
# f.close()
# with open('sent_skvector.pk', 'wb') as file:
#    pickle.dump(s2v, file)
# -----------------------------------


# tfidf結果，且normalized by sklearn
s2v_tfidf = tfidfarray(s2v)

query = input('Please enter some words separated by space: ')
q_vector = []
q_vector.append(querytoarray(query, feature))  # 將query向量弄成一個document
q_tfidf = tfidfarray(q_vector)

# 用cosine_similarity來找
score = (cosine_similarity(q_tfidf, s2v_tfidf))

loadfile = pd.read_excel('sent.xlsx')
sentence = pd.DataFrame({'sentence': loadfile['sent'], 'score': score[0]})
sentence = sentence.sort_values(by=['score'], ascending=False)

# load spacy engine
sp = spacy.load('en_core_web_sm')

for i in range(10):
    pos = sp(sentence.iloc[i][0])
    print('Rank:', i+1, 'score:', sentence.iloc[i][1])
    print(pos.text)
    for word in pos:
        print(word.pos_, end=' ')

    print('\n')

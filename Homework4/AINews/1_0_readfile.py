import pandas as pd
import regex as re
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from gensim.models import Word2Vec

origin = pd.read_excel('ainews.xlsx')
stop_words = stopwords.words('english') + \
    ["'d", "'s", "'ve", "'ll", "'re", "'m"]
additionpunc = '—’“”;'


newsno = []
parano = []
sentno = []

paragraphs = []
sentences = []  # 將paragraphy斷句
sententoken = []  # for tokenization後的句子
wordset = []
nostopsent = []

for i in range(len(origin)):
    origin.iloc[i][1] = origin.iloc[i][1].replace(u'\u200b', "")
    section = re.split(r'\n', origin.iloc[i][1])
    for j in section:
        if len(j) == 0:
            pass
        else:
            j = j.replace("[", "")
            j = j.replace("]", "")
            j = j.replace("—", "-")
            j = j.replace("“", "\"")
            j = j.replace("”", "\"")
            j = j.replace("’", "\'")
            j = j.replace("‘", "\'")
            j = j.replace(" '", " ")
            j = j.replace(".\"", "\'.")
            j = j.replace(",\"", "\',")
            j = j.replace(u'\u200b', "")  # 特別的空白字元，移除
            newsno.append(i)
            paragraphs.append(j)

para = pd.DataFrame({'news': newsno, 'para': paragraphs})
para.to_excel('para.xlsx', index=0)

# adjust puntuations
for i in range(len(paragraphs)):
    temp = re.split(
        r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraphs[i])
    for j in range(len(temp)):
        tokentemp = ''
        nostoptemp = ''
        if len(temp[j]) == 0:
            pass
        else:
            sentences.append(temp[j])
            temp[j] = temp[j].replace("\"", " ")

            for k in word_tokenize(temp[j]):
                if k in string.punctuation or len(k) == 0 or k == '``' or k == "''" or k in additionpunc:
                    pass
                else:
                    tokentemp = tokentemp + ' ' + k.lower()
                    if k.lower() in stop_words:
                        pass
                    else:
                        nostoptemp = nostoptemp + ' ' + k.lower()
                        wordset.append(k.lower())

            sententoken.append(tokentemp)
            nostopsent.append(nostoptemp)
            sentno.append(j)
            parano.append(i)

sent = pd.DataFrame({'para': parano, 'sentno': sentno, 'sent': sentences})

senttoken = pd.DataFrame({'para': parano, 'sentno': sentno,
                          'sententoken': sententoken})
nostop = pd.DataFrame(
    {'para': parano, 'sentno': sentno, 'nostoptoken': nostopsent})
senttoken.to_excel('token.xlsx', index=0)
nostop.to_excel('nostop.xlsx', index=0)
sent.to_excel('sent.xlsx', index=0)


wordset = set(wordset)
wordset = list(wordset)
wordset.sort()

#f = open('wordset.csv', 'w', encoding='utf-8')
#for i in wordset:
#    f.write(i+'\n')
#f.close()


#Training
traintokens=[]
for i in sententoken:
    splitting=i.split(' ')
    splitting.pop(0)
    traintokens.append(splitting)
model = Word2Vec(sentences=traintokens, window=5, sg=1,
                 vector_size=300, epochs=15, min_count=1)
model.save('w2v.model')

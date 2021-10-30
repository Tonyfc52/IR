import pandas as pd
import glob
import os
import string
from nltk import tokenize


def loadorigin():
    global body
    # 撈取原先的CSV
    workdir = os.getcwd()
    csvfiles = glob.glob(workdir+'\\csv\\*.csv')

    for file in csvfiles:
        csvread = pd.read_csv(file)
        body = pd.concat([body, csvread], ignore_index=True)

    # 丟掉原先多餘的index
    body = body.drop(body.columns[2], axis=1)
    body.to_csv('all10k.csv')
    return body


# ******start here
body = pd.DataFrame({"title": [], "abstract": []})
try:
    body = pd.read_csv('all10k.csv')
except:
    loadorigin()
# tokenized
alltxt = list(body["abstract"])
tokens = []
words = []

# 分解，將每一篇放到tokens，全部文字丟到words
# 單一標點符號先去掉
for i in alltxt:
    nopunktoki = []
    if str(i) == 'nan':
        nopunktoki.append('')
    else:
        toki = tokenize.word_tokenize(i)
        for t in toki:
            if t in string.punctuation:
                pass
            else:  # 都小寫
                nopunktoki.append(t.lower())
                words.append(t.lower())
    tokens.append(nopunktoki)

# 個別token寫入個別文章，感覺以後會用到
tokenbody = pd.DataFrame(columns=["title", "tokens"])
tokenbody["title"] = body["title"]
tokenbody["tokens"] = tokens
tokenbody.to_csv('all10ktokens.csv')

# 將全部文字都丟到一個txt檔案
f = open('allwords.txt', 'w', encoding='utf-8')
for i in words:
    f.write(i+' ')
f.close()

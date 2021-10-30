from nltk import FreqDist
import glob
import string
import regex as re
from nltk.corpus import stopwords


def decontracted(phrase):
    """ref: https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python/47091490#47091490"""

    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"won\’t", "will not", phrase)
    phrase = re.sub(r"can\’t", "can not", phrase)
    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    return phrase


stop = set(stopwords.words('English'))
txtname = glob.glob('*.txt')
txtname = list(txtname)
txtname.sort()
words = []
words1 = []
for idx in range(0, len(txtname), 10):
    group10 = txtname[idx:idx+10]
    for file in group10:
        f = open(file, 'r', encoding='utf-8')
        data = (f.read().lower())
        # word decontraction
        for w in data:
            decontracted(w)
        data = data.split(' ')
        for word in data:
            # removal punctuation and stopwords
            if word not in string.punctuation:
                words.append(word)
            if word not in stop and word not in string.punctuation:
                words1.append(word)
        f.close()

    fdist1 = FreqDist(words)
    fdist2 = FreqDist(words1)
    freqlist1 = list(fdist1.most_common())
    freqlist2 = list(fdist2.most_common())
    csvfilename = str(1+(idx)*100)+'-'+str((idx+len(group10))*100)
    print('Writing ', csvfilename, '....')
    title = "token freq"
    f1 = open(csvfilename+'.s', 'w', encoding='utf-8')
    f1.write(title+'\n')

    f2 = open(csvfilename+'.ns', 'w', encoding='utf-8')
    f2.write(title+'\n')

    # 本來想要用逗號的，但是發現數字裡面也有逗號
    for g in freqlist1:
        term, freq = g
        f1.write(str(term)+' '+str(freq)+'\n')
    f1.close()
    for g in freqlist2:
        term, freq = g
        f2.write(str(term)+' '+str(freq)+'\n')
    f2.close()

    # 清空
    words = []
    words1 = []

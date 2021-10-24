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
for idx in range(0, len(txtname), 5):
    group5 = txtname[idx:idx+5]
    for file in group5:
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
    csvfilename = str(1+(idx)*100)+'-'+str((idx+len(group5))*100)
    print('Writing ', csvfilename, '....')
    f1 = open(csvfilename+'.csv', 'w', encoding='utf-8')
    f2 = open('NoSTOP '+csvfilename+'.csv', 'w', encoding='utf-8')
    for g in freqlist1:
        term, freq = g
        f1.write(str(term)+','+str(freq)+'\n')
    f1.close()
    for g in freqlist2:
        term, freq = g
        f2.write(str(term)+','+str(freq)+'\n')
    f2.close()

    # 清空
    words = []
    words1 = []

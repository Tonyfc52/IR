import glob
import xml.etree.ElementTree as XET
from nltk import tokenize, word_tokenize


def simply(file):

    tree = XET.parse(file)
    root = tree.getroot()

    simplename = 'simple '+file.rstrip('.xml')+'.txt'
    f = open(simplename, 'w', encoding='utf-8')
    abstract = []
    for child in root.findall('.//Article'):
        papertitle = child.find('./ArticleTitle').text
        if papertitle == None:
            pass
        else:
            abstract.append(papertitle)
            sentence = []
            for grandchild in child.iter(tag='AbstractText'):
                sentence = ''.join(grandchild.itertext())
                abstract.append(sentence)
    for i in abstract:
        tokens = word_tokenize(i)
        for j in tokens:
            f.write(j+' ')

    f.close()


filenames = glob.glob('*.xml')
for file in filenames:
    print(file)
    simply(file)

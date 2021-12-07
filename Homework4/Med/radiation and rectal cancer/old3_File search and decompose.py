import glob
import xml.etree.ElementTree as XET
import pandas as pd


filenames = glob.glob('*.xml')
abstracttitle = []
abstract = []

for file in filenames:
    tree = XET.parse(file)
    root = tree.getroot()
    for child in root.findall('.//Article'):
        papertitle = child.find('./ArticleTitle').text
        if papertitle == None:
            pass
        else:
            abstracttitle.append(papertitle)
            sentence = ''
            allsent = ''
            for grandchild in child.iter(tag='AbstractText'):
                sentence = ''.join(grandchild.itertext())
                allsent += sentence+'\n'
            abstract.append(allsent)

result = pd.DataFrame({'title': abstracttitle, 'abstract': abstract})
result.to_excel('papers.xlsx')

# Import XML
import re
from typing import NoReturn
import xml.etree.ElementTree as XET

Abstra = []
tree = XET.parse('test2.xml')
root = tree.getroot()

# 尋找tag為ArticleTitle，為文章標題
for elem in tree.iter(tag='ArticleTitle'):
    PaperTitle = elem.text


# 尋找tag為AbstractText，因為文章的粗體字為label先判別是否存在而加入
# 列表為Abstra
labelnum = 0
for elem in tree.iter(tag='AbstractText'):
    if elem.attrib != {}:
        label = elem.attrib['Label']
        Abstra.append(label)
        labelnum += 1  # 標籤通常為大綱，不算句子，統計之後扣除

    # 因為內文中有上下標造成subelement，用
    # join忽略上下標直接接起來''為不加空格
    # itertext來忽略subelement，缺點：上下標格式消失(未解問題)
    Abstra.append(''.join(elem.itertext()))


#print('Paper Title:')
# print(PaperTitle)
# print("\n")
# print('Abstract:')
# print("\n")
# for section in Abstra:
#    print(section+"\n")


# 斷句分析，統計句數
NumofSentence = 0
# 將每一句個別放入list中
Pool = []

for section in Abstra:
    # 原文在https://newbedev.com/python-regex-for-splitting-text-into-sentences-sentence-tokenizing
    # 修改於https://regex101.com/r/nG1gU7/27
    m = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s", section)
    for i in m:
        print(i)
        print("\n")
        Pool.append(i)
        # 計算句數
        NumofSentence += 1
print('The number of sentences is ', (NumofSentence - labelnum))

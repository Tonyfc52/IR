# Import XML
import re
from typing import NoReturn
import xml.etree.ElementTree as XET

Abstra = []
tree = XET.parse('../test3.xml')
root = tree.getroot()

print (root.tag)
for child in root:
    print (child.tag, child.attrib)


for child in root.findall('.//Article'):
    papertitle = child.find('./ArticleTitle').text
    print(papertitle)
    for grandchild in child.iter(tag='AbstractText'):
        print(''.join(grandchild.itertext()))
    print ('\n')


    






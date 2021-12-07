from Bio import Entrez
import time

# About search and fetch technique, please refer to
# http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec143
# https://www.ncbi.nlm.nih.gov/books/NBK25500/?report=reader
# search term example = 'covid-19[Title/Abstract] AND 2021/01:2021/06[pdat]'

filename = 'pubmed search' + time.asctime()[0:13]+'.txt'

Entrez.email = ''  # 這邊要填email以示負責
handle = Entrez.esearch(
    db='pubmed', term='rectal and radiotherapy[Title/Abstract]', retstart=0, retmax=300, usehistory='y', sort='pubdate')
record = Entrez.read(handle)
print('Saving ~5000 PMID to ', filename)
output = open(filename, 'w')
for i in record['IdList']:
    output.write(i+'\n')
output.close()

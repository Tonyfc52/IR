#tf and idf
import pandas as pd
from collections import Counter

paratitle = pd.read_excel('allmed.xlsx')
parasource = pd.read_excel('para.xlsx')
paratoken = pd.read_pickle('para.pkl')
dfsource = pd.read_excel('df.xlsx')

dfindex = []
for i in range(len(dfsource)):
    temp = dfsource.iloc[i][3].split(' ')
    temp.pop(0)
    for j in range(len(temp)):
        temp[j] = int(temp[j])
    dfindex.append(temp)
dfsource['d_index'] = dfindex


def lookup(termlist):
    intersection = {i for i in range(len(parasource))}
    idf_dict = {}
    for term in termlist:
        try:
            i = (dfsource.index[dfsource['token'] == term])
            get_index = set(dfsource.iloc[i[0]][3])
            idf_dict[term] = dfsource.iloc[i[0]][2]

            intersection = get_index & intersection  # 取交集

        except:
            print('term:'+term+' is not exist!')
            intersection = {}
    return list(intersection), idf_dict


def counttf(query, parano):
    para_tfidf = []
    global idf_dict
    for numb in parano:
        get_token = paratoken.iloc[numb][0]
        total_count = (len(get_token))
        wordf = Counter(get_token)
        tf = 0
        tfidf = 0
        for item in query:
            tf += wordf[item] / total_count
            tfidf += idf_dict[item]*tf
        para_tfidf.append(tfidf)
    return para_tfidf


# Main Program
query = ['radiotherapy', 'recurrence']
result, idf_dict = lookup(query)
if result == []:
    print('No paragraphy can be found for your term(s)!')
else:
    print(result)
    result.sort()
    tf_idf = counttf(query, result)
    for i in range(len(result)):
        parano = result[i]
        print(parano, tf_idf[i])
        titleloc = parasource.iloc[parano][0]
        print(paratitle.iloc[titleloc][0])
        print(parasource.iloc[parano][1])
        print('\n')

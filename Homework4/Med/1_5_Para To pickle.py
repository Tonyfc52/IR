# To pickle
import pandas as pd


paras = pd.read_excel('nostop.xlsx')


para_flag = 0
paralist = []
list_temp1 = []
list_temp = []
for i in range(len(paras)):
    list_temp1 = paras.iloc[i][2].split(' ')
    list_temp1.pop(0)
    if paras.iloc[i][0] == para_flag:
        list_temp = list_temp + list_temp1
    else:
        para_flag += 1
        paralist.append(list_temp)
        list_temp = list_temp1
    if i == len(paras)-1:
        paralist.append(list_temp)


file = pd.DataFrame({'Paragraphs': paralist})
file.to_pickle('para.pkl')
file.to_excel('para_token.xlsx')

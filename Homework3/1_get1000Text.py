import pandas
import random


csvread = pandas.read_csv('.\origincsv\\all10k.csv')
num = 0
engpapers = pandas.DataFrame([{}, {}], columns=['title', 'abstract'])
serial = csvread.index
ran10000 = random.sample(set(serial), k=10000)
i = 0
while num < 1000:  # 這邊可以改想要取得的篇數，不超過5000篇(因為測試過很多非純英語或內文太短)
    location = ran10000[i]
    csvtitle = csvread.iat[location, 1]
    csvabstract = csvread.iat[location, 2]
    engdetect = str(csvtitle)+str(csvabstract)
    noeng = 0
    if str(csvabstract) == 'nan' or len(str(csvabstract).split(' ')) < 10:  # 內文太短或者是內容是空的都去掉
        pass

    else:
        for j in engdetect:
            if ord(j) > 128:
                noeng = 1
                break
            else:
                noeng = 0
        if noeng == 0:
            engpapers.loc[num] = [csvtitle, csvabstract]
            num += 1
    i += 1


engpapers.to_csv('1ktext.csv', index=False)

import json
import os


# 用UTF-8編碼打開.json檔案
with open('elonmusk.json', encoding='UTF-8') as f:
    content = json.load(f)
# print(content)
print(type(content))

def tweetsdisp(tweet):
    """try to display tweets in readable condition"""
    tweetobj = []
    tweetobj.append(tweet['user']['name'])
    tweetobj.append(tweet['user']['screen_name'])
    tweetobj.append(tweet['created_at'])
    tweetobj.append(tweet['text'])
    print('Username=',tweetobj[0])
    print('ScreenName=@'+tweetobj[1])
    print('Created at:',tweetobj[2])
    print('Text=',tweetobj[3])
    print ('\n')


#自動判別讀出來的檔案是 單一tweet(dict)，多重tweet(APIV2搜尋出來會有statuses這個字典，要解開)，或者是處裡過後內建多重tweet的list
if type(content) == dict:
    if 'search_metadata' in content:
        for sub in content['statuses']:
            tweetsdisp(sub)

    else:
        tweetsdisp(content)
    

if type(content) == list:
    for sub in content:
        subdict = dict(sub)
        tweetsdisp(subdict)






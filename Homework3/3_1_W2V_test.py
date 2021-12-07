from gensim import models
from gensim.models import Word2Vec


model = Word2Vec.load('w2vCBOW5k_w5v300e100.model')
model1 = Word2Vec.load('w2vSG5k_w5v300e100.model')


ans = ''
while True:
    ans = input('Key the word or \'bye\':')
    if ans == 'bye':
        break
    print('\n CBOW \n')
    try:
        for item in model.wv.most_similar(ans, topn=15):
            print(item)
        print('\n Skip Gram \n')
        for item1 in model1.wv.most_similar(ans, topn=15):
            print(item1)
    except:
        print('input error and quit!')
        break

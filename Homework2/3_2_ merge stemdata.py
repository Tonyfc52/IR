import pandas as pd

stemfreq = pd.read_csv('list_of_stemwords.csv')
stemform = pd.read_csv('list_to_stemwords.csv')
newform = stemfreq.merge(stemform, on='stemword')

# combined together
newform.to_csv('analysis.csv', index=False)

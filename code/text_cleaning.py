import pandas as pd
import regex
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords

dataframe = pd.read_csv(r'C:\Users\14057\Documents\PYTHON\Online Food Industry\CLEANED DATA\cleaned_data.csv')
# Removing null reviews
dataframe1 = dataframe.dropna()
# convert reviews to lower case
dataframe1['Reviews'] = dataframe1['Reviews'].apply(lambda x: " ".join(x.lower() for x in x.split()))
# Remove stop words
stop = stopwords.words('english')
dataframe1['Reviews'] = dataframe1['Reviews'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
# Remove punctuation marks
patternpunc = '[^\w\s]'
dataframe1['Reviews'] = dataframe1['Reviews'].str.replace(patternpunc, '')
# Remove numeric values as appropriate
patterndigits = '.*[0-9]+.*'
dataframe1['Reviews'] = dataframe1['Reviews'].str.replace(patterndigits, '')
# Remove white space characters such as \t, \n
whitespace = '\\t\\n'
dataframe1['Reviews'] = dataframe1['Reviews'].str.replace(whitespace, '')
dataframe1.to_csv(r'C:\Users\14057\Documents\PYTHON\Online Food Industry\CLEANED DATA\cleaned_data3.csv', sep=',', index=False)

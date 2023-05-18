import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer, PorterStemmer

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, plot_confusion_matrix

plot_size = plt.rcParams["figure.figsize"]
plot_size[0] = 8
plot_size[1] = 6
plt.rcParams["figure.figsize"] = plot_size

dataframe = pd.read_csv(r'C:\Users\14057\Documents\PYTHON\Online Food Industry\CLEANED DATA\cleaned_data3.csv')
dataframe = dataframe[dataframe['Reviews'].notnull()]
print(dataframe['Reviews'])

# Stemming the reviews
porstem = PorterStemmer()
dataframe['Reviews'] = dataframe['Reviews'].apply(lambda x: " ".join([porstem.stem(word) for word in x.split()]))

# creating document term matrix for the reviews
vectorizer = CountVectorizer()
tokens_data = pd.DataFrame(vectorizer.fit_transform(dataframe['Reviews']).toarray(), columns=vectorizer.get_feature_names())
print(tokens_data.columns.tolist())

sort_text = tokens_data.sum()
sort_text_output = sort_text.sort_values(ascending=False).head(50)
print(sort_text_output)

# Generating topics
vectorizer = CountVectorizer(max_df=0.8, min_df=4, stop_words='english')
doc_term_matrix = vectorizer.fit_transform(dataframe['Reviews'].values.astype('U'))
review_values = dataframe['Reviews'].values.astype('U')
doc_term_matrix = vectorizer.fit_transform(review_values)
print(doc_term_matrix.shape)
LDA = LatentDirichletAllocation(n_components=5, random_state=35)
LDA.fit(doc_term_matrix)
first_topic = LDA.components_[0]
top_topic_words = first_topic.argsort()[-10:]


for i, topic in enumerate(LDA.components_):
    print(f'Top 10 words for topic #{i}:')
    print([vectorizer.get_feature_names()[i] for i in topic.argsort()[-10:]])
    print('\n')


# Adding a new column to a dataframe
topic_values = LDA.transform(doc_term_matrix)
dataframe['topic'] = topic_values.argmax(axis=1)
print(dataframe.head())

# Non-Negative Matrix Factorization
tfidf_vect = TfidfVectorizer(max_df=0.8, min_df=5, stop_words='english')
doc_term_matrix2 = tfidf_vect.fit_transform(dataframe['Reviews'].values.astype('U'))
nmf = NMF(n_components=5, random_state=42)
nmf.fit(doc_term_matrix2)
first_topic = nmf.components_[0]
top_topic_words = first_topic.argsort()[-10:]
for i, topic in enumerate(nmf.components_):
    print(f'Top 10 words for topic #{i}:')
    print([tfidf_vect.get_feature_names()[i] for i in topic.argsort()[-10:]])
    print('\n')

# Adding a new column for negative topic values
topic_values2 = nmf.transform(doc_term_matrix2)
dataframe['topic2'] = topic_values2.argmax(axis=1)
dataframe.head()

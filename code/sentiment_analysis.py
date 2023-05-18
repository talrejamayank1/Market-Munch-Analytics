import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, plot_confusion_matrix

plot_size = plt.rcParams["figure.figsize"]
plot_size[0] = 8
plot_size[1] = 6
plt.rcParams["figure.figsize"] = plot_size

dataframe = pd.read_csv(r'C:\Users\14057\Documents\PYTHON\Online Food Industry\CLEANED DATA\sentiments.csv')
dataframe2 = pd.read_csv(r'C:\Users\14057\Documents\PYTHON\Online Food Industry\CLEANED DATA\cleaned_data3.csv')

# Percentage of each sentiment type overall
dataframe.sentiment.value_counts().plot(kind='pie', autopct='%1.0f%%', colors=["green", "red"])
plt.show()

# distribution of sentiment by airline
reviews_sentiment = dataframe.groupby([dataframe2['Source'], 'sentiment']).sentiment.count().unstack()
reviews_sentiment.plot(kind='bar')
plt.show()

features = dataframe['word']
vectorizer = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8, stop_words='english')
processed_features = vectorizer.fit_transform(features.values.astype('U')).toarray()
labels = dataframe['sentiment']
X_train, X_test, y_train, y_test = train_test_split(processed_features, labels, test_size=0.2, random_state=0)
text_classifier = RandomForestClassifier(n_estimators=200, random_state=0)
text_classifier.fit(X_train, y_train)
predictions = text_classifier.predict(X_test)
cm = confusion_matrix(y_test, predictions)
print(cm)
plot_confusion_matrix(text_classifier, X_test, y_test)
plt.show()
print(classification_report(y_test, predictions))

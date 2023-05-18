import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from wordcloud import WordCloud, STOPWORDS
import numpy as npy
from PIL import Image
import nltk
from nltk.stem import PorterStemmer

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

from nltk import word_tokenize, pos_tag, ne_chunk
textbank = ""
dataframe = pd.read_csv(r'C:\Users\14057\Documents\PYTHON\Online Food Industry\CLEANED DATA\cleaned_data3.csv')
for value in dataframe['Reviews']:
    textbank = textbank + " " + str(value)
print(textbank)

# Obtain the POS tags for nouns and generate a frequency plot
post1 = pos_tag(word_tokenize(textbank))
tree1 = ne_chunk(post1)
entitydesc = []
for x in str(tree1).split('\n'):
    if '/NN' in x:
        entitydesc.append(x)
print(entitydesc)
noun_df = pd.DataFrame(entitydesc)
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots()
noun_df[0:19].value_counts().plot(ax=ax, kind='bar', xlabel='Nouns', ylabel='Frequency')
plt.show()

entityAdverb = []
for x in str(tree1).split('\n'):
    if '/RB' in x:
        entityAdverb.append(x)
print(entityAdverb)
adverb_df = pd.DataFrame(entityAdverb)
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots()
adverb_df[0:19].value_counts().plot(ax=ax, kind='bar', xlabel='Adverbs', ylabel='Frequency')
plt.show()

# Extract the entities for people, organizations, and locations
entityp = []
entityo = []
entityg = []
for x in str(tree1).split('\n'):
    if 'PERSON' in x:
        entityp.append(x)
    elif 'ORGANIZATION' in x:
        entityo.append(x)
    elif 'GPE' in x or 'GSP' in x:
        entityg.append(x)
print(entityp)
print(entityo)
print(entityg)


# Frequency plot for organizations
orgs = pd.DataFrame(entityo)
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots()
orgs[0:14].value_counts().plot(ax=ax, kind='bar', xlabel='Organizations', ylabel='Frequency')
plt.show()


def plot_cloud(wordcloud):
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud)
    plt.show()
    plt.axis("off")


# Generate a word cloud for top 15 nouns
nounString = entitydesc[0:14]
nounString = ' '.join(nounString)
wordcloud = WordCloud(width= 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(nounString)
plot_cloud(wordcloud)

# Generate a word cloud for top 15 organisations
orgString = entityo[0:14]
orgString = ' '.join(orgString)
wordcloud = WordCloud(width=3000, height=2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords=STOPWORDS).generate(orgString)
plot_cloud(wordcloud)

# Generate a word cloud for top 15 adverbs
adverbsString = entityAdverb[0:14]
adverbsString = ' '.join(adverbsString)
wordcloud = WordCloud(width=3000, height=2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords=STOPWORDS).generate(adverbsString)
plot_cloud(wordcloud)

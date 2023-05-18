import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.stats as sts

# Modifying pandas default max columns and max rows size
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.width = None

# Reading reviews data file
os.chdir(r'C:\Users\14057\Documents\SPRING 2022\DATA SCIENCE PROGRAMMING AND ANALYTICS II\PROJECT\msis-5223-deliverable-1-nsms\data')
os.getcwd()
reviews_data = pd.read_table('scraped_data.txt')

# Converting 'object' data type to 'categorical' data type
reviews_data['Name'] = reviews_data['Name'].astype('category')
reviews_data['Reviews'] = reviews_data['Reviews'].astype('category')
reviews_data['PriceRange'] = reviews_data['PriceRange'].astype('category')
reviews_data['Cuisine'] = reviews_data['Cuisine'].astype('category')
reviews_data['Location'] = reviews_data['Location'].astype('category')
reviews_data['PaymentType'] = reviews_data['PaymentType'].astype('category')
reviews_data['Source'] = reviews_data['Source'].astype('category')

# Performing summary statistics of numerical and categorical data
print(reviews_data.columns)
print('\n\nNUMERICAL COLUMNS\n', reviews_data.describe(include=['number']))
print('\n\nCATEGORICAL COLUMNS\n', reviews_data.describe(include=['category']))
print(reviews_data.shape)
print(reviews_data.median(numeric_only=True))

# Performing skewness and kurtosis of data
print("\n\nKURTOSIS\n", reviews_data.kurt())
print("\n\nSKEWNESS\n", reviews_data.skew())

#Creating scatter plots between different variables
reviews_data.plot.scatter(x='DeliveryFees', y='DeliveryTime')
plt.show()
reviews_data.plot.scatter(x='DeliveryFees', y='Distance')
plt.show()
reviews_data.plot.scatter(x='PriceRange', y='Rating')
plt.show()
reviews_data.plot.scatter(x='DeliveryTime', y='Distance')
plt.show()

#Creating boxplot for the data
reviews_data.boxplot()
plt.show()
reviews_data.loc[:, ['Rating']].boxplot()
plt.show()
reviews_data.loc[:, ['DeliveryFees']].boxplot()
plt.show()
reviews_data.loc[:, ['DeliveryTime']].boxplot()
plt.show()
reviews_data.loc[:, ['Distance']].boxplot()
plt.show()

#Creating Histograms
reviews_data.Rating.value_counts().plot.barh()
plt.show()
reviews_data.PriceRange.value_counts().plot.barh()
plt.show()

# QQ Plots
sts.probplot(reviews_data.Rating, dist="norm", plot=plt)
plt.show()
sts.probplot(reviews_data.Distance, dist="norm", plot=plt)
plt.show()
sts.probplot(reviews_data.DeliveryFees, dist="norm", plot=plt)
plt.show()
sts.probplot(reviews_data.DeliveryTime, dist="norm", plot=plt)
plt.show()

# co occurrence plots of reviews
reviews = reviews_data['Reviews'].as_matrix()

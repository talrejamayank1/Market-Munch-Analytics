from operator import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn import metrics
#Neural Network
from sklearn.neural_network import MLPRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
#Multiple Regression
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf


rating_data = pd.read_csv('scraped_data.csv', index_col=0)
print(rating_data.columns)
rating_data = rating_data[['Name', 'Rating', 'Reviews', 'PriceRange', 'DeliveryFees',
       'DeliveryTime', 'Cuisine', 'Zipcode', 'Location', 'PaymentType',
       'Distance', 'Source', 'Revenue']]
rating_sub = rating_data[['DeliveryFees', 'DeliveryTime', 'Zipcode', 'Distance', 'Revenue']]
rating_data_train, rating_data_test, y_train, y_test = train_test_split(rating_sub, 
                                                                      rating_data.Rating, 
                                                                      test_size=0.3)

# Standardize the scaling of the variables by
# computing the mean and std to be used for later scaling.


# scaler = preprocessing.StandardScaler()
# scaler.fit(rating_data_train)

# # Perform the standardization process
# rating_data_train_std = scaler.transform(rating_data_train)
# rating_data_test_std = scaler.transform(rating_data_test)

# rating_reg = MLPRegressor(activation='relu', solver='sgd', 
#                       early_stopping=True)
# rating_reg.fit(rating_data_train_std, y_train)

# rating_pred = rating_reg.predict(rating_data_test_std)

# # print(rating_pred)

# print("\nMean Absolute Error\n", metrics.mean_absolute_error(y_test, rating_pred))

# print("Mean Squared Error\n", metrics.mean_squared_error(y_test, rating_pred))

# print("Score\n", metrics.r2_score(y_test, rating_pred))

rating_class_sub = rating_data[['Rating', 'DeliveryFees', 'DeliveryTime', 'Zipcode', 'Distance', 'Revenue']]

rating_class_data_train, rating_class_data_test, rating_class_train, rating_class_test = train_test_split(rating_class_sub, 
                                                                              rating_data.PriceRange, 
                                                                              test_size=0.20)

# Standardize the scaling of the variables by
# computing the mean and std to be used for later scaling.
scaler = preprocessing.StandardScaler()
scaler.fit(rating_class_data_train)

# Perform the standardization process
rating_class_data_train_std = scaler.transform(rating_class_data_train)
rating_class_data_test_std = scaler.transform(rating_class_data_test)

nnclass2 = MLPClassifier(activation='relu', solver='sgd',
                         hidden_layer_sizes=(100,100))
nnclass2.fit(rating_class_data_train_std, rating_class_train)

nnclass2_pred = nnclass2.predict(rating_class_data_test_std)

cm = metrics.confusion_matrix(rating_class_test, nnclass2_pred)
print("\n\nConfusion Matrix\n")
print(cm, "\n\n")

plt.matshow(cm)
plt.title('Confusion Matrix')
plt.xlabel('Actual Value')
plt.ylabel('Predicted Value')
plt.xticks([0,1,2,3], ['Low','Medium', 'Expensive','VeryExpensive'])
plt.show()
print("\n\nClassification Report\n", metrics.classification_report(rating_class_test, nnclass2_pred))


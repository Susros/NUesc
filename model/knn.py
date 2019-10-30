""" KNN Model

This script train KNN model using the best parameters
obtained from Grid Search.

Author: Kelvin Yin
"""

from __future__ import print_function

import os
import sys
import matplotlib.pyplot as plt
import numpy
import sklearn

from six.moves import cPickle, range
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

# Output Directory
OUTPUT_DIR = 'output/'

# Metric Parameter
METRIC = 'manhattan'

# K Parmeter
K = 1

# Load MFCC Data Frame
try:
    mfcc_dataframe = cPickle.load(open(OUTPUT_DIR + 'mfcc_feature.p', 'rb'))
except IOError:
    print("Could not load MFCC Data Frame. Please make sure to extract features first.")

# Map label name with label id
labels = []
for label_id in set(mfcc_dataframe['label_id']):
	labels.append((label_id, set(mfcc_dataframe.loc[mfcc_dataframe['label_id'] == label_id]['label'])))


# Get training data and label
train_data = numpy.array(list(mfcc_dataframe.loc[mfcc_dataframe['fold'] < 9]['sample']))
train_label = numpy.array(mfcc_dataframe.loc[mfcc_dataframe['fold'] < 9]['label_id'])

# Get validation data and label
validation_data = numpy.array(list(mfcc_dataframe.loc[mfcc_dataframe['fold'] == 9]['sample']))
validation_label = numpy.array(mfcc_dataframe.loc[mfcc_dataframe['fold'] == 9]['label_id'])

''' Train KNN '''

scores = []

knn = KNeighborsClassifier(n_neighbors = K, metric = METRIC)

print("Training KNN Model ")
print("=========================")

# 10-Fold Cross Validation
val_index = 10
for n_fold in range(1, 11):
    print("Validation Fold: ", val_index)

    # Get training data and label
    train_data = numpy.array(list(mfcc_dataframe.loc[mfcc_dataframe['fold'] != val_index]['sample']))
    train_label = numpy.array(mfcc_dataframe.loc[mfcc_dataframe['fold'] != val_index]['label_id'])

    # Get validation data and label
    validation_data = numpy.array(list(mfcc_dataframe.loc[mfcc_dataframe['fold'] == val_index]['sample']))
    validation_label = numpy.array(mfcc_dataframe.loc[mfcc_dataframe['fold'] == val_index]['label_id'])

    knn_model = knn.fit(train_data, train_label)
    knn_prediction = knn_model.predict(validation_data)
    acc = metrics.accuracy_score(validation_label, knn_prediction)
    scores.append(acc)

    print("Accuracy: ", acc)
    print("")

    val_index -= 1

print("KNN Training Completed")

print()

print("Scores: ")
for i in scores:
	print (i)

pickle.dump(knn, open(OUTPUT_DIR + "knn_model.p", 'wb'))

print()
print("KNN Model has been saved to '"+ OUTPUT_DIR +"'")
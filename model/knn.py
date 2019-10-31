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
import pickle

from six.moves import cPickle, range
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

# Output Directory
OUTPUT_DIR = 'output/'

# Metric Parameter
METRIC = 'manhattan'

# K Parmeter
K = 6

# Load MFCC Data Frame
try:
    mfcc_dataframe = cPickle.load(open(OUTPUT_DIR + 'mfcc_feature.p', 'rb'))
except IOError:
    print("Could not load MFCC Data Frame. Please make sure to extract features first.")
    sys.exit(1)

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

#####################################################

''' Plot confusion matrix '''

matrix = confusion_matrix(validation_label, knn_prediction)

classes = [
	'Air Conditioner',
	'Car Horn',
	'Children Playing',
	'Dog Bark',
	'Drilling',
	'Engine Idling',
	'Gun Shot',
	'Jackhammer',
	'Siren',
	'Street Music'
]

# Normalise matrix
matrix = matrix.astype('float') / matrix.sum(axis = 1)[:, numpy.newaxis]

# Configure figure
fig, ax = plt.subplots()
im = ax.imshow(matrix, interpolation = 'nearest', cmap = plt.cm.Blues)
ax.figure.colorbar(im, ax = ax)
ax.set(xticks = numpy.arange(matrix.shape[1]),
	   yticks = numpy.arange(matrix.shape[0]),
	   xticklabels = classes, yticklabels = classes,
	   title = 'KNN Classification Confusion Matrix',
	   ylabel = 'True Label',
	   xlabel = 'Predicted Label')

plt.setp(ax.get_xticklabels(), rotation = 45, ha = 'right', rotation_mode = 'anchor')

thresh = matrix.max() / 2
for i in range(matrix.shape[0]):
	for j in range(matrix.shape[1]):
		ax.text(j, i, format(matrix[i, j], '.2f'),
				ha = 'center', va = 'center',
				color = 'white' if matrix[i, j] > thresh else 'black')

fig.tight_layout()

plt.show()
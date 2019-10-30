""" Grid Search for KNN

This script perform Grid Search for SVM Model.

Features of sounds need to be extracted first before running this script. It loads MFCC dataframe from
mfcc_feature.p

The Grid Search is performed with K values from 1 to 50 and following metric:

    * Euclidean
    * Manhattan
    * Chebyshev

For each parameter, it performs 10-fold cross validation for all 10 folders of the sound dataset.

Autor: Kelvin Yin
"""

from __future__ import print_function

import os
import sys
import numpy
import sklearn
import pickle

from six.moves import cPickle, range
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

# Output directory
OUTPUT = 'output/'

# Import MFCC Data Frame
try:
    mfcc_dataframe = cPickle.load(open(OUTPUT + 'mfcc_feature.p', 'rb'))
except IOError:
    print("Could not load MFCC Data Frame. Please make sure to extract features first.")

# Map label name with label id
labels = []
for label_id in set(mfcc_dataframe['label_id']):
	labels.append((label_id, set(mfcc_dataframe.loc[mfcc_dataframe['label_id'] == label_id]['label'])))

# Grid Search parameters
param_K = range(1, 51)
param_metric = ["euclidean", "manhattan", "chebyshev"]

grid_accuracy = []

# Run for three metric
for metric in param_metric:
    
    # Store accuracy by matric.
    metric_accuracy = []

    for k in param_K:

        print("Grid Search for K = " + str(k) + " and metric = " + metric)
        print("========================================")

        # KNN
        knn = KNeighborsClassifier(n_neighbors = k, metric = metric)

        # Score for cross validation
        scores = []

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
        
        # Get average score
        avg_score = 0
        for score in scores:
            avg_score += score
        
        avg_score = avg_score / len(scores)

        metric_accuracy.append(avg_score)

        print("Grid Search Result")
        print("===================================")
        print("K = ", k)
        print("Metric = ", metric)
        print("Accuracy = ", avg_score)

        print()
        print(">>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print()

    grid_accuracy.append(metric_accuracy)


# Save grid accuracy
with open("knn_gridsearch.p", "wb") as fp:
    pickle.dump(grid_accuracy, fp)

print("Grid search completed.")
print()

print("Result")
print("==========================")

for i in range(3):
    for k in param_K:
        print("Metric = ", param_metric[i])
        print("K = ", k)
        print("Accuracy = ", grid_accuracy[i][k - 1])
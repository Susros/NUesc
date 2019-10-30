""" Grid Search for SVM Model

This script perform Grid Search for SVM Model.

Features of sounds need to be extracted first before running this script. It loads MFCC dataframe from
mfcc_feature.p

The Grid Search is performed with the following 13 C and gamma parameters:

    * C = {1e-4, 1e-3, 1e-2, 1e-1, 1.0, 1e+1, 1e+2, 1e+3, 1e+4, 1e+5, 1e+6, 1e+7, 1e+8}
    * gamma = {1e-11, 1e-10, 1e-09, 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 1e-02, 1e-01, 1.0, 10.0}

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
from sklearn.svm import SVC

# Output Directory
OUTPUT_DIR = 'output/'

# Import MFCC dataframe
try:
    mfcc_dataframe = cPickle.load(open(OUTPUT_DIR + 'mfcc_feature.p', 'rb'))
except IOError:
    print("Could not load MFCC Data Frame. Please make sure to extract features before running this script.")

# Map label name with label id
labels = []
for label_id in set(mfcc_dataframe['label_id']):
	labels.append((label_id, set(mfcc_dataframe.loc[mfcc_dataframe['label_id'] == label_id]['label'])))

# Grid search parameters
param_C = [1e-04, 1e-03, 1e-02, 1e-01, 1.0, 1e+01, 1e+02, 1e+03, 1e+04, 1e+05, 1e+06, 1e+07, 1e+08]
param_gamma = [1e-11, 1e-10, 1e-09, 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 1e-02, 1e-01, 1.0, 10.0]

# To store Grid Search accuracy
grid_accuracy = []

''' Start Grid Search '''
for C in param_C:
    for gamma in param_gamma:
        
        print("Grid Search for C = " + str(C) + " and gamma = " + str(gamma))
        print("============================================= ")

        # To store accuracy score for cross validation
        scores = []

        # SVM
        svm = SVC(C=C, gamma=gamma, kernel='rbf', decision_function_shape='ovr')

        # Cross validation
        val_index = 10
        for n_fold in range(1, 11):
            print("Validation Fold: ", val_index)

            train_data = numpy.array(list(mfcc_dataframe.loc[mfcc_dataframe['fold'] != val_index]['sample']))
            train_label = numpy.array(mfcc_dataframe.loc[mfcc_dataframe['fold'] != val_index]['label_id'])

            validation_data = numpy.array(list(mfcc_dataframe.loc[mfcc_dataframe['fold'] == val_index]['sample']))
            validation_label = numpy.array(mfcc_dataframe.loc[mfcc_dataframe['fold'] == val_index]['label_id'])

            svm_model = svm.fit(train_data, train_label)

            svc_prediction = svm_model.predict(validation_data)

            svc_accuracy = numpy.sum(svc_prediction == validation_label) / validation_label.shape[0]
            scores.append(svc_accuracy)

            print("Accuracy: ", svc_accuracy)
            print("")

            val_index -= 1

        # Get average accuracy
        avg_score = 0
        for score in scores:
            avg_score += score
        
        avg_score = avg_score/len(scores)

        grid_accuracy.append(avg_score)

        print("Grid Search Result")
        print("============================")
        print("C        = ", C)
        print("gamma    = ", gamma)
        print("Accuracy = ", avg_score)

        print()
        print(">>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print()

# Save grid accuracy
with open(OUTPUT_DIR + "svm_gridsearch.p", "wb") as fp:
    pickle.dump(grid_accuracy, fp)

print("Grid search completed.")
print("")

print("Result")
print("======================")

result_index = 0

for C in param_C:
    for gamma in param_gamma:
        print("C = ", C)
        print("Gamma = ", gamma)
        print("Accuracy = ", grid_accuracy[result_index])
        result_index += 1

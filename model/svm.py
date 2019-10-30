""" SVM Model

Train SVM model using the best parameters obtained
from Grid Search.

Autor: Kelvin Yin
"""

from __future__ import print_function

import os
import sys
import matplotlib.pyplot as plt
import numpy
import sklearn
import pickle

from six.moves import cPickle, range
from sklearn.svm import SVC

# Output directory
OUTPUT_DIR = 'output/'

# C Parameter
C = 1000

# Gamma Parameter
GAMMA = 1e-06

# Load MFCC Data Frame
try:
    mfcc_dataframe = cPickle.load(open(OUTPUT_DIR + 'mfcc_feature.p', 'rb'))
except IOError:
    print("Could not load MFCC Data Frame. Please make sure to extract features first.")

# Map label name with label id
labels = []
for label_id in set(mfcc_dataframe['label_id']):
	labels.append((label_id, set(mfcc_dataframe.loc[mfcc_dataframe['label_id'] == label_id]['label'])))

# To store prediction score
scores = []

svm = SVC(C = C, gamma = GAMMA, kernel = 'rbf', decision_function_shape = 'ovr')

''' Train SVM with 10-fold cross validation '''

print("Training SVM Model ")
print("=========================")

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

print("SVM Training Completed.")
print()

print("Scores: ")
for i in scores:
	print (i)

pickle.dump(svm, open(OUTPUT_DIR + "svm_model.p", 'wb'))

print()
print("SVM Model has been saved to '"+ OUTPUT_DIR +"'")
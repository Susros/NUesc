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
from sklearn.metrix import confusion_matrix

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

#####################################################

''' Plot confusion matrix '''

matrix = confusion_matrix(validation_label, svc_prediction)

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
im = ax.imgshow(matrix, interpolation = 'nearest', cmap = plt.cm.Blues)
ax.figure.colorbar(im, ax = ax)
ax.set(xticks = numpy.arange(matrix.shape[1]),
	   yticks = numpy.arange(matrix.shape[0]),
	   xticklabels = classes, yticklabels = classes,
	   title = 'SVM Classification Confusion Matrix',
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
""" Feature Extraction

This script extract features from UrbanSound8K 
sound dataset.

UrbanSound8K dataset must be in dataset folder.

Author: Kelvin Yin
"""

import sys
import numpy
import pandas
import sklearn
import librosa
import soundfile

from os import listdir
from os.path import isfile, join
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from six.moves import cPickle, range

print("Feature Extraction")
print("=========================")
print("")

# Dataset directory
DATASET_DIR = 'dataset/UrbanSound8K/'

# Output directory
OUTPUT_DIR = 'output/'

# Get meta data from sound dataset
sound_metadata = pandas.read_csv(DATASET_DIR + 'metadata/UrbanSound8K.csv')

# Get list of folder from sound dataset
# There are 10 folder, naming fold1 ... fold10
fold_list = ['fold' + str(i) for i in range(1, 11)]

# To store mfcc data
mfcc_data = []

''' Extract features from all 10 folders '''
for i in range(10):

    # Folder path
    fold_path = DATASET_DIR + 'audio/' + fold_list[i] + '/'

    # Get all sound files from each folder
    sound_files = [fold_path + f for f in listdir(fold_path) if isfile(join(fold_path, f))]

    for sound_file in sound_files:
        try:

            print("Extracting features from " + sound_file + " ...")

            # Load sound file
            y, sr = librosa.load(sound_file)

            # Compute Short-time Fourier Transform
            stft = numpy.abs(librosa.stft(y))

            # Compute MFCCs
            mfccs = numpy.mean(librosa.feature.mfcc(y = y, sr = sr, n_mfcc = 40).T, axis = 0)

            # Compute a chromagram from a waveform or power spectrogram
            chroma = numpy.mean(librosa.feature.chroma_stft(S = stft, sr = sr).T, axis = 0)
			
            # Compute a mel-scaled spectrogram
            mel = numpy.mean(librosa.feature.melspectrogram(y = y, sr = sr).T, axis = 0)

            # Compute spectral contrast
            contrast = numpy.mean(librosa.feature.spectral_contrast(S = stft, sr = sr).T, axis = 0)

            # Computes the tonal centroid features
            tonnetz = numpy.mean(librosa.feature.tonnetz(y = librosa.effects.harmonic(y), sr = sr).T, axis = 0)

			# 193 Features
            features = numpy.vstack([numpy.empty((0, 193)), numpy.hstack([mfccs, chroma, mel, contrast, tonnetz])])

        except:
            print("Exception: Cound not extract '" + sound_file + "'")
            continue

        # Get label
        label_row = sound_metadata.loc[sound_metadata['slice_file_name'] == sound_file.split('/')[-1]].values.tolist()
        label = label_row[0][-1]
		
		# Folder number
        fold = i + 1

		# Add it to mfcc data
        mfcc_data.append([features, features.shape, label, fold])

# Construct MFCC Data Frame
mfcc_dataframe = pandas.DataFrame(data = mfcc_data, columns = ["features", "shape", "label", "fold"])

# Convert Label to class number
label_encoder = LabelEncoder()
label_num = label_encoder.fit_transform(mfcc_dataframe["label"])

# One hot encode
one_hot_encoder = OneHotEncoder()
one_hot = one_hot_encoder.fit_transform(label_num.reshape(-1, 1))

for i in range(10):
	mfcc_dataframe[label_encoder.classes_[i]] = one_hot[:, i].toarray()

# Add sample into MFCC Data Frame
mfcc_dataframe['sample'] = pandas.Series([mfcc_dataframe['features'][i].ravel() for i in range(mfcc_dataframe.shape[0])], index = mfcc_dataframe.index)

# Remove features from MFCC Data Frame
del mfcc_dataframe['features']

# Add Label ID into MFCC Data Frame
mfcc_dataframe['label_id'] = label_num

print("Exporting MFCC features ...")

# Export it
cPickle.dump(mfcc_dataframe, open(OUTPUT_DIR + 'mfcc_feature.p', 'wb'))

print("MFCC Features have been saved: '" + OUTPUT_DIR + " mfcc_feature.p'")
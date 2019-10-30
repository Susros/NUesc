""" Run Pi

Record sound and predict the events based on UrbanSound8K classes.

Author: Kelvin Yin
"""

import sys
import numpy
import pandas
import sklearn
import librosa
import pyaudio
import wave
import pickle
import time
import pixels

# Load SVM Model
try:
    SVM = pickle.load(open('svm_model.p', 'rb'))
except IOError:
    print("SVM Model could not be loaded.")
    sys.exit(1)

# Set ReSpeaker recording config
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 2
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = 2
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = 'output.wav'

# Start PyAudio
p = pyaudio.PyAudio()

# Get seeed 2-mic voice card. Default is 2.
for i in range(0, p.get_host_api_info_by_index(0).get('deviceCount')):
    info = p.get_device_info_by_host_api_device_index(0, i)

    if (info.get('maxInputChannels') > 0 and 'seeed-2mic-voicecard' in info.get('name')):
        RESPEAKER_INDEX = i

# UrbanSound8K Classes
sound_class = [
    'Air Conditioner',      # 0
    'Car Horn',             # 1
    'Children Playing',     # 2
    'Dog Bark',             # 3
    'Drilling',             # 4
    'Engine Idling',        # 5
    'Gun Shot',             # 6
    'Jackhammer',           # 7
    'Siren',                # 8
    'Street Music'          # 9
]

# Sound to detct for LED to light up
TO_DETECT = 3

while(True):

    ''' Start Recording '''

    print()
    print("Recording ...")
    
    stream = p.open(
        rate = RESPEAKER_RATE,
        format = p.get_format_from_width(RESPEAKER_WIDTH),
        channels = RESPEAKER_CHANNELS,
        input = True,
        input_device_index = RESPEAKER_INDEX
    )

    frames = []

    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop stream
    stream.stop_stream()
    stream.close()

    # Save sound file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Done Recording !")

    #############################

    ''' Extract features from recorded sound '''

    print()
    print("Extracting MFCC Features...")

    y, sr = librosa.load(WAVE_OUTPUT_FILENAME)
    stft = numpy.abs(librosa.stft(y))
    mfccs = numpy.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    chroma = numpy.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T, axis=0)
    mel = numpy.mean(librosa.feature.melspectrogram(y, sr=sr).T, axis=0)
    contrast = numpy.mean(librosa.feature.spectral_contrast(S=stft, sr=sr).T, axis=0)
    tonnetz = numpy.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)

    features = numpy.vstack([numpy.empty((0, 193)), numpy.hstack([mfccs, chroma, mel, contrast, tonnetz])])

    # Get sample from features
    sample = [features[i].ravel() for i in range(features.shape[0])]

    print("MFCC features extracted !")

    #############################

    ''' Predict the sound event'''

    pred = SVM.predict(numpy.array(list(sample)))

    print()
    print("Detected: ", sound_class[pred[0]])

    # Do the LED thing
    if (pred[0] == TO_DETECT):
        led = pixels.Pixels()
        led.wakeup()
        led.think()
        time.sleep(3)
        led.off()
    else:
        time.sleep(3)

""" Start Pi

Pi listen to the the server for command and send signal
when the sound is detected.

Sound to listen can be set from cloud server.

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
import socketio

# Get server address for socket
SERVER_URL = 'http://localhost:8080'

if (len(sys.argv) == 2):
    SERVER_URL = sys.argv[1]

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

# Initialise socket io client
sio = socketio.Client()

# Conenct to server
sio.connect(SERVER_URL)

# Sound to detct for LED to light up
TO_DETECT = 0

# Flag to start recording
START = False

# Get what sound to listen from server
@sio.event
def pi_setsound(sound_id):
    global TO_DETECT
    global START

    TO_DETECT = int(sound_id)
    START = True

while(True):
    if (START) :

        # Let server know what it's listening to
        sio.emit('pi_status', 'Listening to ' + sound_class[TO_DETECT])

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

        # Let Server know it detected
        if (pred[0] == TO_DETECT):
            sio.emit('pi_detected', str(TO_DETECT))

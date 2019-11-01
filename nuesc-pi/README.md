# Sound Classifier in Pi

The Respberry Pi records a sound and predict the event using the trained machine learning model. The Pi communicates with cloud server to send the message when the sound is detected. That particular sound can be set from cloud using web application.

## Requirement

The following hardwares are required:

* Raspberry Pi 3
* ReSpeaker 2-Mics Pi HAT

The following python packages are required:

* numpy
* pandas
* sklearn
* librosa
* pyaudio
* wave
* pickle
* socketio

## Usage

Before running the py, server has too be running first. Then, run the following command:

``` console
python3 start.py http[s]://[IP_ADDRESS]:[PORT]
```

`start.py` accept one parameter argument for server address. 
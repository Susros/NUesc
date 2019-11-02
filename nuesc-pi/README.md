# Sound Classifier in Pi

The Respberry Pi records a sound and predicts the event using the trained machine learning model. The Pi communicates with cloud server to send the message when the sound is detected. That particular sound can be set from cloud using web application.

## Requirement

The following hardwares are required:

* Raspberry Pi 3
* ReSpeaker 2-Mics Pi HAT

The following python packages are required:

* __numpy__ *(pip3 install numpy)*
* __pandas__ *(pip3 install pandas)*
* __sklearn__ *(pip3 install sklearn)*
* __librosa__ *(pip3 install librosa)*
* __pyaudio__ *(pip3 install pyaudio)*
* __wave__ *(pip3 install wave)*
* __pickle__ *(pip3 install pickle)*
* __socketio__ *(pip3 install python-socketio[client])*

## Usage

Before running the Pi, server has to be running first. Then, run the following command:

``` console
python3 start.py http[s]://[IP_ADDRESS]:[PORT]
```

`start.py` accept one parameter argument for server address. The Pi will then start listening to server for any command.

To run the Pi without server connection:

``` console
python3 run.py
```

This script uses APA102 library for LED on ReSpeaker board. You may modify the sound for Pi to detect in the script.

``` python
TO_DETECT = [SOUND_ID]
```

Replace [SOUND_ID] with the ID of sound event to detect. Once the Pi detects that sound, the LED will light up on the board.

## Disclaimer

Currently, sounds are not being analysed in real-time. The Pi records a sound, then extracts the features and predicts the sound event. After all that, the Pi will start recording the sound for next prediction.

# NUesc

NUesc is IoT based environmental sound classification system for smart cities. The machine learning inference is deployed on Raspberry Pi to detect the events such as dog bark, car horn, gun shot and so on. The Raspberry Pi talks to cloud server when the event is detected. The web application is used to manage the sounds for Raspberry Pi to listen to.

This is the final year project of Software Engineering from University of Newcastle, Australia. This project is currently in prototype version.

## Requirement

* Python 3
* Nodejs
* Raspberry Pi 3
* ReSpeaker 2-Mics Pi HAT
* UrbanSound8K Dataset

## Instruction

There are four components: model, nuesc-pi, server, and webapp. The *__detail documentation__* for each component can be found in each folder. The instructions for setup are as follows:

* First train the machine learning model. There are two models: SVM and KNN.
* Copy __nuesc-pi__ into Rasbperry Pi.
* Copy trained model to __nuesc-pi__ folder on Raspberry Pi. Make sure to name the model file as *model.p*
* Then, run the server from __server__ folder.
* Finally, web application can be launched from __webapp__.

To setup Raspberry Pi and Respeaker 2-Mics Pi HAT, please follow http://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT/
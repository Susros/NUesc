# NUesc Cloud Server

The server helps communication between Web Application and Raspberry Pi. It listens to the message sent from Raspberry Pi and Web Application, then sends a response back. The communication is done via Socket.

## Requirement

* Nodejs

## Usage

First, install all dependencies:

``` console
npm install
```

Then, configure the server in *.env* file:

``` env
PORT=8080
```

The default port is 8080.

Then, run the server:

``` console
npm start
```

/**
 * NUesc Server
 * 
 * This server handles request from Raspberry Pi when
 * the sound event is detected.
 * 
 * @author Kelvin Yin
 * @since 1.0.0
 * @version 1.0.0
 */

// Set up environment
const dotenv       = require('dotenv');
dotenv.config();

// Set up express framework
const express      = require('express');
const bodyParser   = require('body-parser');
const helmet       = require('helmet');
const cookieparser = require('cookie-parser');
const socket       = require('socket.io');
const cors         = require('cors');

const app = express();
app.use(helmet());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(cookieparser());
app.use(cors({ credentials: true, origin: '*' }));

// Listen
const server = app.listen(process.env.PORT);

// Web Socket
var ws = socket(server);

// Sound Class
const soundClass = [
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

// Check web socket connection
ws.on('connection', (s) => {
    console.log("Socket connection received: " + s.id);

    s.on('pi_detected', (data) => {
        ws.emit('webapp_detected', {
            data : {
                id: data,
                sound_event: soundClass[data]
            }
        })
    });

    s.on('webapp_setsound', (data) => {
        ws.emit('pi_setsound', data);
    });

    s.on('pi_status', (data) => {
        ws.emit('webapp_status', data);
    });
});

app.get('/soundclass', (req, res) => {
    res.status(200).json({ data: soundClass });
});
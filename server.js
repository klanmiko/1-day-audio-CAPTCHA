const express = require('express')
const fileUpload = require('express-fileupload')
const fs = require('fs')
const ogg = require('ogg');
const opus = require('node-opus');
 
// Create the encoder.
// Specify 48kHz sampling rate and 10ms frame size.
// NOTE: The decoder must use the same values when decoding the packets.
var rate = 48000;

const app = express()
const port = 8000

var decoder = new ogg.Decoder();
const Readable = require('stream').Readable ; 

decoder.on('stream', function (stream) {   
    // emitted for each `ogg_packet` instance in the stream.
    var opusDecoder = new opus.Decoder();
    opusDecoder.on('format', function (format) {
	    opusDecoder.pipe(process.stdout);

        // or pipe to node-speaker, a file, etc
    });

    // an "error" event will get emitted if the stream is not a Vorbis stream
    // (i.e. it could be a Theora video stream instead)
    opusDecoder.on('error', console.error);

    stream.pipe(opusDecoder);
  });

app.use(fileUpload());

app.get('/', (req, res) => res.sendFile('index.html', {root: __dirname}))

app.post('/audio', (req, res) => {
    let speech = req.files.speech;
    let stream = new Readable()
    stream.push(speech.data);
    fs.writeFile('./speech.ogg', speech.data, () => {});
    stream.push(null);
    stream.pipe(decoder)
    res.sendStatus(200);
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))
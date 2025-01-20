//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;
var gumStream;
//stream from getUserMedia()
var rec;
//Recorder.js object
var input;
//MediaStreamAudioSourceNode we'll be recording
// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext = new AudioContext;
//new audio context to help us record
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");
var proc = document.getElementById("procesing");
var ptx = document.getElementById("player_text");
var pl = document.getElementById("player");
//add events to those 3 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);
// const saveButton = document.getElementById('saveButton');

function startRecording() { console.log("recordButton clicked");
proc.style.display = 'none';
ptx.style.display ='none';
pl.style.display ='none';
var au = document.getElementById('player1');
au.style.display='none';
var constraints = {
    audio: true,
    video: false
}

recordButton.disabled = true;
stopButton.disabled = false;
pauseButton.disabled = false

navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
    /* assign to gumStream for later use */
    gumStream = stream;
    /* use the stream */
    input = audioContext.createMediaStreamSource(stream);
    /* Create the Recorder object and configure to record mono sound (1 channel) Recording 2 channels will double the file size */
    rec = new Recorder(input, {
        numChannels: 1
    })
    //start the recording process
    rec.record()
    console.log("Recording started");
}).catch(function(err) {
    //enable the record button if getUserMedia() fails
    recordButton.disabled = false;
    stopButton.disabled = true;
    pauseButton.disabled = true
});
}
function pauseRecording() {
    console.log("pauseButton clicked rec.recording=", rec.recording);
    if (rec.recording) {
        //pause
        rec.stop();
        pauseButton.innerHTML = "Resume";
    } else {
        //resume
        rec.record()
        pauseButton.innerHTML = "Pause";
    }
}
function stopRecording() {
    proc.style.display ='block';
    console.log("stopButton clicked");
    //disable the stop button, enable the record too allow for new recordings
    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;
    //reset button just in case the recording is stopped while paused
    pauseButton.innerHTML = "Pause";
    //tell the recorder to stop the recording
    rec.stop(); //stop microphone access
    gumStream.getAudioTracks()[0].stop();
    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV(createDownloadLink);
}
function createDownloadLink(blob) {
    const filename =  'recording.wav';
    const formData = new FormData();
    const fr= document.getElementById("fromLanguage").value
    const to = document.getElementById("toLanguage").value
    console.log(fr,to)
    formData.append('audio', blob);
    formData.append('filename', filename);
    formData.append('fr', fr);
    formData.append('to', to);
    fetch('/upload', {
                    method: 'POST',
                    body: formData
                }).catch(error => console.error('Error:', error));
    var url = URL.createObjectURL(blob);
    var au = document.getElementById('player1');
    au.style.display='block';
    var li = document.createElement('li');
    var link = document.createElement('a');
    //add controls to the <audio> element
    au.controls = true;
    au.src = url;
    //link the a element to the blob
    link.href = url;
    link.download = new Date().toISOString() + '.wav';
    link.innerHTML = link.download;

    setTimeout(function(){ loadAudio()},22000);
}
function loadAudio() {
    proc.style.display ='none';
    pl.style.display ='block';
    ptx.style.display ='block';
    fetch('/generate_audio')
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.blob();
        })
        .then(blob => {
            const audioUrl = URL.createObjectURL(blob);
            const audioPlayer = document.getElementById('player');
            audioPlayer.src = audioUrl;
            audioPlayer.play(); // Automatically play the audio once loaded
        })
        .catch(error => {
            console.error('Error fetching audio:', error);
        });
}
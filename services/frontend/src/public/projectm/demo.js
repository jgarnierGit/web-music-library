"use strict";

let _rAF, analyser, audioBuffer, canvas, pmModule;
let isStopped = true;

function addAudioData() {
    if (!audioBuffer) return;

    analyser.getByteTimeDomainData(audioBuffer);

    pmModule.ccall(
        'add_audio_data',
        null,
        ['array', 'number'],
        [audioBuffer, audioBuffer.length],
    );
}

function createCanvas() {
    if (canvas) return;

    let container = document.getElementById('container');
    let width = container.clientWidth;
    let height = container.clientHeight;

    canvas = document.createElement('canvas');
    canvas.id = "my-canvas";
    canvas.width = width;
    canvas.height = height;

    container.appendChild(canvas);
}

function destruct() {
    if (!pmModule) return;

    isStopped = true;
    pmModule.destruct();

    if (canvas) {
        let container = document.getElementById('container');
        container.removeChild(canvas);
        canvas = null;
    }
}

function init() {
    if (!pmModule) return;
    createCanvas();
    pmModule.init();
    pmModule.setWindowSize(canvas.width, canvas.height);
}

function loadModule() {
    if (pmModule) return;

    createModule({
        noInitialRun: true,
    })
        .then(module => {
            pmModule = module;
            console.log('module loaded');
        });
}

function loadPreset() {
    if (!pmModule) return;
    //pmModule.loadPresetFile('presets/Martin - underwater cathedral.milk');  // RuntimeError
    //pmModule.loadPresetFile('presets/martin - cope - laser dome.milk');
    //pmModule.loadPresetFile('presets/martin - the forge of isengard.milk');
    pmModule.loadPresetFile('presets/martin - castle in the air.milk');
}

function enableAudio(audio, enableLoop) {
    // already enabled
    if (audioBuffer) return;

    let audioContext = new AudioContext();

    let inputNode = audioContext.createGain();
    let outputNode = audioContext.createGain();

    inputNode.connect(outputNode);
    outputNode.connect(audioContext.destination);
    audio.loop = enableLoop;
    let sourceNode = audioContext.createMediaElementSource(audio);
    sourceNode.connect(inputNode);

    analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;  // pass 256 samples to projectM
    inputNode.connect(analyser);

    audioBuffer = new Uint8Array(analyser.fftSize);
}

function toggleVisualizer() {
    if (!pmModule) return;

    if (isStopped) {
        isStopped = false;
        init();
        visualize();
    }
    else {
        isStopped = true;
        cancelAnimationFrame(_rAF);
    }
}

function visualize() {
    if (isStopped) return;
    _rAF = requestAnimationFrame(() => visualize());
    addAudioData();
    pmModule.renderFrame();
}

document.addEventListener("DOMContentLoaded", loadModule);

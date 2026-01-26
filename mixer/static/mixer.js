// --- Controls ---
const speedControl = document.getElementById('speed');
const pitchControl = document.getElementById('frequency');
const amplitudeControl = document.getElementById('amplitude');
const loopsControl = document.getElementById('loops');
const resetBtn = document.getElementById('resetBtn');

const speedValue = document.getElementById('speedValue');
const pitchValue = document.getElementById('pitchValue');
const amplitudeValue = document.getElementById('amplitudeValue');

const categorySelect = document.getElementById('categorySelect');
const subcategorySelect = document.getElementById('subcategorySelect');
const speciesSelect = document.getElementById('speciesSelect');
const soundSelect = document.getElementById('soundSelect');
const playButton = document.getElementById('playClip');

const waveformContainer = document.getElementById('waveformContainer');
const spectrogramContainer = document.getElementById('spectrogramContainer');

const addToMixBtn = document.getElementById("addToMix");
const timeline = document.querySelector("#fullSongContainer .timeline-track");

let audioContext = null;
let sourceNode = null;
let gainNode = null;
let audioBuffer = null;
let isPlaying = false;
let songClips = [];
let songSources = [];
let selectedClipId = null;
const songTimeline = document.getElementById("songTimeline");
const SONG_DURATION = 60;
const PX_PER_SECOND = 20; // visual scale

// Load sound structure
let soundStructure = {};
try {
    soundStructure = JSON.parse(document.getElementById('sound-structure-data').textContent);
} catch (e) {
    console.error("Failed to load sound structure", e);
}

// --- Audio Functions ---
function initAudioContext() {
    if (!audioContext) audioContext = new (window.AudioContext || window.webkitAudioContext)();
    return audioContext;
}

function stopPlayback() {
    if (sourceNode) {
        try { sourceNode.stop(); } catch(e){}
        sourceNode = null;
    }
    isPlaying = false;
}

function updateAudioSettings() {
    if (!sourceNode || !gainNode) return;
    sourceNode.playbackRate.value = parseFloat(speedControl.value);
    gainNode.gain.value = parseFloat(amplitudeControl.value);

    const pitchShiftHz = parseFloat(pitchControl.value);
    const referenceFrequency = 440;
    if (pitchShiftHz !== 0) {
        const ratio = 1 + pitchShiftHz / referenceFrequency;
        sourceNode.detune.value = 1200 * Math.log2(ratio);
    }
}

async function playAudio(url) {
    const ctx = initAudioContext();
    stopPlayback();

    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    audioBuffer = await ctx.decodeAudioData(arrayBuffer);

    sourceNode = ctx.createBufferSource();
    gainNode = ctx.createGain();
    sourceNode.buffer = audioBuffer;

    sourceNode.connect(gainNode);
    gainNode.connect(ctx.destination);

    updateAudioSettings();

    sourceNode.start();
    isPlaying = true;

    sourceNode.onended = () => { isPlaying = false; };
}

// --- Load Timeseries ---
async function loadTimeseries(audioUrl) {
    waveformContainer.innerHTML = `<div class="text-center py-3">Loading...</div>`;
    try {
        const response = await fetch(`/mixer/timeseries/?audio_url=${encodeURIComponent(audioUrl)}&speed=${speedControl.value}&pitch=${pitchControl.value}&amplitude=${amplitudeControl.value}`);
        const data = await response.json();
        if (data.success) {
            waveformContainer.innerHTML = `<img src="data:image/png;base64,${data.timeseries}" class="img-fluid" style="border-radius:5px;">`;
        } else {
            waveformContainer.innerHTML = `<div class="alert alert-danger">Failed to generate waveform</div>`;
        }
    } catch (err) {
        waveformContainer.innerHTML = `<div class="alert alert-danger">Error loading waveform</div>`;
        console.error(err);
    }
}

// --- Load Spectrogram ---
async function loadSpectrogram(audioUrl) {
    spectrogramContainer.innerHTML = `<div class="text-center py-3">Loading...</div>`;
    try {
        const response = await fetch(`/mixer/spectrogram/?audio_url=${encodeURIComponent(audioUrl)}&speed=${speedControl.value}&pitch=${pitchControl.value}&amplitude=${amplitudeControl.value}`);
        const data = await response.json();
        if (data.success) {
            spectrogramContainer.innerHTML = `<img src="data:image/png;base64,${data.spectrogram}" class="img-fluid" style="border:1px solid #dee2e6; border-radius:5px;">`;
        } else {
            spectrogramContainer.innerHTML = `<div class="alert alert-danger">Failed to generate spectrogram</div>`;
        }
    } catch (err) {
        spectrogramContainer.innerHTML = `<div class="alert alert-danger">Error loading spectrogram</div>`;
        console.error(err);
    }
}

// --- Update Previews ---
function updatePreview() {
    const url = soundSelect.value;
    if (!url) return;
    loadTimeseries(url);
    loadSpectrogram(url);
}

// --- Dropdown Logic ---
categorySelect.addEventListener('change', function() {
    const cat = this.value;
    subcategorySelect.innerHTML = '<option value="">Select a subcategory...</option>';
    speciesSelect.innerHTML = '<option value="">Select a subcategory first...</option>';
    soundSelect.innerHTML = '<option value="">Make selections above...</option>';
    speciesSelect.disabled = true; soundSelect.disabled = true;

    if (cat && soundStructure[cat]) {
        subcategorySelect.disabled = false;
        Object.keys(soundStructure[cat]).forEach(subcat => {
            if (subcat !== '_files') {
                const opt = document.createElement('option');
                opt.value = subcat; opt.textContent = subcat;
                subcategorySelect.appendChild(opt);
            }
        });
        if (soundStructure[cat]._files) {
            const opt = document.createElement('option');
            opt.value = '_direct'; opt.textContent = 'Any/all';
            subcategorySelect.appendChild(opt);
        }
    } else subcategorySelect.disabled = true;
});

subcategorySelect.addEventListener('change', function() {
    const cat = categorySelect.value;
    const sub = this.value;
    speciesSelect.innerHTML = '<option value="">Select species/type...</option>';
    soundSelect.innerHTML = '<option value="">Select a species first...</option>';
    soundSelect.disabled = true;

    if (cat && sub && soundStructure[cat][sub]) {
        speciesSelect.disabled = false;
        if (sub === '_direct') {
            speciesSelect.disabled = true;
            soundSelect.disabled = false;
            soundStructure[cat]._files.forEach(f => {
                const o = document.createElement('option'); o.value = f.url; o.textContent = f.display_name;
                soundSelect.appendChild(o);
            });
        } else {
            Object.keys(soundStructure[cat][sub]).forEach(spec => {
                if (spec !== '_files') {
                    const opt = document.createElement('option'); opt.value = spec; opt.textContent = spec;
                    speciesSelect.appendChild(opt);
                }
            });
            if (soundStructure[cat][sub]._files) {
                const opt = document.createElement('option'); opt.value = '_direct'; opt.textContent = 'Any/all';
                speciesSelect.appendChild(opt);
            }
        }
    } else speciesSelect.disabled = true;
});

speciesSelect.addEventListener('change', function() {
    const cat = categorySelect.value;
    const sub = subcategorySelect.value;
    const spec = this.value;
    soundSelect.innerHTML = '<option value="">Select a sound...</option>';

    if (cat && sub && spec) {
        soundSelect.disabled = false;
        if (spec === '_direct') {
            (soundStructure[cat][sub]._files || []).forEach(f => {
                const o = document.createElement('option'); o.value = f.url; o.textContent = f.display_name;
                soundSelect.appendChild(o);
            });
        } else {
            (soundStructure[cat][sub][spec] || []).forEach(f => {
                const o = document.createElement('option'); o.value = f.url; o.textContent = f.display_name;
                soundSelect.appendChild(o);
            });
        }
    } else soundSelect.disabled = true;
});

// --- Event Listeners ---
soundSelect.addEventListener('change', () => {
    stopPlayback();
    updatePreview();
});

[speedControl, pitchControl, amplitudeControl, loopsControl].forEach(el => {
    el.addEventListener('input', () => {
        speedValue.textContent = parseFloat(speedControl.value).toFixed(1) + 'x';
        pitchValue.textContent = pitchControl.value + ' Hz';
        amplitudeValue.textContent = parseFloat(amplitudeControl.value).toFixed(1) + 'x';
        if (isPlaying) updateAudioSettings();
        updatePreview();
    });
});

playButton.addEventListener('click', () => playAudio(soundSelect.value));

resetBtn.addEventListener('click', () => {
    speedControl.value = 1; pitchControl.value = 0; amplitudeControl.value = 1; loopsControl.value = 1;
    speedValue.textContent = '1.0x'; pitchValue.textContent = '0 Hz'; amplitudeValue.textContent = '1.0x';
    if (isPlaying) updateAudioSettings();
    updatePreview();
});

addToMixBtn.addEventListener("click", async () => {
    const url = soundSelect.value;
    if (!url) return alert("Select a sound first");

    const ctx = initAudioContext();
    const buffer = await fetch(url)
        .then(r => r.arrayBuffer())
        .then(b => ctx.decodeAudioData(b));

    const baseDuration = buffer.duration;
    const loops = +loopsControl.value;

    const clip = {
        id: crypto.randomUUID(),
        url,
        category: categorySelect.value,
        species: speciesSelect.value,
        speed: +speedControl.value,
        pitch: +pitchControl.value,
        amplitude: +amplitudeControl.value,
        loops,
        start: 0,
        baseDuration,
        duration: baseDuration * loops
    };

    songClips.push(clip);
    renderSong();
});

function createTrack({ url, category, iconUrl, timeseries, duration }) {
    const clip = document.createElement("div");
    clip.className = "clip";
    clip.style.left = "0px";
    clip.style.width = (duration * PX_PER_SECOND) + "px";

    clip.innerHTML = `
        <div class="clip-icon">
            <img src="${iconUrl}">
        </div>
        <img class="clip-waveform" src="data:image/png;base64,${timeseries}">
    `;

    makeDraggable(clip);
    timeline.appendChild(clip);
}

function makeDraggable(el) {
    el.onmousedown = e => {
        const startX = e.clientX;
        const startLeft = el.offsetLeft;

        document.onmousemove = ev => {
            const dx = ev.clientX - startX;
            el.style.left = Math.max(0, startLeft + dx) + "px";
        };

        document.onmouseup = () => {
            document.onmousemove = null;
            document.onmouseup = null;
        };
    };
}
async function renderSong() {
    const container = document.getElementById("songTracks");
    container.innerHTML = "";

    for (const clip of songClips) {
        const track = document.createElement("div");
        track.className = "song-track";

        const icon = document.createElement("div");
        icon.className = "track-icon";
        icon.innerHTML = `<img src="/static/icons/${clip.category}.png">`;

        // Fetch waveform base64 for one loop
        const waveformData = await fetch(
        `/mixer/timeseriesSlider/?audio_url=${encodeURIComponent(clip.url)}&speed=${clip.speed}&pitch=${clip.pitch}&amplitude=${clip.amplitude}&category=${clip.category}`
        ).then(r => r.json());
        
        const el = document.createElement("div");
        el.className = "clip";
        el.classList.add(clip.category);  // Add category as class for coloring
        if (clip.id === selectedClipId) el.classList.add("selected");

        el.style.left = (clip.start * PX_PER_SECOND + 24) + "px";
        el.style.width = (clip.duration * PX_PER_SECOND) + "px";
        el.dataset.id = clip.id;
        const waveformColor = categoryColors[clip.category] || "#000000";
        
        el.innerHTML = `
            <div class="clip-icon">
                <img src="/static/icons/${clip.species}.png" />
            </div>
            <div class="clip-waveform" style="
                background-color: ${waveformColor};
                -webkit-mask-image: url('data:image/png;base64,${waveformData.timeseries}');
                mask-image: url('data:image/png;base64,${waveformData.timeseries}');
                mask-repeat: repeat-x;
                mask-size: auto 100%;
                width: 100%;
                height: 100%;
            "></div>
        `;

        enableDrag(el, clip);
        el.onclick = () => {
            selectClip(clip.id);
            renderSong(); // re-render to update highlight
        };

        track.append(el);
        container.appendChild(track);
    }
}

function enableDrag(el, clip) {
    el.onmousedown = e => {
        const startX = e.clientX;
        const startLeft = clip.start * PX_PER_SECOND;

        document.onmousemove = ev => {
            let dx = ev.clientX - startX;
            let px = Math.max(
                0,
                Math.min(startLeft + dx, SONG_DURATION * PX_PER_SECOND)
            );

            clip.start = Math.round(px / PX_PER_SECOND);
            el.style.left = (px + 24) + "px";
        };

        document.onmouseup = () => {
            document.onmousemove = null;
        };
    };
}
document.getElementById("songPlay").onclick = async () => {
    const ctx = initAudioContext();
    songSources = [];

    for (const clip of songClips) {
        const buffer = await fetch(clip.url)
            .then(r => r.arrayBuffer())
            .then(b => ctx.decodeAudioData(b));

        for (let i = 0; i < clip.loops; i++) {
            const src = ctx.createBufferSource();
            const gain = ctx.createGain();

            src.buffer = buffer;
            src.playbackRate.value = clip.speed;
            src.detune.value = clip.pitch;
            gain.gain.value = clip.amplitude;

            src.connect(gain).connect(ctx.destination);
            src.start(ctx.currentTime + clip.start + i * buffer.duration);

            songSources.push(src);
        }
    }
};
function selectClip(id) {
    if (selectedClipId === id) {
        selectedClipId = null; // toggle off if already selected
    } else {
        selectedClipId = id;
    }
    renderSong(); // rerender to update highlight
}
document.getElementById("songStop").onclick = () => {
    songSources.forEach(src => {
        try { src.stop(); } catch {}
    });
    songSources = [];
};
function selectClip(id) {
    selectedClipId = id;
}

document.getElementById("deleteClip").onclick = () => {
    if (!selectedClipId) return;
    songClips = songClips.filter(c => c.id !== selectedClipId);
    selectedClipId = null;
    renderSong();
};
document.getElementById("clearSong").onclick = () => {
    songClips = [];
    renderSong();
};

document.getElementById("exportWavBtn").addEventListener("click", exportMixAsWav);

const categoryColors = {
        'Anthropogenic': "#57f011",
        'Environmental': "#0ebfff",
        'Biological': "#edc526",
    }

function bufferToWavBlob(buffer) {
  const numOfChan = buffer.numberOfChannels,
        length = buffer.length * numOfChan * 2 + 44,
        bufferArray = new ArrayBuffer(length),
        view = new DataView(bufferArray),
        channels = [],
        sampleRate = buffer.sampleRate;

  function writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  }

  // RIFF chunk descriptor
  writeString(view, 0, 'RIFF');
  view.setUint32(4, length - 8, true);
  writeString(view, 8, 'WAVE');
  writeString(view, 12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true); // PCM format
  view.setUint16(22, numOfChan, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2 * numOfChan, true);
  view.setUint16(32, numOfChan * 2, true);
  view.setUint16(34, 16, true);
  writeString(view, 36, 'data');
  view.setUint32(40, length - 44, true);

  // Write interleaved audio data
  for (let i = 0; i < numOfChan; i++) {
    channels.push(buffer.getChannelData(i));
  }

  let offset = 44;
  for (let i = 0; i < buffer.length; i++) {
    for (let chan = 0; chan < numOfChan; chan++) {
      let sample = channels[chan][i];
      sample = Math.max(-1, Math.min(1, sample));
      view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
      offset += 2;
    }
  }

  return new Blob([bufferArray], { type: 'audio/wav' });
}

async function exportMixAsWav() {
  if (!songClips.length) {
    alert("No clips to export!");
    return;
  }

  const sampleRate = 44100;  // Standard sample rate
  // Calculate total duration needed, accounting for clip start + duration
  const totalDuration = Math.max(...songClips.map(c => c.start + c.duration));
  const ctx = new OfflineAudioContext(2, sampleRate * totalDuration, sampleRate);

  for (const clip of songClips) {
    // Fetch and decode audio buffer for this clip
    const buffer = await fetch(clip.url)
      .then(r => r.arrayBuffer())
      .then(b => ctx.decodeAudioData(b));

    // Create a buffer source for each loop iteration
    for (let i = 0; i < clip.loops; i++) {
      const source = ctx.createBufferSource();
      source.buffer = buffer;
      source.playbackRate.value = clip.speed;
      source.detune.value = clip.pitch;

      const gainNode = ctx.createGain();
      gainNode.gain.value = clip.amplitude;

      source.connect(gainNode).connect(ctx.destination);

      // Start time = clip start + loop iteration * base duration
      source.start(clip.start + i * buffer.duration);
    }
  }

  // Render the mixed audio offline
  const renderedBuffer = await ctx.startRendering();

  // Convert to WAV blob
  const wavBlob = bufferToWavBlob(renderedBuffer);

  // Trigger file download
  const url = URL.createObjectURL(wavBlob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "mix.wav";
  a.click();

  URL.revokeObjectURL(url);
}
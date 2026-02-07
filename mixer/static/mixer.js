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
const songWrapper = document.getElementById("songWrapper");


let audioContext = null;
let sourceNode = null;
let gainNode = null;
let audioBuffer = null;
let playheadInterval = null;
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

function resolveIconPath(clip) {
    const base = "/static/icons";
    const { category, subcategory, species } = clip;

    const catData = soundStructure?.[category];
    const subData = catData?.[subcategory];

    // Species (only if species folder exists)
    if (
        subData &&
        species &&
        species !== "_direct" &&
        Array.isArray(subData[species])
    ) {
        return `${base}/${species}.png`;
    }

    // Subcategory
    if (subcategory && subcategory !== "_direct") {
        return `${base}/${subcategory}.png`;
    }

    // Category fallback
    return `${base}/${category}.png`;
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
songWrapper.addEventListener("scroll", () => {
    const playhead = document.getElementById("playhead");
    playhead.style.top = songWrapper.scrollTop + "px";
});

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

[speedControl, pitchControl, amplitudeControl].forEach(el => {
    el.addEventListener('input', () => {
        speedValue.textContent = parseFloat(speedControl.value).toFixed(1) + 'x';
        pitchValue.textContent = pitchControl.value + ' Hz';
        amplitudeValue.textContent = parseFloat(amplitudeControl.value).toFixed(1) + 'x';

        if (isPlaying) updateAudioSettings();
    });
});
[speedControl, pitchControl, amplitudeControl].forEach(el => {
    el.addEventListener('change', () => {
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

    const baseDuration = buffer.duration / +speedControl.value; // <-- divide by speed
    let loops = +loopsControl.value;
    let totalDuration = baseDuration * loops;

    // Clip to max 60s
    if (totalDuration > SONG_DURATION) {
        loops = Math.floor(SONG_DURATION / baseDuration);   // full loops that fit
        const remainder = SONG_DURATION - loops * baseDuration; // partial last loop
        totalDuration = loops * baseDuration + remainder;
    } else {
        var remainder = 0;
    }

    // Clip to max 60s
    if (totalDuration > SONG_DURATION) {
        loops = Math.floor(SONG_DURATION / baseDuration);   // full loops that fit
        const remainder = SONG_DURATION - loops * baseDuration; // partial last loop
        totalDuration = loops * baseDuration + remainder;
    } else {
        var remainder = 0;
    }

    const clip = {
    id: crypto.randomUUID(),
    url,
    category: categorySelect.value,
    subcategory: subcategorySelect.value,
    species: speciesSelect.value,
    speed: +speedControl.value,
    pitch: +pitchControl.value,
    amplitude: +amplitudeControl.value,
    fullLoops: loops,
    remainder,
    start: 0,
    baseDuration,
    duration: totalDuration
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

        // Clip icon
        const icon = document.createElement("div");
        icon.className = "track-icon";
        icon.innerHTML = `<img src="${resolveIconPath(clip)}">`;

        // Fetch waveform base64 for **one loop**
        const waveformData = await fetch(
            `/mixer/timeseriesSlider/?audio_url=${encodeURIComponent(clip.url)}&speed=${clip.speed}&pitch=${clip.pitch}&amplitude=${clip.amplitude}&category=${clip.category}`
        ).then(r => r.json());

        // Compute total width
        const totalWidthPx = clip.duration * PX_PER_SECOND;
        const singleLoopWidthPx = clip.baseDuration * PX_PER_SECOND;

        // Build waveform HTML with one <img> per loop
        let waveformHTML = "";
        for (let i = 0; i < clip.fullLoops; i++) {
            waveformHTML += `<img src="data:image/png;base64,${waveformData.timeseries}"
                              style="height:100%; flex-shrink:0; width:${singleLoopWidthPx}px;">`;
        }
        if (clip.remainder > 0) {
            const remainderWidthPx = clip.remainder * PX_PER_SECOND;
            waveformHTML += `<img src="data:image/png;base64,${waveformData.timeseries}"
                              style="height:100%; flex-shrink:0; width:${remainderWidthPx}px; object-fit:cover;">`;
        }

        // Clip element
        const el = document.createElement("div");
        el.className = "clip";
        el.classList.add(clip.category);
        if (clip.id === selectedClipId) el.classList.add("selected");

        el.style.left = (clip.start * PX_PER_SECOND + 24) + "px";
        el.style.width = `${totalWidthPx}px`;
        el.dataset.id = clip.id;

        el.innerHTML = `
            <div class="clip-icon">
                <img src="${resolveIconPath(clip)}" />
            </div>
            <div class="clip-waveform-wrapper" style="display:flex; height:100%; width:100%; overflow:hidden;">
                ${waveformHTML}
            </div>
        `;

        enableDrag(el, clip);
        el.onclick = e => {
            e.stopPropagation();
            selectClip(clip.id);
        };

        track.append(el);
        container.appendChild(track);
    }

    container.style.minWidth = (SONG_DURATION * PX_PER_SECOND + 48) + "px";
    resizeSongGrid();
}

// --- Playhead logic ---
document.getElementById("songPlay").onclick = async () => {
    // Stop any currently playing audio
    songSources.forEach(src => { try { src.stop(); } catch {} });
    clearInterval(playheadInterval);

    const ctx = initAudioContext();
    songSources = [];

    const playhead = document.getElementById("playhead");
    const startTime = ctx.currentTime;
    playhead.style.left = "24px";

    // Move playhead visually
    playheadInterval = setInterval(() => {
        const elapsed = ctx.currentTime - startTime; // real seconds
        const px = elapsed * PX_PER_SECOND;

        if (elapsed > SONG_DURATION) {
            clearInterval(playheadInterval);
            return;
        }

        playhead.style.left = (px + 24) + "px";
    }, 30);

    // Play each clip
    for (const clip of songClips) {
        const buffer = await fetch(clip.url)
            .then(r => r.arrayBuffer())
            .then(b => ctx.decodeAudioData(b));

        const clipDuration = buffer.duration / clip.speed;

        // Full loops
        for (let i = 0; i < clip.fullLoops; i++) {
            const src = ctx.createBufferSource();
            const gain = ctx.createGain();

            src.buffer = buffer;
            src.playbackRate.value = clip.speed;
            src.detune.value = clip.pitch;
            gain.gain.value = clip.amplitude;

            src.connect(gain).connect(ctx.destination);
            src.start(ctx.currentTime + clip.start + i * clipDuration);

            songSources.push(src);
        }

        // Remainder
        if (clip.remainder > 0) {
            const src = ctx.createBufferSource();
            const gain = ctx.createGain();

            src.buffer = buffer;
            src.playbackRate.value = clip.speed;
            src.detune.value = clip.pitch;
            gain.gain.value = clip.amplitude;

            src.connect(gain).connect(ctx.destination);
            src.start(ctx.currentTime + clip.start + clip.fullLoops * clipDuration, 0, clip.remainder);

            songSources.push(src);
        }
    }
};

function resizeSongGrid() {
    const grid = document.getElementById("songGrid");
    const tracksContainer = document.getElementById("songTracks");

    // Minimum width to cover full 60s
    const minWidth = SONG_DURATION * PX_PER_SECOND + 48; // +24px padding left + right
    const contentWidth = tracksContainer.scrollWidth;

    grid.style.width = Math.max(minWidth, contentWidth) + "px";
    grid.style.height = tracksContainer.scrollHeight + "px";
}

function enableDrag(el, clip) {
    el.onmousedown = e => {
        e.preventDefault();

        const startX = e.clientX;
        const startLeftPx = el.offsetLeft;

        const minLeftPx = 24;
        const maxLeftPx =
            24 + (SONG_DURATION - clip.duration) * PX_PER_SECOND;

        document.onmousemove = ev => {
            const dx = ev.clientX - startX;

            let newLeftPx = startLeftPx + dx;
            newLeftPx = Math.max(minLeftPx, Math.min(newLeftPx, maxLeftPx));

            el.style.left = newLeftPx + "px";

            // pixels → seconds
            const startSeconds = (newLeftPx - 24) / PX_PER_SECOND;

            // HARD clamp (this is the important part)
            clip.start = Math.max(
                0,
                Math.min(startSeconds, SONG_DURATION - clip.duration)
            );
        };

        document.onmouseup = () => {
            document.onmousemove = null;
            document.onmouseup = null;
        };
    };
}



function selectClip(id) {
    selectedClipId = selectedClipId === id ? null : id;
    renderSong();
}

document.getElementById("songStop").onclick = () => {
    songSources.forEach(src => {
        try { src.stop(); } catch {}
    });
    songSources = [];

    clearInterval(playheadInterval);
};

document.getElementById("deleteClip").onclick = () => {
    if (!selectedClipId) return;
    songClips = songClips.filter(c => c.id !== selectedClipId);
    selectedClipId = null;
    renderSong();
};

document.getElementById("clearSong").onclick = () => {
    songSources.forEach(src => {
        try { src.stop(); } catch {}
    });
    clearInterval(playheadInterval);
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

    const sampleRate = 44100;
    const totalDuration = Math.max(...songClips.map(c => c.start + c.duration));
    const ctx = new OfflineAudioContext(2, sampleRate * totalDuration, sampleRate);

    for (const clip of songClips) {
        const buffer = await fetch(clip.url)
            .then(r => r.arrayBuffer())
            .then(b => ctx.decodeAudioData(b));

        const clipDuration = buffer.duration / clip.speed; // <-- adjust for speed

        // Full loops
        for (let i = 0; i < clip.fullLoops; i++) {
            const source = ctx.createBufferSource();
            const gainNode = ctx.createGain();

            source.buffer = buffer;
            source.playbackRate.value = clip.speed;
            source.detune.value = clip.pitch;
            gainNode.gain.value = clip.amplitude;

            source.connect(gainNode).connect(ctx.destination);
            source.start(clip.start + i * clipDuration);
        }

        // Remainder
        if (clip.remainder > 0) {
            const source = ctx.createBufferSource();
            const gainNode = ctx.createGain();

            source.buffer = buffer;
            source.playbackRate.value = clip.speed;
            source.detune.value = clip.pitch;
            gainNode.gain.value = clip.amplitude;

            source.connect(gainNode).connect(ctx.destination);
            source.start(clip.start + clip.fullLoops * clipDuration, 0, clip.remainder);
        }
    }

    const renderedBuffer = await ctx.startRendering();
    const wavBlob = bufferToWavBlob(renderedBuffer);

    const url = URL.createObjectURL(wavBlob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "mix.wav";
    a.click();
    URL.revokeObjectURL(url);
}



//CLIPPY HELPERS
const clippyData = {
    waveform: {
        title: "Waveform",
        blurb: `All sounds in the ocean travel as waves through the water. It starts when something like a whale or a boat creates a vibration that increases local 
        pressure. That pressure increase and subsequent decrease moves outward, passing from molecule to molecule, spreading across the ocean as a traveling wave 
        that carries the sound far from its source.Here, you can see what we call a waveform in the image. A waveform is a time-series plot showing how a sound changes 
        over time. The x-axis represents time, and the y-axis represents the sound’s amplitude, or strength.
        Peaks in the waveform occur when water pressure is high, and dips occur when it’s low. These pressure changes travel through the ocean and reach our sensors. 
        In general, a larger amplitude means a louder sound, and a faster wave (more waves close together) corresponds to a higher pitch. You can see each of these 
        features in the image below:`,
        staticFile: "{% static 'Clippy_support/timeseries.jpg' %}" 
    },
    spectrogram: {
        title: "Spectrogram",
        blurb: ` A spectrogram is a tool scientists use to see how a sound changes over time. In the plot, time runs along the horizontal 
        axis and frequency along the vertical axis. Colors show the amplitude, or strength, of the sound at each frequency and moment. 
        This creates a visual map of the sound, helping us identify different sources in the underwater soundscape. In the example below, 
        you can see an orca singing: his song rises and falls in frequency and amplitude, creating the flowing patterns you see.`,
        staticFile: "{% static 'Clippy_support/spectrogram.jpg' %}" 
    },
    clippyspeed: {
        title: "Frequency",
        blurb: `Frequency tells us how fast a sound wave vibrates. Higher frequencies mean the sound wiggles more times per second than lower frequencies.
         On a waveform, you can see this by how close together the peaks and dips are. If you listen closely, you will hear this in your everyday life.
          A common low frequency sound you might know is a thunder clap. A common high frequency sound you might know is a firetruck siren.`,
        staticFile: "{% static 'Clippy_support/freq.jpg' %}"
    },
    clippypitch: {
        title: "Pitch",
        blurb: `What scientists think of as frequency you probably hear as pitch. Pitch is how high or low a sound seems to your ears. 
        A bird’s song might have a high pitch, while a drumbeat has a low pitch. Keep in mind that pitch is human-specific, so a sound 
        you hear one way, like a crashing wave, might be perceived differently by a marine mammal.`, 
        staticFile: "{% static 'Clippy_support/freq.jpg' %}"
    },
    clippyamplitude: {
        title: "Amplitude",
        blurb: `What scientists call amplitude is what you probably think of as loudness. Sounds with higher amplitude will seem louder, 
        while those with lower amplitude will seem quieter. On a waveform, taller peaks indicate higher amplitude, and shorter peaks indicate 
        lower amplitude. Scientists usually measure amplitude in decibels (dB). Humans can hear sounds as soft as 0 dB, and prolonged 
        exposure to sounds above 70 dB can damage our ears. Do you think marine mammals experience loudness the same way we do?`, 
        staticFile: "{% static 'Clippy_support/amplitude.jpg' %}"
    },
    clippyloops: {
        title: "Repeated Signals",
        blurb: `Many baleen whales sing the same songs over and over again in search of love. Scientists study repeating signals like this
        to understand communication patterns in marine mammals. In the mixer, you can do this too by looping your signal.`,
    }
};

document.querySelectorAll(".clippy-helper").forEach(el => {
    el.addEventListener("click", async () => {
        const id = el.id; // 'waveform' or 'spectrogram'
        const modalEl = document.getElementById("previewClippyModal");
        const modal = new bootstrap.Modal(modalEl);

        // Set title from clippyData
        document.getElementById("previewClippyTitle").textContent = clippyData[id].title;

        // Try loading static file if it exists
        const filePath = clippyStaticFiles[id];
        const bodyEl = document.getElementById("previewClippyBody");

        if (filePath) {
            bodyEl.innerHTML = `
                <p>${clippyData[id].blurb}</p>
                <div class="text-center">
                    <img src="${filePath}" class="img-fluid mt-3" 
                        style="border-radius:5px; max-height:300px; width:auto;">
                </div>
            `;
        } else {
            bodyEl.innerHTML = `<p>${clippyData[id].blurb}</p>`;
        }

        modal.show();
    });
});
document.querySelectorAll(".control-clippy").forEach(el => {
    el.addEventListener("click", async () => {
        const id = el.id; // 'waveform' or 'spectrogram'
        const modalEl = document.getElementById("previewClippyModal");
        const modal = new bootstrap.Modal(modalEl);

        // Set title from clippyData
        document.getElementById("previewClippyTitle").textContent = clippyData[id].title;

        // Try loading static file if it exists
        const filePath = clippyStaticFiles[id];
        const bodyEl = document.getElementById("previewClippyBody");

        if (filePath) {
            bodyEl.innerHTML = `
                <p>${clippyData[id].blurb}</p>
                <div class="text-center">
                    <img src="${filePath}" class="img-fluid mt-3" 
                        style="border-radius:5px; max-height:300px; width:auto;">
                </div>
            `;
        } else {
            bodyEl.innerHTML = `<p>${clippyData[id].blurb}</p>`;
        }

        modal.show();
    });
});
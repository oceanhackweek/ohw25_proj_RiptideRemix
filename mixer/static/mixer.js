const soundStructure = JSON.parse(
    document.getElementById("sound-structure-data").textContent
);

const categorySelect = document.getElementById("categorySelect");
const subcategorySelect = document.getElementById("subcategorySelect");
const speciesSelect = document.getElementById("speciesSelect");
const iconGrid = document.getElementById("iconGrid");

const playBtn = document.getElementById("playClip");
const addBtn = document.getElementById("addToTimeline");

const speed = document.getElementById("speed");
const pitch = document.getElementById("pitch");
const amplitude = document.getElementById("amplitude");
const loops = document.getElementById("loops");

const audio = document.getElementById("audioPlayer");
const timeline = document.getElementById("timeline");

let currentSound = null;
const TIMELINE_SECONDS = 60;

/* ------------------ Dropdown Logic ------------------ */

categorySelect.onchange = () => {
    reset(subcategorySelect, "Subcategory");
    reset(speciesSelect, "Species");
    iconGrid.innerHTML = "";

    const cat = categorySelect.value;
    if (!cat) return;

    subcategorySelect.disabled = false;
    Object.keys(soundStructure[cat]).forEach(k => {
        if (k !== "_files") addOption(subcategorySelect, k);
    });
};

subcategorySelect.onchange = () => {
    reset(speciesSelect, "Species");
    iconGrid.innerHTML = "";

    const { value: cat } = categorySelect;
    const sub = subcategorySelect.value;
    if (!sub) return;

    speciesSelect.disabled = false;
    Object.keys(soundStructure[cat][sub]).forEach(k => {
        if (k !== "_files") addOption(speciesSelect, k);
    });
};

speciesSelect.onchange = () => {
    iconGrid.innerHTML = "";

    const cat = categorySelect.value;
    const sub = subcategorySelect.value;
    const sp = speciesSelect.value;

    if (!sp) return;

    renderIcons(soundStructure[cat][sub][sp]);
};

/* ------------------ Icons ------------------ */

function renderIcons(files) {
    iconGrid.innerHTML = "";

    files.forEach(sound => {
        const div = document.createElement("div");
        div.className = "icon";
        div.innerHTML = `
            <img src="/static/icons/sound.png">
            <small>${sound.display_name}</small>
        `;
        div.onclick = () => selectSound(sound);
        iconGrid.appendChild(div);
    });
}

function selectSound(sound) {
    currentSound = sound;
    audio.src = sound.url;
    loadSpectrogram(sound.url);
}

/* ------------------ Playback ------------------ */

playBtn.onclick = () => {
    if (!currentSound) return alert("Select a sound first");
    audio.playbackRate = speed.value;
    audio.volume = Math.min(amplitude.value / 5, 1);
    audio.play();
};

/* ------------------ Timeline ------------------ */

addBtn.onclick = () => {
    if (!currentSound) return alert("Select a sound first");

    createTimelineClip({
        clip: currentSound.url,
        speed: +speed.value,
        pitch: +pitch.value,
        amplitude: +amplitude.value,
        loops: +loops.value,
        start_time: 0
    });
};

function createTimelineClip(params) {
    const el = document.createElement("div");
    el.className = "clip-block";
    el.textContent = params.clip.split("/").pop();
    el.style.left = "0px";
    el.style.width = (params.loops * 25) + "px";

    timeline.appendChild(el);
    drag(el, params);
}

function drag(el, params) {
    el.onmousedown = e => {
        const shift = e.offsetX;
        document.onmousemove = ev => {
            const r = timeline.getBoundingClientRect();
            let x = ev.clientX - r.left - shift;
            x = Math.max(0, Math.min(x, timeline.clientWidth));
            el.style.left = x + "px";
            params.start_time = Math.round((x / timeline.clientWidth) * TIMELINE_SECONDS);
        };
        document.onmouseup = () => document.onmousemove = null;
    };
}

/* ------------------ Spectrogram ------------------ */

function loadSpectrogram(url) {
    fetch(`/mixer/spectrogram/?audio_url=${encodeURIComponent(url)}`)
        .then(r => r.json())
        .then(d => {
            document.getElementById("spectrogramContainer").innerHTML =
                `<img class="img-fluid" src="data:image/png;base64,${d.spectrogram}">`;
        });
}

/* ------------------ Helpers ------------------ */

function reset(select, label) {
    select.innerHTML = `<option value="">${label}</option>`;
    select.disabled = true;
}

function addOption(select, text) {
    const o = document.createElement("option");
    o.value = text;
    o.textContent = text;
    select.appendChild(o);
}

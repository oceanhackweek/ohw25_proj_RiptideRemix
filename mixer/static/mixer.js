const subcategories = {
    whale: [
        { name: "Orca", file: "/static/audio/orca.wav" },
        { name: "Humpback", file: "/static/audio/humpback.wav" }
    ],
    ice: [
        { name: "Ice Crack", file: "/static/audio/ice.wav" }
    ]
};

const category = document.getElementById("category");
const subcategory = document.getElementById("subcategory");
const iconGrid = document.getElementById("iconGrid");

const editor = document.getElementById("clipEditor");
const audio = document.getElementById("clipAudio");
const spectrogram = document.getElementById("spectrogram");
const title = document.getElementById("clipTitle");

const timeline = document.getElementById("timeline");
const TIMELINE_SECONDS = 60;

let currentClip = null;
let timelineClips = [];

category.onchange = () => {
    subcategory.innerHTML = "";
    iconGrid.innerHTML = "";
    subcategories[category.value]?.forEach((s, i) => {
        const opt = document.createElement("option");
        opt.value = i;
        opt.textContent = s.name;
        subcategory.appendChild(opt);
    });
};

subcategory.onchange = () => {
    iconGrid.innerHTML = "";
    const clip = subcategories[category.value][subcategory.value];

    const div = document.createElement("div");
    div.className = "icon";
    div.innerHTML = `<img src="/static/icons/sound.png"><br>${clip.name}`;
    div.onclick = () => loadClip(clip);
    iconGrid.appendChild(div);
};

function loadClip(clip) {
    currentClip = clip;
    editor.classList.remove("d-none");
    title.textContent = clip.name;
    audio.src = clip.file;

    fetch(`/mixer/spectrogram/?file=${clip.file}`)
        .then(r => r.json())
        .then(d => spectrogram.src = "data:image/png;base64," + d.image);
}

document.getElementById("addToTimeline").onclick = () => {
    const params = {
        clip: currentClip.file,
        speed: +speed.value,
        pitch: +pitch.value,
        amplitude: +amplitude.value,
        loops: +loops.value,
        start_time: 0
    };
    createTimelineClip(params);
};

function createTimelineClip(params) {
    const el = document.createElement("div");
    el.className = "clip-block";
    el.textContent = params.clip.split("/").pop();
    el.style.left = "0px";
    el.style.width = (params.loops * 20) + "px";

    timeline.appendChild(el);
    timelineClips.push({ el, params });

    drag(el, params);
}

function drag(el, params) {
    el.onmousedown = e => {
        const shiftX = e.offsetX;

        document.onmousemove = e => {
            const rect = timeline.getBoundingClientRect();
            let x = e.clientX - rect.left - shiftX;
            x = Math.max(0, Math.min(x, timeline.clientWidth));
            el.style.left = x + "px";
            params.start_time = Math.round((x / timeline.clientWidth) * 60);
        };

        document.onmouseup = () => {
            document.onmousemove = null;
            document.onmouseup = null;
        };
    };
}

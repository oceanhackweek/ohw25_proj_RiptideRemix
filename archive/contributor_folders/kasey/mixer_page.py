import marimo

__generated_with = "0.14.17"
app = marimo.App(
    width="columns",
    app_title="RiptideRemix_mixer",
    layout_file="layouts/mixer_page.grid.json",
)


@app.cell(column=0)
def _():
    import platform
    from pathlib import Path

    # Detect OS and set project root accordingly
    if platform.system() == "Windows":
        basePath = Path("C:/Users/kasey/Desktop/ohw25_proj_RiptideRemix")
    else:
        basePath = Path("/home/jovyan/ohw25_proj_RiptideRemix")
    return (basePath,)


@app.cell
def _(basePath):
    import marimo as mo
    mo.image(
        src= basePath / "Images" / "logo_flat.jpg",
        alt="placeholder",
        width=1200,
        height=100,
        rounded=True,
        caption=""
    )
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Welcome, sound pirate! You’ve just discovered RiptideRemix, a GarageBand for all of your ocean mixing needs. Every clip in the Ocean Sound Library is a piece of the sea’s continual symphony. Start by exploring our available databases and get an idea of what kinds of sounds you could encounter. Add a clip to your library - listen closely and edit it to make it your own. Once you've built up a soundscape, click the MIX! button and listen to your new song. Congrats! Not only are you a sound pirate, you're now a bonafide ocean DJ.""")
    return


@app.cell
def _(mo):
    mo.md("""---""")
    return


@app.cell
def _(basePath, mo):
    mo.image(
        src= basePath / "Images" /  "ArtGifs" / "placeholder.gif",
        alt="placeholder",
        width=900,
        height=200,
        rounded=False,
        caption=""
    )
    return


@app.cell
def _(mo):
    mo.md("""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(basePath, mo):
    mo.image(
        src= basePath / "Images" / "welcome.png",
        alt="placeholder",
        width=115,
        height=115,
        rounded=False,
        caption=""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell
def _(mo):
    mo.md(r"""---""")
    return


@app.cell(column=1)
def _(mo):
    nav_menu = mo.nav_menu({
        "/": "Mix Sounds",  # internal
        "/learn": "Learn More",  # internal
        "/about": "About the Team",  # internal
        "/quake": "Gather More Data"
    })
    nav_menu
    return


@app.cell(column=2)
def _(mo):
    mo.md(r"""## LIBRARY""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Ahoy, explorer! Here lies a treasure chest of the sea’s secrets. Drift through our collection and discover glaciers groaning, icebergs cracking, whales singing their hearts out, and even the occasional mischievous crocodile. Each clip is yours to play with:

    * Speed it up to make it race like a storm or slow it down to let it drift like a lazy current.

    * Shift the frequency to soar into the skies or rumble in the deep.

    * Adjust the amplitude to make it whisper or roar.

    Experiment freely—the ocean has endless voices, and now they’re in your hands. When you’ve crafted the sound just the way you like, click “Add to Song” to weave it into your grand ocean symphony.
    """
    )
    return


@app.cell
def _(mo):
    category_dropdown = mo.ui.dropdown(options={'Seismic Event': 1, 'Cetacean Call': 2, 'Anthropogenic': 3, 'Other': 3}, value = 'Cetacean Call')
    return (category_dropdown,)


@app.cell
def _(mo):
    mo.md(r"""### Choose Your Clip:""")
    return


@app.cell
def _(mo):
    mo.md(r"""Category:""")
    return


@app.cell
def _(mo):
    mo.md(r"""Class:""")
    return


@app.cell
def _(mo):
    mo.md(r"""Subclass:""")
    return


@app.cell
def _(mo):
    mo.md(r"""Clip:""")
    return


@app.cell
def _(category_dropdown):
    category_dropdown
    return


@app.cell
def _(category_dropdown, mo):
    if category_dropdown.selected_key == 'Seismic Event':
        labelopts = {'Japan2011': 1, 'Alaska2021': 2, 'Russia2025': 3}
    elif category_dropdown.selected_key == 'Cetacean Call':
        labelopts = {'Mysticetes': 1, 'Odontocetes': 2} # replace with available_wavs/cetacean
    elif category_dropdown.selected_key == 'Anthropogenic':
        labelopts = {"All": 1}
    else:
        labelopts = {"All": 1} # replace with available_wavs/other

    class_dropdown = mo.ui.dropdown(options=labelopts)
    class_dropdown
    return (class_dropdown,)


@app.cell
def _(basePath, category_dropdown, class_dropdown, mo, os):
    if category_dropdown.selected_key == 'Cetacean Call':
        sc_path = basePath / "Library" / "Cetacean" / class_dropdown.selected_key
        sc_list = os.listdir(sc_path)
        sc_dict = {sc_list[i]: i for i in range(len(sc_list))}
    elif category_dropdown.selected_key == 'Seismic Event':
        sc_dict = {"All": 1}
    else:
        sc_dict = {"All": 1}
    sc_dropdown = mo.ui.dropdown(options=sc_dict)
    return (sc_dropdown,)


@app.cell
def _(sc_dropdown):
    sc_dropdown
    return


@app.cell
def _(basePath, category_dropdown, class_dropdown, os, sc_dropdown):
    if category_dropdown.selected_key == 'Cetacean Call':
        clips_path = basePath / "Library" / "Cetacean" / class_dropdown.selected_key / sc_dropdown.selected_key
        clip_list = os.listdir(clips_path)
    elif category_dropdown.selected_key == 'Seismic Event':
        clips_path = basePath / "Library" / "Seismic" / class_dropdown.selected_key
        clip_list = os.listdir(clips_path)
    elif category_dropdown.selected_key == 'Anthropogenic':
        clips_path = basePath / "Library" / "Anthropogenic"
        clip_list = os.listdir(clips_path)
    else:
        clips_path = basePath / "Library" / "Other"
        clip_list = os.listdir(clips_path)
    return clip_list, clips_path


@app.cell
def _(clip_list, mo):
    clip_dict = {clip_list[i]: i for i in range(len(clip_list))}
    clip_dropdown = mo.ui.dropdown(options=clip_dict)
    clip_dropdown
    return (clip_dropdown,)


@app.cell
def _(clip_dropdown, clips_path, os):
    selected_audio = os.path.join(clips_path, clip_dropdown.selected_key)
    return


@app.cell
def _(mo):
    button_preview = mo.ui.run_button(label="Update preview")
    button_preview
    return (button_preview,)


@app.cell
def _(
    audio_selected,
    button_preview,
    ipd,
    np,
    process_one_clip_to_add,
    slider_amp,
    slider_loops,
    slider_pitch,
    slider_speed,
    slider_t,
):
    if button_preview.value and audio_selected:
        print(
            audio_selected,
            slider_t.value,
            slider_loops.value,
            slider_amp.value,
            slider_pitch.value,
            slider_speed.value
        )
        sr_clip, d_clip = process_one_clip_to_add(
            audio_selected,
            slider_t.value,
            slider_loops.value,
            slider_amp.value,
            slider_pitch.value,
            slider_speed.value
        )
        if np.max(np.abs(d_clip)) > 0:
            d_clip = d_clip / np.max(np.abs(d_clip))

        ipd.display(ipd.Audio(data=d_clip, rate=sr_clip))
    return


@app.cell
def _():
    # Keep this for displaying wave form, spectrogram, and explanation of clip
    # stretch goal for educational piece
    # button_libraryadd = mo.ui.run_button(label='Explore this sound')
    # button_libraryadd
    return


@app.cell
def _(d_final, plot_waveform, sr_resampled):
    fig = plot_waveform(d_final, sr_resampled)
    fig
    return


@app.cell
def _(d_final, plot_spectrogram, sr_selected):
    fig2 = plot_spectrogram(d_final, sr_selected)
    fig2
    return


@app.cell(column=3)
def _(mo):
    mo.md(r"""## Clip Editor""")
    return


@app.cell
def _(slider_amp, slider_loops, slider_pitch, slider_speed, slider_t):
    start_time = slider_t.value
    ptch = slider_pitch.value
    spd = slider_speed.value
    # ptch_speed = slider_speed.value
    loops = slider_loops.value # slider_f.value
    loudness = slider_amp.value

    return loops, loudness, ptch, spd, start_time


@app.cell
def _(mo):
    # start time
    slider_t = mo.ui.slider(0, 20.0, label='Time in Song (s)')
    slider_t
    return (slider_t,)


@app.cell
def _(mo):
    # ptch_spd
    slider_speed = mo.ui.slider(0, 2, .1, label='Speed', value=1)
    slider_speed
    return (slider_speed,)


@app.cell
def _(mo):
    # reporpoise
    slider_pitch = mo.ui.slider(0, 2, .1, label='Pitch', value=1)
    slider_pitch
    return (slider_pitch,)


@app.cell
def _(mo):
    # loudness
    slider_amp = mo.ui.slider(0, 2, .1, label='Amplitude (dB)', value=1)
    slider_amp
    return (slider_amp,)


@app.cell
def _(mo):
    # loops
    slider_loops = mo.ui.slider(0, 15, 1, label='Loops', value=1)
    slider_loops
    return (slider_loops,)


@app.cell
def _(mo):
    # Add to mix
    button_add_clip = mo.ui.run_button(label="Add Clip")
    button_add_clip
    return (button_add_clip,)


@app.cell
def _(
    audio_selected,
    button_add_clip,
    clips_to_add,
    slider_amp,
    slider_loops,
    slider_pitch,
    slider_speed,
    slider_t,
):
    if button_add_clip.value and audio_selected:
        clips_to_add.loc[len(clips_to_add)] = [
            audio_selected,
            slider_t.value,
            slider_loops.value,
            slider_amp.value,
            slider_pitch.value,
            slider_speed.value
        ]
        print(f"Added clip to mix: {audio_selected}")
    return


@app.cell
def _(mo):
    mo.md(r"""### Acoustic Modifiers""")
    return


@app.cell
def _(build_mix_array, button_play_mix, clips_to_add, ipd):
    if button_play_mix.value and len(clips_to_add) > 0:
        sr_mix, mix_data_array = build_mix_array(clips_to_add)
        clips_to_add.drop(clips_to_add.index, inplace=True)
        clips_to_add.reset_index(drop=True, inplace=True)
        ipd.display(ipd.Audio(mix_data_array, rate=sr_mix))
    return


@app.cell(column=4)
def _(mo):
    mo.md(r"""##FINAL SONG""")
    return


@app.cell
def _(mo):
    mo.md(r"""Here’s where your ocean melody comes together. Watch your creation take shape through the waveform (the rolling tides of your song) and the spectrogram (a colorful map of its hidden patterns). Layer, blend, and fine-tune until your composition feels just right. When your symphony is complete, click “Export” to set it free.""")
    return


@app.cell
def _(mo):
    # a button that when clicked will have its value set to True;
    # any cells referencing that button will automatically run.
    button_export = mo.ui.run_button(label='Export file')
    button_export
    return (button_export,)


@app.cell
def _(clips_to_add, np, plt, wavfile):
    def plot_clips(clips_to_add):
        fig, ax = plt.subplots(figsize=(12, 3))
        num_clips = len(clips_to_add)

        if num_clips == 0:
            ax.set_title("Your New Song (Nothing Added Yet)")
            ax.set_xlabel("Time [s]")
            ax.set_ylabel("Amplitude")
            ax.set_xticks([])
            ax.set_yticks([])
            return fig
        colors = plt.cm.tab10(np.linspace(0, 1, num_clips))  # distinct colors

        for i, (idx, row) in enumerate(clips_to_add.iterrows()):
            clip_path = row[0]  # Assuming first column is audio file path
            sr, data = wavfile.read(clip_path)

            # Convert stereo -> mono if needed
            if len(data.shape) > 1:
                data = data.mean(axis=1)

            time = np.arange(len(data)) / sr
            ax.plot(time, data, color=colors[i], label=f"Clip {i+1}")

        ax.set_title("Your New Song")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        ax.set_xlim(0, 30)
        ax.legend()
        ax.grid(alpha=0.3)
        fig.tight_layout()
        return fig

    fig3 = plot_clips(clips_to_add)
    fig3
    return


@app.cell
def _(clips_to_add, np, plt, spectrogram, wavfile):
    def plot_combined_spectrogram(clips_to_add):
        # Handle empty clips case
        if clips_to_add.empty:
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.set_title("Your New Song (Nothing Added Yet)")
            ax.set_xticks([])
            ax.set_yticks([])
            return fig

        combined_audio = []
        sr = None

        # Load all clips and concatenate
        for idx, row in clips_to_add.iterrows():
            clip_path = row[0]  # Assuming first column is audio path
            clip_sr, data = wavfile.read(clip_path)

            # Handle stereo -> mono
            if len(data.shape) > 1:
                data = data.mean(axis=1)

            # Ensure sample rates are consistent
            if sr is None:
                sr = clip_sr
            elif sr != clip_sr:
                raise ValueError(f"Sample rate mismatch: expected {sr}, got {clip_sr}")

            combined_audio.append(data)

        # Combine into one array
        combined_audio = np.concatenate(combined_audio)

        # Compute spectrogram
        f, t, Sxx = spectrogram(combined_audio, fs=sr, nperseg=1024, noverlap=512)

        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        im = ax.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading="auto", cmap="magma")
        fig.colorbar(im, ax=ax, label="Power (dB)")
        ax.set_title("Your New Song")
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Frequency [Hz]")
        ax.set_ylim(0, sr / 2)  # Nyquist limit

        fig.tight_layout()
        return fig
    fig4 = plot_combined_spectrogram(clips_to_add)
    fig4
    return


@app.cell
def _(mo):
    # Play full mix
    button_play_mix = mo.ui.run_button(label="Hear Full Mix")
    button_play_mix
    return (button_play_mix,)


@app.cell
def _(button_export, clips_to_add, combine_clips, finalwav):
    if button_export.value:
        final_wavPath, final_wav = combine_clips(clips_to_add)
        final_mp3 = finalwav.export_to_mp3(final_wavPath)
        print("Exported mix to:", final_mp3)
    return


@app.cell
def _(basePath, mo):

    mo.image(
        src= basePath / "Images" / "bunda-feia-cute.gif",
        alt="placeholder",
        width=300,
        height=300,
        rounded=True,
        caption=""
    )
    return


@app.cell(column=5)
def _(basePath, mo):
    mo.image(
        src=  basePath / "Images" / "logo.png",
        alt="Logo",
        width=100,
        height=100,
        rounded=True,
        caption=""
    )
    return


@app.cell
def _(mo):
    mo.md(r"""Thanks for your RiptideRemix! Your journey through sound has brought together whispers, rumbles, and songs of the sea. We’re so glad you set sail with us. Now take your creation, share it, and let it ripple out into the world.""")
    return


@app.cell
def _(mo):
    mo.md(r"""Derya""")
    return


@app.cell
def _(mo):
    mo.md(r"""Mattie""")
    return


@app.cell
def _(mo):
    mo.md(r"""Isabelle""")
    return


@app.cell
def _(mo):
    mo.md(r"""Kasey""")
    return


@app.cell
def _(mo):
    mo.md(r"""Oluwatofunmi""")
    return


@app.cell
def _(mo):
    mo.md(r"""Dwight""")
    return


@app.cell(column=6)
def _(mo):
    mo.md(r"""# Underlying Python functions""")
    return


@app.cell
def _():
    return


@app.cell
def _():
    import pandas as pd
    import ffmpeg

    import glob
    import os
    import shutil
    import librosa

    import IPython.display as ipd
    from scipy.io import wavfile
    from scipy import signal

    from pydub import AudioSegment
    from scipy.signal import resample
    from pydub.effects import speedup
    return ipd, librosa, os, pd, signal, wavfile


@app.cell
def _(np, process_one_clip_to_add):
    def build_mix_array(mix_clips, sr=44100, duration=30):
        """
        Combine all clips in mix_clips into a single audio array.
        Each row should have: 'clip', 'start_time', 'loops', 'loudness', 'pitch', 'speed'
        """
        mix_array = np.zeros(duration * sr, dtype=np.float32)

        for _, row in mix_clips.iterrows():
            sr_clip, clip_data = process_one_clip_to_add(
                row['clip'],
                row['start_time'],
                row['loops'],
                row['loudness'],
                row['pitch'],
                row['speed'],
                gen_sr=sr,
                max_len=duration
            )

            # Ensure clip fits in the mix
            if len(clip_data) > len(mix_array):
                clip_data = clip_data[:len(mix_array)]
            mix_array[:len(clip_data)] += clip_data

        # Normalize
        if np.max(np.abs(mix_array)) > 0:
            mix_array = mix_array / np.max(np.abs(mix_array))

        return sr, mix_array
    return (build_mix_array,)


@app.cell
def _(np, plt):
    from scipy.signal import spectrogram

    def plot_spectrogram(audio_data, sr):
        if audio_data.ndim > 1:
            audio_data = audio_data[:, 0]

        # Compute spectrogram
        frequencies, time_segments, Sxx = spectrogram( audio_data, fs=sr, nperseg=1024, noverlap=256, scaling="spectrum")

        # Convert power to dB
        Sxx_dB = 10 * np.log10(Sxx + 1e-10)

        # Create figure and plot
        fig, ax = plt.subplots(figsize=(10, 3))
        pcm = ax.pcolormesh( time_segments, frequencies, Sxx_dB, shading="gouraud", cmap="viridis", vmin=-99)
        fig.colorbar(pcm, ax=ax, label="Intensity [dB]")
        ax.set_ylabel("Frequency [Hz]")
        ax.set_xlabel("Time [s]")
        ax.set_ylim(0, sr / 2)
        plt.tight_layout()

        return fig
    return plot_spectrogram, spectrogram


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt

    def plot_waveform(audio_data, sr):
        # Handle stereo: take first channel if needed
        if audio_data.ndim > 1:
            audio_data = audio_data[:, 0]

        # Normalize amplitude to [-1, 1]
        audio_data = audio_data.astype(np.float32)
        audio_data /= np.max(np.abs(audio_data))

        # Time axis in seconds
        duration = len(audio_data) / sr
        times = np.linspace(0, duration, len(audio_data))

        # Create the figure
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(times, audio_data, color="steelblue", linewidth = 0.2)
        ax.set_xlim(0, duration)
        ax.set_ylim(-1.1, 1.1)
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Amplitude")
        ax.grid(alpha=0.3)
        plt.tight_layout()

        # For Marimo / Jupyter, returning fig allows inline display
        return fig
    return np, plot_waveform, plt


@app.cell
def _(basePath, wavfile):
    workingWavPath = basePath / "data" / "workingwav" / 'mysong.wav'
    sr_base, d_base = wavfile.read(workingWavPath)
    return


@app.cell
def _(librosa, np, signal, wavfile):
    def process_one_clip_to_add(clip, start_time, loop_val, loud_val, ptch_val, spd_val, gen_sr=44100, max_len=30):
        max_len = gen_sr * max_len
        print("NEXT FILE____________________________")
        sr, d = wavfile.read(clip)
        if len(d.shape) > 1:
            d = d.mean(axis=1)
        if np.max(np.abs(d)) != 0: d = d / np.max(np.abs(d))  # Normalize the amplitudes

        print("The raw sampling rate and length are: ", sr, len(d))

        # Modify sampling rate to match the file we are building on
        if sr != 44100:
            ratio = 44100 / sr
            d = signal.resample(d, int(len(d) * ratio))        # Use Fourier method for better quality
            sr = 44100

        # Loop
        sr_looped, d_looped = loop(sr, d, loop_val)
        print("Length of looped file: ", len(d_looped))

        # Loudness
        sr_loop_amp, d_loop_amp = loud(sr_looped, d_looped, loud_val)

        # Pitch
        sr_loop_amp_p, d_loop_amp_p = pitch(sr_loop_amp, d_loop_amp, ptch_val)

        # Speed
        sr_loop_amp_p_s, d_loop_amp_p_s = speed(sr_loop_amp_p, d_loop_amp_p, spd_val)

        sr = sr_loop_amp_p_s
        d = d_loop_amp_p_s

        # Length and start time adjustment
        start_chunk_len = int(start_time * sr)   # <-- Convert to int
        strt_zero_chunk = np.zeros(start_chunk_len)
        padded_d = np.concatenate((strt_zero_chunk, d))

        if len(padded_d) > 2646000: d = padded_d[:2646000]
        elif len(padded_d) < 2646000: d = np.append(padded_d, np.zeros(2646000 - len(padded_d)))
        else: d = padded_d

        return sr, d


    def loop(sr, d, num_loops):
        d_looped = np.tile(d, num_loops)
        sr_looped = sr
        return sr_looped, d_looped


    def loud(sr, d, loud_val):
        d_amp = d * loud_val
        sr_amp = sr
        return sr_amp, d_amp

    def pitch(sr, d, factor):
        d_pitched = librosa.effects.pitch_shift(y=d, sr=sr, n_steps=factor)
        sr_pitched = sr
        return sr_pitched, d_pitched

    def speed(sr, d, factor):
        d_sped = librosa.effects.time_stretch(d, rate=factor)
        sr_sped = sr
        return sr_sped, d_sped
    return (process_one_clip_to_add,)


@app.cell
def _(basePath, np, process_one_clip_to_add, wavfile):
    def combine_clips(clips_to_add, output_wav="my_final_song.wav", sr=44100, duration=60):
        """
        Combine all clips from the clips_to_add DataFrame into one overlapping mix.
        - Each row in clips_to_add contains: clip name, start_time, loops, loudness, pitch, speed
        - Mix length is fixed by duration (seconds).
        """
        owp = basePath / output_wav
        total_samples = sr * duration
        final_mix = np.zeros(total_samples, dtype=np.float32)

        for _, row in clips_to_add.iterrows():
            sr_clip, d_clip = process_one_clip_to_add(
                row['clip'],
                row['start_time'],
                row['loops'],
                row['loudness'],
                row['pitch'],
                row['speed'],
                gen_sr=sr,
                max_len=duration
            )

            # Align this clip in time
            start_sample = int(float(row['start_time']) * sr)
            end_sample = start_sample + len(d_clip)

            if start_sample < total_samples:
                # Clip if it runs off the end
                end_sample = min(end_sample, total_samples)
                clip_segment = d_clip[:end_sample - start_sample]
                final_mix[start_sample:end_sample] += clip_segment.astype(np.float32)

        # Normalize to prevent clipping
        if np.max(np.abs(final_mix)) > 0:
            final_mix /= np.max(np.abs(final_mix))

        wavfile.write(owp, sr, final_mix)
        return owp, final_mix

    return (combine_clips,)


@app.cell
def _(np, pd, wavfile):
    # clear audio
    sample_rate = 44100
    duration = 10
    empty_audio = np.zeros(int(sample_rate * duration), dtype=np.float32)
    clips_to_add = pd.DataFrame(columns=['clip', 'start_time', 'loops', 'loudness', 'pitch', 'speed'])

    wavfile.write('my_song.wav', sample_rate, empty_audio)
    print("The original empty song file is length: ", len(empty_audio))
    print(clips_to_add)
    return (clips_to_add,)


@app.cell
def _(clip_dropdown, clips_path, os):
    os.path.join(clips_path, clip_dropdown.selected_key)
    return


@app.cell
def _(
    clip_dropdown,
    clips_path,
    librosa,
    loops,
    loudness,
    np,
    os,
    ptch,
    signal,
    spd,
    wavfile,
):
    ## SELECT YOUR CLIP:
    audio_selected = os.path.join(clips_path, clip_dropdown.selected_key)
    sr_selected, d_selected = wavfile.read(audio_selected)
    d_selected = d_selected / np.max(np.abs(d_selected))

    # Modify sampling rate to match the file we are building on
    if sr_selected != 44100:
        ratio = 44100 /sr_selected
        d_resampled = signal.resample(d_selected, int(len(d_selected) * ratio))        # Use Fourier method for better quality
        sr_resampled = 44100
    else:
        d_resampled = d_selected
        sr_resampled = sr_selected

    d_looped = np.tile(d_resampled, loops)
    d_louded = d_looped * loudness
    d_pitched = librosa.effects.pitch_shift(y=d_louded, sr=sr_resampled, n_steps=ptch)
    d_final = librosa.effects.time_stretch(d_pitched, rate=spd)
    return audio_selected, d_final, sr_resampled, sr_selected


@app.cell
def _(audio_selected, clips_to_add, loops, loudness, ptch, spd, start_time):
    clips_to_add.loc[len(clips_to_add)] = [audio_selected, start_time, loops, loudness, ptch, spd]
    return


@app.cell
def _(patches, plt):
    def plot_time_freq_boxes(boxes,
                             time_range=(0, 60),
                             freq_range=(0, 20000)):
        """
        Plot time-frequency boxes on a 2D plot with labels and colors.

        Parameters
        ----------
        boxes : list of tuples
            Each tuple = (t_start, t_end, f_start, f_end, label)
        time_range : tuple
            (min_time, max_time) for x-axis
        freq_range : tuple
            (min_freq, max_freq) for y-axis
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_facecolor("black")  # black background

        for (t_start, t_end, f_start, f_end, label) in boxes:
            # Pick color based on label
            if label.lower() == "seismic":
                facecolor = "deeppink"
                edgecolor = "hotpink"
            elif label.lower() == "whale":
                facecolor = "purple"
                edgecolor = "violet"
            else:
                facecolor = "gray"
                edgecolor = "lightgray"

            # Draw box
            rect = patches.Rectangle(
                (t_start, f_start),
                t_end - t_start,
                f_end - f_start,
                linewidth=1.5, edgecolor=edgecolor, facecolor=facecolor, alpha=0.8
            )
            ax.add_patch(rect)

            # Add label text at the center of the box
            # ax.text(
            #     (t_start + t_end) / 2,
            #     (f_start + f_end) / 2,
            #     label,
            #     color="white", ha="center", va="center", fontsize=9, weight="bold"
            # )

        # Set limits and labels
        ax.set_xlim(time_range)
        ax.set_ylim(freq_range)
        ax.set_xlabel("Time (s)", color="Purple")
        ax.set_ylabel("Frequency (Hz)", color="Purple")
        ax.set_title("MY SONG", color="Purple")

        # White ticks
        ax.tick_params(colors="white")

        return fig


    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

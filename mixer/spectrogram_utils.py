import os
import io
import base64
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from pydub import AudioSegment
from django.conf import settings  # assuming you’re using Django
import librosa
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.core.cache import cache
import hashlib
from PIL import Image


def generate_spectrogram(audio_data, sr):
    try:
        #CHANGE: Data comes from cache pre-calculated so just need to plot
        # Generate spectrogram
        nperseg = 256
        noverlap = nperseg // 2
        frequencies, times, spectrogram = signal.spectrogram(
            audio_data,
            fs=sr,
            nperseg=nperseg,
            noverlap=noverlap,
            scaling='density'
        )
        # Convert to dB scale
        spectrogram_db = 20 * np.log10(np.sqrt(spectrogram) + 1e-10)
         
        # Plot
        fig = Figure(figsize=(10, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        pcm = ax.pcolormesh(times, frequencies, spectrogram_db, shading='gouraud', cmap='cividis')

        ax.set_ylabel('Frequency (Hz)')
        ax.set_xlabel('Time (s)')
        ax.set_title('Audio Spectrogram')
        fig.colorbar(pcm, ax=ax, label='Sound Pressure Level (dB)')

        fig.tight_layout()

        buffer = io.BytesIO()
        canvas.print_png(buffer)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return image_base64

    except Exception as e:
        print(f"Error generating spectrogram: {e}")
        return None

def generate_timeseries(audio_data, sr):
    """
    Generates a base64 waveform image (timeseries) from an audio array.
    Supports WAV, MP3, and common audio formats.
    Applies speed, pitch, and amplitude adjustments safely.
    """
    try:
        # Generate time axis
        times = np.arange(len(audio_data)) / sr

        # Plot waveform
        fig = Figure(figsize=(12, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        ax.plot(times, audio_data, color='royalblue')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Audio Waveform')

        fig.tight_layout()

        buffer = io.BytesIO()
        canvas.print_png(buffer)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return image_base64

    except Exception as e:
        print(f"Error generating timeseries: {e}")
        return None

def pitch_shift_hz(audio_data, sample_rate, pitch_hz, reference_freq=440):
    """
    Convert Hz slider to semitones and apply librosa pitch shift.
    pitch_hz: positive or negative slider value
    """
    if pitch_hz == 0:
        return audio_data

    # Convert Hz to semitones
    target_freq = reference_freq + pitch_hz
    target_freq = max(1, target_freq)  # prevent negative frequencies
    n_steps = 12 * np.log2(target_freq / reference_freq)

    # Apply librosa pitch shift safely
    return librosa.effects.pitch_shift(audio_data, sr=sample_rate, n_steps=n_steps)

def get_audio_file_path(url_path):
    # Convert URL path to filesystem path, remove /static/ prefix if present
    if url_path.startswith('/static/'):
        relative_path = url_path[8:]  # Remove '/static/'
    elif url_path.startswith('static/'):
        relative_path = url_path[7:]  # Remove 'static/'
    else:
        relative_path = url_path

    possible_paths = [
        os.path.join(settings.BASE_DIR, 'static', relative_path),
        os.path.join(settings.BASE_DIR, relative_path),
        os.path.join(settings.STATIC_ROOT, relative_path) if settings.STATIC_ROOT else None,
    ]

    for path in possible_paths:
        if path and os.path.exists(path):
            return path

    raise FileNotFoundError(f"Audio file not found: {url_path}")

def timeSeriesForSongSlider(audio_data, sr, category=None):
    """
    Generate a small, clean, transparent waveform image (base64 PNG)
    for use as a repeating tile in the song slider.
    No axes, labels, or background.
    """
    CATEGORY_COLORS = {
        'Anthropogenic': "#57f011",
        'Environmental': "#0ebfff",
        'Biological': "#edc526",
    }
    try:
        # Generate a small waveform snippet — e.g. first 0.5 seconds or so
        times = np.arange(len(audio_data)) / sr

        # Plot waveform with no axes, transparent background
        line_color = CATEGORY_COLORS.get(category, '#000000')
        fig = Figure(figsize=(3, 0.4), dpi=100)  # ~300x40 px
        canvas = FigureCanvas(fig)
        ax = fig.add_axes([0, 0, 1, 1])

        ax.plot(times, audio_data, color=line_color, linewidth=1)
        ax.set_axis_off()
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        fig.tight_layout(pad=0)

        buffer = io.BytesIO()
        canvas.print_png(buffer)
        buffer.seek(0)
        buffer.seek(0)
        img = Image.open(buffer).convert("RGBA")

        data = np.array(img)
        alpha = data[:, :, 3]

        # Find non-transparent bounds
        rows = np.where(alpha.max(axis=1) > 0)[0]
        cols = np.where(alpha.max(axis=0) > 0)[0]

        if rows.size and cols.size:
            cropped = img.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
        else:
            cropped = img  # fallback

        out = io.BytesIO()
        cropped.save(out, format="PNG")
        out.seek(0)

        image_base64 = base64.b64encode(out.getvalue()).decode("utf-8")
        return image_base64


    except Exception as e:
        print(f"Error generating timeseries for slider: {e}")
        return None
    
def load_clip_audio(audio_path, max_duration=60):
    """
    Load WAV or MP3 and return normalized float32 array and sample rate.
    Clip to max_duration (seconds).
    """
    d, sr = librosa.load(audio_path, sr=22050, mono=True)
    max_samples =  int(sr*max_duration)
    
    if len(d) > max_samples:
        d = d[:max_samples]
    
    return d, sr


#Added Caching to speedup 
CACHE_TIMEOUT = 60 * 60

def safe_cache_key(prefix, *parts):
    raw = "|".join(str(p) for p in parts)
    digest = hashlib.md5(raw.encode()).hexdigest()
    return f"{prefix}:{digest}"

#Enable caching of audio
def get_cached_audio(audio_url, speed=1.0, pitch=0, amplitude=1.0):
    """
    Load and process audio once per request, cache it for reuse
    """
    key = safe_cache_key("audio", audio_url, speed, pitch, amplitude)
    cached = cache.get(key)
    if cached:
        return cached  # (audio_data, sample_rate)

    audio_path = get_audio_file_path(audio_url)
    audio_data, sr = load_clip_audio(audio_path)

    # Apply speed
    if speed != 1.0:
        audio_data = librosa.effects.time_stretch(audio_data, rate=speed)

    # Apply pitch
    if pitch != 0:
        audio_data = pitch_shift_hz(audio_data, sr, pitch)

    # Apply amplitude
    audio_data *= amplitude

    cache.set(key, (audio_data, sr), CACHE_TIMEOUT)
    return audio_data, sr
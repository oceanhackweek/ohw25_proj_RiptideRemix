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


def generate_spectrogram(audio_path, speed=1.0, pitch=0, amplitude=1.0):
    try:
        # Resolve path
        if not os.path.exists(audio_path):
            static_path = os.path.join(settings.BASE_DIR, 'static', audio_path.lstrip('/'))
            if os.path.exists(static_path):
                audio_path = static_path
            else:
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Load audio
        ext = os.path.splitext(audio_path)[1].lower()
        if ext == '.mp3':
            audio = AudioSegment.from_file(audio_path, format="mp3")
            audio_data = np.array(audio.get_array_of_samples()).astype(np.float32)
            audio_data /= np.iinfo(audio.array_type).max  # normalize
            if audio.channels > 1:
                audio_data = audio_data.reshape((-1, audio.channels)).mean(axis=1)
            sample_rate = audio.frame_rate
            max_duration_sec = 10
            if len(audio_data) / sample_rate > max_duration_sec:
                audio_data = audio_data[: int(sample_rate * max_duration_sec)]
        else:
            sample_rate, audio_data = wavfile.read(audio_path)
            if len(audio_data.shape) > 1:
                audio_data = audio_data.mean(axis=1)
            audio_data = audio_data.astype(np.float32)
            audio_data /= np.max(np.abs(audio_data))  # normalize

        # Apply amplitude scaling
        audio_data *= amplitude

        # Apply speed (resample)
        if speed != 1.0:
            new_length = int(len(audio_data) / speed)
            indices = np.linspace(0, len(audio_data) - 1, new_length)
            audio_data = np.interp(indices, np.arange(len(audio_data)), audio_data)

        # Apply pitch (frequency scaling)
        if pitch != 0:
            audio_data = pitch_shift_hz(audio_data, sample_rate, pitch)

        # Generate spectrogram
        nperseg = 256
        noverlap = nperseg // 2
        frequencies, times, spectrogram = signal.spectrogram(
            audio_data,
            fs=sample_rate,
            nperseg=nperseg,
            noverlap=noverlap,
            scaling='density'
        )

        # Convert to dB scale
        spectrogram_db = 10 * np.log10(spectrogram + 1e-10)

        # Plot
        fig = Figure(figsize=(10, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        pcm = ax.pcolormesh(times, frequencies, spectrogram_db, shading='gouraud', cmap='cividis')

        ax.set_ylabel('Frequency (Hz)')
        ax.set_xlabel('Time (s)')
        ax.set_title('Audio Spectrogram')
        fig.colorbar(pcm, ax=ax, label='Intensity (dB)')

        fig.tight_layout()

        buffer = io.BytesIO()
        canvas.print_png(buffer)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return image_base64

    except Exception as e:
        print(f"Error generating spectrogram: {e}")
        return None

def generate_timeseries(audio_path, speed=1.0, pitch=0, amplitude=1.0):
    """
    Generates a base64 waveform image (timeseries) from an audio file.
    Supports WAV, MP3, and common audio formats.
    Applies speed, pitch, and amplitude adjustments safely.
    """
    try:
        # Resolve path
        if not os.path.exists(audio_path):
            static_path = os.path.join(settings.BASE_DIR, 'static', audio_path.lstrip('/'))
            if os.path.exists(static_path):
                audio_path = static_path
            else:
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

        ext = os.path.splitext(audio_path)[1].lower()

        # Load audio
        if ext == '.mp3':
            audio = AudioSegment.from_file(audio_path, format="mp3")
            audio_data = np.array(audio.get_array_of_samples()).astype(np.float32)
            audio_data /= np.iinfo(audio.array_type).max  # normalize
            if audio.channels > 1:
                audio_data = audio_data.reshape((-1, audio.channels)).mean(axis=1)
            sample_rate = audio.frame_rate
            max_duration_sec = 10
            if len(audio_data) / sample_rate > max_duration_sec:
                audio_data = audio_data[: int(sample_rate * max_duration_sec)]
        else:
            sample_rate, audio_data = wavfile.read(audio_path)
            if len(audio_data.shape) > 1:
                audio_data = audio_data.mean(axis=1)
            audio_data = audio_data.astype(np.float32)
            audio_data /= np.max(np.abs(audio_data))  # normalize

        # Apply amplitude scaling
        audio_data *= amplitude

        # Apply speed (resample)
        if speed != 1.0:
            new_length = int(len(audio_data) / speed)
            indices = np.linspace(0, len(audio_data) - 1, new_length)
            audio_data = np.interp(indices, np.arange(len(audio_data)), audio_data)

        # Apply pitch safely using librosa
        if pitch != 0:
            audio_data = pitch_shift_hz(audio_data, sample_rate, pitch)

        # Generate time axis
        times = np.arange(len(audio_data)) / sample_rate

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

def timeSeriesForSongSlider(audio_path, speed=1.0, pitch=0, amplitude=1.0, category=None):
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
        # Resolve and load audio (reuse your existing logic)
        if not os.path.exists(audio_path):
            static_path = os.path.join(settings.BASE_DIR, 'static', audio_path.lstrip('/'))
            if os.path.exists(static_path):
                audio_path = static_path
            else:
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

        ext = os.path.splitext(audio_path)[1].lower()

        if ext == '.mp3':
            audio = AudioSegment.from_file(audio_path, format="mp3")
            audio_data = np.array(audio.get_array_of_samples()).astype(np.float32)
            audio_data /= np.iinfo(audio.array_type).max
            if audio.channels > 1:
                audio_data = audio_data.reshape((-1, audio.channels)).mean(axis=1)
            sample_rate = audio.frame_rate
            max_duration_sec = 10
            if len(audio_data) / sample_rate > max_duration_sec:
                audio_data = audio_data[: int(sample_rate * max_duration_sec)]
        else:
            sample_rate, audio_data = wavfile.read(audio_path)
            if len(audio_data.shape) > 1:
                audio_data = audio_data.mean(axis=1)
            audio_data = audio_data.astype(np.float32)
            audio_data /= np.max(np.abs(audio_data))

        audio_data *= amplitude

        if speed != 1.0:
            new_length = int(len(audio_data) / speed)
            indices = np.linspace(0, len(audio_data) - 1, new_length)
            audio_data = np.interp(indices, np.arange(len(audio_data)), audio_data)

        if pitch != 0:
            audio_data = pitch_shift_hz(audio_data, sample_rate, pitch)

        # Generate a small waveform snippet — e.g. first 0.5 seconds or so
        snippet_duration = 0.5  # seconds
        snippet_samples = int(snippet_duration * sample_rate)
        snippet_data = audio_data[:snippet_samples]
        times = np.arange(len(snippet_data)) / sample_rate

        # Plot waveform with no axes, transparent background
        line_color = CATEGORY_COLORS.get(category, '#000000')
        fig = Figure(figsize=(3, 0.4), dpi=100)  # ~300x40 px
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        ax.plot(times, snippet_data, color=line_color, linewidth=1)
        ax.set_axis_off()
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')

        fig.tight_layout(pad=0)

        buffer = io.BytesIO()
        canvas.print_png(buffer)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return image_base64

    except Exception as e:
        print(f"Error generating timeseries for slider: {e}")
        return None
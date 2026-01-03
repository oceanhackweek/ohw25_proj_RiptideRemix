# mixer/spectrogram_utils.py
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import io
import base64
import os
from django.conf import settings


def generate_spectrogram(audio_path, speed, pitch, amplitude):
    try:
        if not os.path.exists(audio_path):
            static_path = os.path.join(settings.BASE_DIR, 'static', audio_path.lstrip('/'))
            if os.path.exists(static_path):
                audio_path = static_path
            else:
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

        sample_rate, audio_data = wavfile.read(audio_path)
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)

        # Apply amplitude scaling
        audio_data = audio_data * amplitude

        # Apply speed (resample)
        if speed != 1.0:
            new_length = int(len(audio_data) / speed)
            indices = np.linspace(0, len(audio_data) - 1, new_length)
            audio_data = np.interp(indices, np.arange(len(audio_data)), audio_data)

        # Apply pitch (frequency scaling)
        if pitch != 0:
            factor = 2 ** (pitch / 12.0)
            new_length = int(len(audio_data) * factor)
            indices = np.linspace(0, len(audio_data) - 1, new_length)
            audio_data = np.interp(indices, np.arange(len(audio_data)), audio_data)

        # Generate spectrogram
        nperseg = 256  # Length of each segment
        noverlap = nperseg // 2  # Overlap between segments

        frequencies, times, spectrogram = signal.spectrogram(
            audio_data,
            fs=sample_rate,
            nperseg=nperseg,
            noverlap=noverlap,
            scaling='density'
        )

        # Convert to dB scale
        spectrogram_db = 10 * np.log10(spectrogram + 1e-10)  # Add small value to avoid log(0)

        plt.figure(figsize=(10, 4))
        plt.pcolormesh(times, frequencies, spectrogram_db, shading='gouraud', cmap='cividis')
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')
        plt.title('Audio Spectrogram')
        plt.colorbar(label='Intensity (dB)')
        plt.tight_layout()

        # Save to bytes buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        plt.close()
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')        # Encode to base64

        return image_base64

    except Exception as e:
        print(f"Error generating spectrogram: {e}")
        return None


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

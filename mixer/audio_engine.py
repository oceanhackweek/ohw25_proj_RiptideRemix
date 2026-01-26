import numpy as np
import librosa
from scipy.io import wavfile
from scipy import signal

GEN_SR = 44100
MAX_SAMPLES = GEN_SR * 60


def process_clip(clip, start_time, loops, loudness, pitch, speed):
    sr, d = wavfile.read(clip)

    if d.ndim > 1:
        d = d.mean(axis=1)

    d = d.astype(np.float32)
    if np.max(np.abs(d)) > 0:
        d /= np.max(np.abs(d))

    if sr != GEN_SR:
        d = signal.resample(d, int(len(d) * GEN_SR / sr))
        sr = GEN_SR

    d = np.tile(d, loops)
    d *= loudness

    if pitch != 0:
        d = librosa.effects.pitch_shift(d, sr, pitch)

    if speed != 1:
        d = librosa.effects.time_stretch(d, speed)

    start_pad = np.zeros(int(start_time * sr))
    d = np.concatenate([start_pad, d])

    if len(d) > MAX_SAMPLES:
        d = d[:MAX_SAMPLES]
    else:
        d = np.pad(d, (0, MAX_SAMPLES - len(d)))

    return d


def combine_clips(base_clip, clip_params):
    mix = np.zeros(MAX_SAMPLES, dtype=np.float32)

    for p in clip_params:
        mix += process_clip(**p)

    mix /= np.max(np.abs(mix)) + 1e-6
    return mix

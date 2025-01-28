import numpy as np
from scipy.signal import find_peaks

# For simulation purpose
def generate_ecg_data(duration=10, sampling_rate=100, bpm=70):
    heart_rate_hz = bpm / 60.0 # per second
    t = np.linspace(0, duration, int(duration * sampling_rate))
    ecg_signal = 0.6 * np.sin(2 * np.pi * heart_rate_hz * t)
    for peak_time in np.arange(0, duration, 1 / heart_rate_hz):
        peak_idx = int(peak_time * sampling_rate)
        if peak_idx < len(ecg_signal):
            ecg_signal[peak_idx] += 1.0
    noise = np.random.normal(0, 0.05, ecg_signal.shape)
    ecg_signal += noise
    return t, ecg_signal

def calculate_bpm_from_simulated_ecg(ecg_signal, sampling_rate=100):
    peaks, _ = find_peaks(ecg_signal, height=0.8, distance=sampling_rate // 2)
    rr_intervals = np.diff(peaks) / sampling_rate
    bpm = 60 / np.mean(rr_intervals) if len(rr_intervals) > 0 else 0
    return bpm


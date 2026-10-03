"""Signal processing utilities for respiratory waveform data."""

from .features import estimate_breathing_rate, peak_to_peak_amplitude
from .preprocessing import detrend_signal, normalize_signal, smooth_signal

__all__ = [
    "estimate_breathing_rate",
    "peak_to_peak_amplitude",
    "detrend_signal",
    "normalize_signal",
    "smooth_signal",
]

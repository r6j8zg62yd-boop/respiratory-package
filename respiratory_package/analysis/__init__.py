"""Respiratory feature extraction routines."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def estimate_breathing_rate(signal: Sequence[float], sample_rate_hz: float) -> float:
    """Estimate breathing rate in breaths per minute using FFT peak detection."""
    arr = np.asarray(signal, dtype=float)
    if arr.ndim != 1:
        raise ValueError("Signal must be a 1D sequence.")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive.")
    if arr.size < 2:
        return 0.0

    centered = arr - np.mean(arr)
    spectrum = np.abs(np.fft.rfft(centered))
    freqs = np.fft.rfftfreq(arr.size, d=1.0 / sample_rate_hz)

    valid = (freqs >= 0.1) & (freqs <= 1.0)
    if not np.any(valid):
        return 0.0

    dominant_frequency = freqs[valid][np.argmax(spectrum[valid])]
    return float(dominant_frequency * 60.0)


def peak_to_peak_amplitude(signal: Sequence[float]) -> float:
    """Return the range of a signal as a proxy for tidal amplitude."""
    arr = np.asarray(signal, dtype=float)
    if arr.ndim != 1:
        raise ValueError("Signal must be a 1D sequence.")
    if arr.size == 0:
        return 0.0
    return float(np.max(arr) - np.min(arr))

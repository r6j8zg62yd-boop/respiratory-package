"""Respiratory metric calculations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from respiratory_package.signal.features import estimate_breathing_rate, peak_to_peak_amplitude
from respiratory_package.signal.preprocessing import normalize_signal, smooth_signal


@dataclass
class RespiratoryMetrics:
    """Container for derived respiratory descriptors."""

    breathing_rate_bpm: float
    tidal_volume_index: float
    minute_ventilation_index: float
    signal_variance: float
    signal_mean: float

    def as_dict(self) -> dict[str, float]:
        return {
            "breathing_rate_bpm": self.breathing_rate_bpm,
            "tidal_volume_index": self.tidal_volume_index,
            "minute_ventilation_index": self.minute_ventilation_index,
            "signal_variance": self.signal_variance,
            "signal_mean": self.signal_mean,
        }


def summarize_signal(signal: Sequence[float], sample_rate_hz: float) -> RespiratoryMetrics:
    """Compute a compact summary for a respiratory waveform."""
    arr = np.asarray(signal, dtype=float)
    if arr.ndim != 1:
        raise ValueError("Signal must be a 1D sequence.")
    if arr.size == 0:
        raise ValueError("Signal cannot be empty.")

    normalized = normalize_signal(arr)
    smoothed = smooth_signal(normalized, window_size=min(5, max(1, arr.size // 50)))

    breathing_rate = estimate_breathing_rate(smoothed, sample_rate_hz)
    tidal_volume_index = peak_to_peak_amplitude(smoothed)
    variance = float(np.var(smoothed))
    mean_signal = float(np.mean(smoothed))
    minute_ventilation_index = breathing_rate * tidal_volume_index

    return RespiratoryMetrics(
        breathing_rate_bpm=breathing_rate,
        tidal_volume_index=tidal_volume_index,
        minute_ventilation_index=minute_ventilation_index,
        signal_variance=variance,
        signal_mean=mean_signal,
    )

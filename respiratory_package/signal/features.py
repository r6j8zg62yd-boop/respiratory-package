"""Preprocessing routines for respiratory signal data."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def normalize_signal(signal: Sequence[float]) -> np.ndarray:
    """Rescale a 1D signal to the range [0, 1]."""
    arr = np.asarray(signal, dtype=float)
    if arr.ndim != 1:
        raise ValueError("Signal must be a 1D sequence.")
    if arr.size == 0:
        return arr.copy()
    min_value = float(np.min(arr))
    max_value = float(np.max(arr))
    if np.isclose(max_value, min_value):
        return np.zeros_like(arr, dtype=float)
    return (arr - min_value) / (max_value - min_value)


def smooth_signal(signal: Sequence[float], window_size: int = 5) -> np.ndarray:
    """Apply a moving average smoothing filter."""
    arr = np.asarray(signal, dtype=float)
    if arr.ndim != 1:
        raise ValueError("Signal must be a 1D sequence.")
    if window_size < 1:
        raise ValueError("window_size must be >= 1")
    if window_size == 1:
        return arr.copy()

    kernel = np.ones(window_size, dtype=float) / float(window_size)
    pad_width = window_size // 2
    padded = np.pad(arr, (pad_width, window_size - pad_width - 1), mode="edge")
    return np.convolve(padded, kernel, mode="valid")


def detrend_signal(signal: Sequence[float], window_size: int = 9) -> np.ndarray:
    """Subtract the local moving-average baseline from the signal."""
    arr = np.asarray(signal, dtype=float)
    baseline = smooth_signal(arr, window_size=window_size)
    if baseline.shape[0] != arr.shape[0]:
        baseline = np.pad(baseline, (window_size // 2, window_size - window_size // 2 - 1), mode="edge")
    return arr - baseline[: arr.shape[0]]

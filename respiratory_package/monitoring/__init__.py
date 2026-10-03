"""Pattern classification helpers for respiratory data."""

from __future__ import annotations

from typing import Sequence

from respiratory_package.analysis.metrics import summarize_signal


def classify_breathing_pattern(signal: Sequence[float], sample_rate_hz: float) -> str:
    """Return a simple label for observed respiratory behavior."""
    metrics = summarize_signal(signal, sample_rate_hz)

    if metrics.breathing_rate_bpm < 12:
        return "bradypnea"
    if metrics.breathing_rate_bpm > 20:
        return "tachypnea"
    return "normal"

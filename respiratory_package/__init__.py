"""Top-level package for respiratory data processing and monitoring."""

from .analysis.metrics import RespiratoryMetrics, summarize_signal
from .analysis.patterns import classify_breathing_pattern
from .monitoring.monitor import RespiratoryMonitor
from .signal.features import estimate_breathing_rate
from .signal.preprocessing import normalize_signal, smooth_signal

__all__ = [
    "RespiratoryMetrics",
    "summarize_signal",
    "classify_breathing_pattern",
    "RespiratoryMonitor",
    "estimate_breathing_rate",
    "normalize_signal",
    "smooth_signal",
]

import numpy as np

from respiratory_package.analysis.metrics import summarize_signal
from respiratory_package.analysis.patterns import classify_breathing_pattern
from respiratory_package.monitoring.monitor import RespiratoryMonitor
from respiratory_package.signal.features import estimate_breathing_rate
from respiratory_package.signal.preprocessing import normalize_signal, smooth_signal


def test_normalize_signal_returns_unit_range():
    values = np.array([0.0, 2.0, 4.0])
    normalized = normalize_signal(values)
    assert normalized.min() >= 0.0
    assert normalized.max() <= 1.0


def test_breathing_rate_estimation_is_positive():
    sample_rate = 25
    signal = np.sin(np.linspace(0, 10, sample_rate * 10))
    rate = estimate_breathing_rate(signal, sample_rate)
    assert rate > 0.0


def test_summarize_signal_works():
    sample_rate = 25
    signal = np.sin(np.linspace(0, 20, sample_rate * 20))
    metrics = summarize_signal(signal, sample_rate)
    assert metrics.breathing_rate_bpm >= 0.0
    assert metrics.tidal_volume_index >= 0.0


def test_classify_breathing_pattern_returns_string():
    sample_rate = 25
    signal = np.sin(np.linspace(0, 10, sample_rate * 10))
    label = classify_breathing_pattern(signal, sample_rate)
    assert label in {"normal", "tachypnea", "bradypnea"}


def test_monitor_evaluates_status():
    sample_rate = 25
    signal = np.sin(np.linspace(0, 10, sample_rate * 10))
    monitor = RespiratoryMonitor()
    result = monitor.evaluate(signal, sample_rate)
    assert "status" in result
    assert "alerts" in result
    assert "metrics" in result


def test_smooth_signal_has_same_length():
    signal = np.linspace(0.0, 1.0, 20)
    smoothed = smooth_signal(signal, window_size=5)
    assert smoothed.shape == signal.shape


if __name__ == "__main__":
    test_normalize_signal_returns_unit_range()
    test_breathing_rate_estimation_is_positive()
    test_summarize_signal_works()
    test_classify_breathing_pattern_returns_string()
    test_monitor_evaluates_status()
    test_smooth_signal_has_same_length()

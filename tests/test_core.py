"""Monitoring logic for respiratory signals."""

from __future__ import annotations

from typing import Sequence

from respiratory_package.analysis.metrics import summarize_signal
from respiratory_package.monitoring.alerts import Alert


class RespiratoryMonitor:
    """Evaluate respiratory signal health and emit alerts when thresholds are crossed."""

    def __init__(
        self,
        *,
        low_bpm: float = 12.0,
        high_bpm: float = 24.0,
        low_tidal_index: float = 0.05,
        high_tidal_index: float = 1.5,
    ) -> None:
        self.low_bpm = low_bpm
        self.high_bpm = high_bpm
        self.low_tidal_index = low_tidal_index
        self.high_tidal_index = high_tidal_index

    def evaluate(self, signal: Sequence[float], sample_rate_hz: float) -> dict[str, object]:
        metrics = summarize_signal(signal, sample_rate_hz)
        alerts: list[Alert] = []

        if metrics.breathing_rate_bpm < self.low_bpm:
            alerts.append(
                Alert(
                    level="warning",
                    message="Breathing rate is below the expected range.",
                    metric_name="breathing_rate_bpm",
                    observed_value=metrics.breathing_rate_bpm,
                    threshold=self.low_bpm,
                )
            )

        if metrics.breathing_rate_bpm > self.high_bpm:
            alerts.append(
                Alert(
                    level="warning",
                    message="Breathing rate is above the expected range.",
                    metric_name="breathing_rate_bpm",
                    observed_value=metrics.breathing_rate_bpm,
                    threshold=self.high_bpm,
                )
            )

        if metrics.tidal_volume_index < self.low_tidal_index:
            alerts.append(
                Alert(
                    level="info",
                    message="Tidal amplitude is low relative to the configured threshold.",
                    metric_name="tidal_volume_index",
                    observed_value=metrics.tidal_volume_index,
                    threshold=self.low_tidal_index,
                )
            )

        if metrics.tidal_volume_index > self.high_tidal_index:
            alerts.append(
                Alert(
                    level="warning",
                    message="Tidal amplitude is high relative to the configured threshold.",
                    metric_name="tidal_volume_index",
                    observed_value=metrics.tidal_volume_index,
                    threshold=self.high_tidal_index,
                )
            )

        return {
            "metrics": metrics.as_dict(),
            "alerts": [alert.__dict__ for alert in alerts],
            "status": "ok" if not alerts else "alert",
        }

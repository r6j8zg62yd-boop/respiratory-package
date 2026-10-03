"""Alert definitions for monitoring workflows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Alert:
    """A simple alert emitted during respiratory monitoring."""

    level: str
    message: str
    metric_name: str
    observed_value: float
    threshold: float

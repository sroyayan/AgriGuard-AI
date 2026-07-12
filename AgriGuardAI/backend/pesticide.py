"""Pesticide recommendation rules (phase-4)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Severity = Literal["Low", "Medium", "High", "Critical"]


@dataclass(frozen=True)
class PesticideRecommendation:
    """Structured pesticide recommendation."""

    should_apply: bool
    message: str


def recommend_pesticide(severity: Severity) -> PesticideRecommendation:
    """Return pesticide recommendation from infestation severity."""
    if severity == "Critical":
        return PesticideRecommendation(
            should_apply=True,
            message="Immediate pesticide application is recommended.",
        )
    if severity == "High":
        return PesticideRecommendation(
            should_apply=True,
            message="Pesticide application is recommended soon.",
        )
    if severity == "Medium":
        return PesticideRecommendation(
            should_apply=False,
            message="Monitor closely and use targeted control if population rises.",
        )
    return PesticideRecommendation(
        should_apply=False,
        message="No pesticide needed now; continue routine monitoring.",
    )

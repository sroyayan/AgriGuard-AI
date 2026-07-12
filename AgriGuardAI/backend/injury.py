"""Rule engine for crop infestation severity (phase-3)."""

from __future__ import annotations

from typing import Literal

Severity = Literal["Low", "Medium", "High", "Critical"]
SUPPORTED_CROPS = {"rice"}


def calculate_infestation_severity(crop: str, harmful_count: int, total_count: int) -> Severity:
    """Compute infestation severity using harmful insect pressure for rice."""
    normalized_crop = crop.strip().lower()
    if normalized_crop not in SUPPORTED_CROPS:
        raise ValueError(f"Unsupported crop '{crop}'. Supported crops: Rice")

    if harmful_count <= 0 or total_count <= 0:
        return "Low"

    harmful_ratio = harmful_count / max(total_count, 1)

    if harmful_count >= 30 or (harmful_count >= 20 and harmful_ratio >= 0.8):
        return "Critical"
    if harmful_count >= 15 or (harmful_count >= 10 and harmful_ratio >= 0.6):
        return "High"
    if harmful_count >= 6 or (harmful_count >= 3 and harmful_ratio >= 0.4):
        return "Medium"
    return "Low"

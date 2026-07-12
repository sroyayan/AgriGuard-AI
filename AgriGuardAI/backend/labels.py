"""Static insect impact lookup for phase-2 classification."""

from __future__ import annotations

from typing import Dict, Literal

ImpactType = Literal["Harmful", "Beneficial", "Unknown"]

INSECT_IMPACT_LOOKUP: Dict[str, ImpactType] = {
    "brown_planthopper": "Harmful",
    "stem_borer": "Harmful",
    "leaf_folder": "Harmful",
    "rice_hispa": "Harmful",
    "armyworm": "Harmful",
    "ladybird": "Beneficial",
    "dragonfly": "Beneficial",
    "lacewing": "Beneficial",
    "spider": "Beneficial",
    "parasitoid_wasp": "Beneficial",
}


def classify_insect(label: str) -> ImpactType:
    """Classify a detected insect label as harmful or beneficial."""
    normalized = label.strip().lower().replace(" ", "_")
    return INSECT_IMPACT_LOOKUP.get(normalized, "Unknown")

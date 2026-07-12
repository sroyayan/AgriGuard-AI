"""Simple economic estimation for spraying decision (phase-5)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Severity = Literal["Low", "Medium", "High", "Critical"]

SEVERITY_LOSS_REDUCTION = {
    "Low": 0.10,
    "Medium": 0.30,
    "High": 0.50,
    "Critical": 0.70,
}


@dataclass(frozen=True)
class CostBenefitResult:
    """Result of spray cost-benefit evaluation."""

    estimated_benefit: float
    net_benefit: float
    economically_worthwhile: bool


def estimate_spray_economics(
    *,
    severity: Severity,
    should_apply_pesticide: bool,
    affected_area_acres: float = 1.0,
    expected_yield_kg_per_acre: float = 3200.0,
    crop_price_per_kg: float = 0.35,
    expected_loss_percent_without_control: float = 20.0,
    spray_cost_total: float = 120.0,
) -> CostBenefitResult:
    """Estimate whether spraying is economically worthwhile."""
    if not should_apply_pesticide:
        return CostBenefitResult(0.0, -spray_cost_total, False)

    reduction_factor = SEVERITY_LOSS_REDUCTION[severity]
    potential_loss_value = (
        affected_area_acres
        * expected_yield_kg_per_acre
        * crop_price_per_kg
        * (expected_loss_percent_without_control / 100)
    )
    estimated_benefit = potential_loss_value * reduction_factor
    net_benefit = estimated_benefit - spray_cost_total

    return CostBenefitResult(
        estimated_benefit=round(estimated_benefit, 2),
        net_benefit=round(net_benefit, 2),
        economically_worthwhile=net_benefit > 0,
    )

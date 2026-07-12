from AgriGuardAI.backend.cost_benefit import estimate_spray_economics
from AgriGuardAI.backend.injury import calculate_infestation_severity
from AgriGuardAI.backend.labels import classify_insect
from AgriGuardAI.backend.pesticide import recommend_pesticide


def test_label_classification_known_and_unknown() -> None:
    assert classify_insect("Brown Planthopper") == "Harmful"
    assert classify_insect("Ladybird") == "Beneficial"
    assert classify_insect("Unknown Beetle") == "Unknown"


def test_injury_severity_thresholds_for_rice() -> None:
    assert calculate_infestation_severity("Rice", harmful_count=1, total_count=10) == "Low"
    assert calculate_infestation_severity("Rice", harmful_count=6, total_count=10) == "Medium"
    assert calculate_infestation_severity("Rice", harmful_count=15, total_count=20) == "High"
    assert calculate_infestation_severity("Rice", harmful_count=30, total_count=30) == "Critical"


def test_pesticide_recommendation_from_severity() -> None:
    assert recommend_pesticide("High").should_apply is True
    assert recommend_pesticide("Low").should_apply is False


def test_cost_benefit_uses_recommendation_gate() -> None:
    no_spray = estimate_spray_economics(severity="Medium", should_apply_pesticide=False, spray_cost_total=50)
    assert no_spray.economically_worthwhile is False

    spray = estimate_spray_economics(
        severity="Critical",
        should_apply_pesticide=True,
        affected_area_acres=5,
        expected_yield_kg_per_acre=4000,
        crop_price_per_kg=0.4,
        expected_loss_percent_without_control=25,
        spray_cost_total=200,
    )
    assert spray.estimated_benefit > 0

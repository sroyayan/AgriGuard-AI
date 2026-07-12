"""FastAPI application for AgriGuard AI."""

from __future__ import annotations

import base64
import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from .config import settings
from .cost_benefit import CostBenefitResult, estimate_spray_economics
from .detection import Detection, InsectDetector, get_default_detector
from .injury import calculate_infestation_severity
from .labels import classify_insect
from .pesticide import PesticideRecommendation, recommend_pesticide

logging.basicConfig(level=settings.log_level)
LOGGER = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, version="1.0.0")


def _init_database() -> None:
    db_path = settings.sqlite_absolute_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analyzed_at TEXT NOT NULL,
                crop TEXT NOT NULL,
                total_insects INTEGER NOT NULL,
                harmful_insects INTEGER NOT NULL,
                severity TEXT NOT NULL,
                pesticide_needed INTEGER NOT NULL,
                net_benefit REAL NOT NULL
            )
            """
        )
        connection.commit()


@contextmanager
def get_db_connection():
    connection = sqlite3.connect(settings.sqlite_absolute_path)
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


@app.on_event("startup")
def startup_event() -> None:
    _init_database()
    app.state.detector = get_default_detector()
    LOGGER.info("AgriGuard AI API started")


class DetectionOutput(BaseModel):
    label: str
    confidence: float
    impact: str


class PesticideOutput(BaseModel):
    should_apply: bool
    message: str


class CostBenefitOutput(BaseModel):
    estimated_benefit: float
    net_benefit: float
    economically_worthwhile: bool


class AnalysisResponse(BaseModel):
    crop: str
    insect_count: int
    detections: List[DetectionOutput]
    counts_by_label: Dict[str, int]
    counts_by_impact: Dict[str, int]
    infestation_severity: str
    pesticide: PesticideOutput
    cost_benefit: CostBenefitOutput
    annotated_image_base64: str


def _enforce_upload_size(file_size_bytes: int) -> None:
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if file_size_bytes > max_bytes:
        raise HTTPException(status_code=413, detail=f"Image exceeds {settings.max_upload_size_mb}MB upload limit")


def _build_detection_output(detection: Detection) -> DetectionOutput:
    impact = classify_insect(detection.label)
    return DetectionOutput(label=detection.label, confidence=detection.confidence, impact=impact)


def _serialize_pesticide(recommendation: PesticideRecommendation) -> PesticideOutput:
    return PesticideOutput(should_apply=recommendation.should_apply, message=recommendation.message)


def _serialize_cost_benefit(result: CostBenefitResult) -> CostBenefitOutput:
    return CostBenefitOutput(
        estimated_benefit=result.estimated_benefit,
        net_benefit=result.net_benefit,
        economically_worthwhile=result.economically_worthwhile,
    )


def _record_analysis(
    *,
    crop: str,
    insect_count: int,
    harmful_count: int,
    severity: str,
    pesticide_needed: bool,
    net_benefit: float,
) -> None:
    _init_database()
    with get_db_connection() as connection:
        connection.execute(
            """
            INSERT INTO analysis_history (
                analyzed_at, crop, total_insects, harmful_insects, severity, pesticide_needed, net_benefit
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                crop,
                insect_count,
                harmful_count,
                severity,
                int(pesticide_needed),
                net_benefit,
            ),
        )


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(
    image: UploadFile = File(...),
    crop: str = Form("Rice"),
    affected_area_acres: float = Form(1.0, ge=0.1, le=500.0),
    expected_yield_kg_per_acre: float = Form(3200.0, ge=100.0, le=10000.0),
    crop_price_per_kg: float = Form(0.35, ge=0.01, le=10.0),
    expected_loss_percent_without_control: float = Form(20.0, ge=0.0, le=100.0),
    spray_cost_total: float = Form(120.0, ge=0.0, le=100000.0),
) -> AnalysisResponse:
    """Analyze crop image for detection and recommendation outputs."""
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    image_bytes = await image.read()
    _enforce_upload_size(len(image_bytes))

    detector: Optional[InsectDetector] = getattr(app.state, "detector", None)
    if detector is None:
        raise HTTPException(status_code=500, detail="Detector is not initialized")

    try:
        detection_result = detector.detect(image_bytes)
        detections = [_build_detection_output(item) for item in detection_result.detections]
        harmful_count = sum(1 for item in detections if item.impact == "Harmful")
        beneficial_count = sum(1 for item in detections if item.impact == "Beneficial")

        severity = calculate_infestation_severity(
            crop=crop,
            harmful_count=harmful_count,
            total_count=detection_result.total_count,
        )
        pesticide_recommendation = recommend_pesticide(severity)
        economics = estimate_spray_economics(
            severity=severity,
            should_apply_pesticide=pesticide_recommendation.should_apply,
            affected_area_acres=affected_area_acres,
            expected_yield_kg_per_acre=expected_yield_kg_per_acre,
            crop_price_per_kg=crop_price_per_kg,
            expected_loss_percent_without_control=expected_loss_percent_without_control,
            spray_cost_total=spray_cost_total,
        )

        _record_analysis(
            crop=crop,
            insect_count=detection_result.total_count,
            harmful_count=harmful_count,
            severity=severity,
            pesticide_needed=pesticide_recommendation.should_apply,
            net_benefit=economics.net_benefit,
        )

        return AnalysisResponse(
            crop=crop,
            insect_count=detection_result.total_count,
            detections=detections,
            counts_by_label=detection_result.counts,
            counts_by_impact={
                "Harmful": harmful_count,
                "Beneficial": beneficial_count,
                "Unknown": detection_result.total_count - harmful_count - beneficial_count,
            },
            infestation_severity=severity,
            pesticide=_serialize_pesticide(pesticide_recommendation),
            cost_benefit=_serialize_cost_benefit(economics),
            annotated_image_base64=base64.b64encode(detection_result.annotated_image_bytes).decode("utf-8"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - safety guard
        LOGGER.exception("Analysis failed")
        raise HTTPException(status_code=500, detail="Failed to analyze image") from exc

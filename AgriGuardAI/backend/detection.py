"""YOLOv11-based insect detection (phase-1)."""

from __future__ import annotations

import io
import logging
from dataclasses import dataclass
from typing import Dict, List

import numpy as np
from PIL import Image, UnidentifiedImageError

from .config import settings

LOGGER = logging.getLogger(__name__)

try:
    from ultralytics import YOLO
except Exception:  # pragma: no cover - optional import fallback for environments without ultralytics
    YOLO = None


@dataclass(frozen=True)
class Detection:
    """Single object detection record."""

    label: str
    confidence: float


@dataclass(frozen=True)
class DetectionResult:
    """Phase-1 detection output."""

    detections: List[Detection]
    counts: Dict[str, int]
    annotated_image_bytes: bytes

    @property
    def total_count(self) -> int:
        return len(self.detections)


class InsectDetector:
    """Ultralytics YOLO detector wrapper."""

    def __init__(self, model_path: str, confidence: float) -> None:
        self._model_path = model_path
        self._confidence = confidence
        self._model = None

    def _load_model(self):
        if self._model is not None:
            return self._model
        if YOLO is None:
            raise RuntimeError("Ultralytics is not installed. Install dependencies from requirements.txt")
        self._model = YOLO(self._model_path)
        LOGGER.info("Loaded YOLO model from %s", self._model_path)
        return self._model

    def detect(self, image_bytes: bytes) -> DetectionResult:
        """Run model inference and return detections plus an annotated image."""
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except UnidentifiedImageError as exc:
            raise ValueError("Uploaded file is not a valid image") from exc

        image_array = np.array(image)
        model = self._load_model()
        results = model.predict(source=image_array, conf=self._confidence, verbose=False)

        if not results:
            return DetectionResult(detections=[], counts={}, annotated_image_bytes=image_bytes)

        result = results[0]
        names = result.names
        detections: List[Detection] = []
        counts: Dict[str, int] = {}

        for box in result.boxes:
            class_id = int(box.cls.item())
            label = str(names.get(class_id, f"class_{class_id}")).strip().lower().replace(" ", "_")
            confidence = float(box.conf.item())
            detections.append(Detection(label=label, confidence=round(confidence, 4)))
            counts[label] = counts.get(label, 0) + 1

        plotted = result.plot()
        annotated_image = Image.fromarray(plotted[..., ::-1])
        output = io.BytesIO()
        annotated_image.save(output, format="JPEG", quality=90)

        return DetectionResult(detections=detections, counts=counts, annotated_image_bytes=output.getvalue())


def get_default_detector() -> InsectDetector:
    """Build detector from app settings."""
    return InsectDetector(model_path=settings.model_path, confidence=settings.model_confidence)

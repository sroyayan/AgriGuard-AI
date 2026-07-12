import io

from fastapi.testclient import TestClient
from PIL import Image

from AgriGuardAI.backend.api import app
from AgriGuardAI.backend.detection import Detection, DetectionResult


class StubDetector:
    def detect(self, image_bytes: bytes) -> DetectionResult:  # noqa: ARG002
        image = Image.new("RGB", (32, 32), color=(0, 255, 0))
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        return DetectionResult(
            detections=[
                Detection(label="brown_planthopper", confidence=0.92),
                Detection(label="ladybird", confidence=0.88),
            ],
            counts={"brown_planthopper": 1, "ladybird": 1},
            annotated_image_bytes=buffer.getvalue(),
        )


def test_analyze_endpoint_returns_expected_payload() -> None:
    app.state.detector = StubDetector()
    client = TestClient(app)

    image = Image.new("RGB", (20, 20), color=(255, 255, 255))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    response = client.post(
        "/analyze",
        files={"image": ("test.jpg", buffer, "image/jpeg")},
        data={"crop": "Rice"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["insect_count"] == 2
    assert payload["counts_by_impact"]["Harmful"] == 1
    assert payload["pesticide"]["should_apply"] is False
    assert payload["annotated_image_base64"]

# AgriGuard AI

Production-ready AI-powered agricultural pest detection and decision support system.

## Project Structure

```text
AgriGuardAI/
├── datasets/
├── models/
├── backend/
│   ├── api.py
│   ├── config.py
│   ├── cost_benefit.py
│   ├── detection.py
│   ├── injury.py
│   ├── labels.py
│   └── pesticide.py
├── docs/
└── tests/
frontend/
requirements.txt
```

## Core Phases Implemented

1. **YOLOv11 detection** with Ultralytics wrapper (`backend/detection.py`) and insect counting.
2. **Harmful vs Beneficial** classification via static lookup table (`backend/labels.py`).
3. **Rice-only infestation severity** rule engine (`backend/injury.py`).
4. **Pesticide recommendation** from severity (`backend/pesticide.py`).
5. **Economic spray decision** using simple cost-benefit model (`backend/cost_benefit.py`).

## Backend (FastAPI + SQLite)

### Install

```bash
pip install -r requirements.txt
```

### Run API

```bash
uvicorn AgriGuardAI.backend.api:app --reload
```

### API Endpoints

- `GET /health`
- `POST /analyze`
  - Multipart image upload (`image`)
  - Optional economic inputs (`affected_area_acres`, `expected_yield_kg_per_acre`, `crop_price_per_kg`, `expected_loss_percent_without_control`, `spray_cost_total`)

## Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Set backend URL with `VITE_API_URL` if needed (defaults to `http://localhost:8000/analyze`).

## Testing

```bash
pytest AgriGuardAI/tests -q
```

## Notes

- Place YOLO model weights at `AgriGuardAI/models/yolo11-insects.pt` (or override with `AGRIGUARD_MODEL_PATH`).
- Detection dataset source can be managed via Roboflow exports in `AgriGuardAI/datasets/`.

# AgriGuard AI Architecture

## Pipeline
1. **Detection** (`backend/detection.py`): runs YOLOv11 object detection and returns insect counts with an annotated image.
2. **Impact Labeling** (`backend/labels.py`): maps each insect label to Harmful/Beneficial via static lookup.
3. **Infestation Rule Engine** (`backend/injury.py`): derives Rice infestation severity (`Low`, `Medium`, `High`, `Critical`).
4. **Pesticide Recommendation** (`backend/pesticide.py`): decides whether spraying is required.
5. **Cost-Benefit** (`backend/cost_benefit.py`): estimates whether spraying is economically worthwhile.

## API
- `GET /health`
- `POST /analyze` (multipart image upload + optional economic inputs)

## Data Persistence
- SQLite database (`backend/agriguard.db`) stores analysis summary history.

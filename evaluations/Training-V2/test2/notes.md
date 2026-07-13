# AgriGuard AI - Evaluation Test 2

## Test Information

- **Date:** 13 July 2026
- **Model:** Training V2 (YOLO11n)
- **Dataset:** IP102 YOLOv5
- **Evaluation Type:** Multiple real-world garden images
- **Location:** Home Garden

---

# Image 1

## Original Image
**Filename:** IMG20260712121653.jpg

### Description
Fly resting on a vine.

### Model Prediction
- **Predicted Class:** Beet spot flies
- **Confidence:** 0.55

### Ground Truth
General fly (exact species not verified).

### Detection Result
- ✅ Object detected successfully.
- ✅ Bounding box correctly localized the insect.

### Remarks
Model correctly detected the insect but classified it as "Beet spot flies."
Species verification required.

---

# Image 2

## Original Image
**Filename:** IMG20260712121710.jpg

### Description
Dark winged insect resting on a leaf.

### Model Prediction
- **Predicted Class:** Cicadellidae
- **Confidence:** 0.55

### Ground Truth
Unknown.
Requires expert identification.

### Detection Result
- ✅ Object detected successfully.
- ✅ Bounding box correctly localized the insect.

### Remarks
Prediction appears plausible but cannot yet be verified.

---

# Image 3

## Original Image
**Filename:** IMG20260712121715.jpg

### Description
Ant hanging beneath a leaf.

### Model Prediction
- **Predicted Class:** Locustoidea
- **Confidence:** 0.34

### Ground Truth
Ant

### Detection Result
- ✅ Object detected successfully.
- ❌ Incorrect classification.

### Remarks
The model successfully localized the insect but misclassified it.
This is expected because ants are not among the trained IP102 object classes.
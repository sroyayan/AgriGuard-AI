"""
AgriGuard AI
Core Detection Module
"""

import os
import shutil
from ultralytics import YOLO

# Load the model only once
model = YOLO("models/best.pt")


def detect_insect(image_path):
    """
    Detect insects in an image.

    Args:
        image_path (str): Path to the image.

    Returns:
        dict: Detection results.
    """

    results = model.predict(
        source=image_path,
        conf=0.5,
        save=True,
        exist_ok=True
    )

    result = results[0]

    # No detections
    if len(result.boxes) == 0:
        return {
            "detected": False,
            "detections": [],
            "output_image": None
        }

    # Copy annotated image into project outputs folder
    os.makedirs("outputs", exist_ok=True)

    source_output = os.path.join(
        result.save_dir,
        os.path.basename(image_path)
    )

    destination_output = os.path.join(
        "outputs",
        os.path.basename(image_path)
    )

    shutil.copy(source_output, destination_output)

    detections = []

    for box in result.boxes:

        class_id = int(box.cls[0])

        detections.append({
            "class": result.names[class_id],
            "confidence": round(float(box.conf[0]), 2),
            "bbox": [
                round(float(x), 2)
                for x in box.xyxy[0]
            ]
        })

    return {
        "detected": True,
        "detections": detections,
        "output_image": destination_output
    }


# Standalone testing
if __name__ == "__main__":

    image = "test_images/test (6).jpg"

    result = detect_insect(image)

    if result["detected"]:

        print("\nDetected Insects\n")

        for insect in result["detections"]:
            print(f"Class      : {insect['class']}")
            print(f"Confidence : {insect['confidence']}")
            print(f"Bounding Box : {insect['bbox']}")
            print()

        print("Annotated Image:")
        print(result["output_image"])

    else:
        print("No insect detected.")
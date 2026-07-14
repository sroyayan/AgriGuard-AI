"""
AgriGuard AI
Detector Testing Script
"""

from core.detector import detect_insect


def main():

    image_path = "test_images/test (6).jpg"

    result = detect_insect(image_path)

    print("\n========== AgriGuard AI ==========\n")

    if result["detected"]:

        print(f"Total Detections : {len(result['detections'])}\n")

        for index, insect in enumerate(result["detections"], start=1):

            print(f"Insect {index}")
            print(f"Class       : {insect['class']}")
            print(f"Confidence  : {insect['confidence']}")
            print(f"BoundingBox : {insect['bbox']}")
            print()

        print("Annotated Image:")
        print(result["output_image"])

    else:
        print("No insect detected.")

    print("\n==================================\n")


if __name__ == "__main__":
    main()
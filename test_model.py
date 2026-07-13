from ultralytics import YOLO

# Load your trained model
model = YOLO("models/best.pt")

# Test on one image
results = model.predict(
    source="test_images",
    conf=0.25,
    save=True
)

print("Prediction completed!")
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from core.detector import detect_insect

# ==========================================
# App Settings
# ==========================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

selected_image = None


# ==========================================
# Functions
# ==========================================
def upload_image():
    global selected_image

    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp")
        ]
    )

    if not file_path:
        return

    selected_image = file_path

    image = Image.open(file_path)
    image.thumbnail((350, 350))

    preview = ctk.CTkImage(
        light_image=image,
        dark_image=image,
        size=image.size
    )

    image_placeholder.configure(
        image=preview,
        text=""
    )

    image_placeholder.image = preview

    status_label.configure(
        text="Status : Image Loaded"
    )

    detect_button.configure(
        state="normal"
    )

def detect_image():

    global selected_image

    if selected_image is None:
        return

    status_label.configure(text="Status : Detecting...")
    app.update()

    result = detect_insect(selected_image)

    if result["detected"]:

        insect = result["detections"][0]

        prediction_label.configure(
            text=f"Prediction : {insect['class']}"
        )

        confidence_label.configure(
            text=f"Confidence : {int(insect['confidence']*100)}%"
        )

        output = Image.open(result["output_image"])
        output.thumbnail((350, 350))

        preview = ctk.CTkImage(
            light_image=output,
            dark_image=output,
            size=output.size
        )

        image_placeholder.configure(
            image=preview,
            text=""
        )

        image_placeholder.image = preview

        status_label.configure(
            text="Status : Detection Completed"
        )

    else:

        prediction_label.configure(
            text="Prediction : No Insect Detected"
        )

        confidence_label.configure(
            text="Confidence : ---"
        )

        status_label.configure(
            text="Status : No Insect Detected"
        )
# ==========================================
# Main Window
# ==========================================
app = ctk.CTk()

app.title("🌿 AgriGuard AI")
app.geometry("1000x700")
app.minsize(900, 650)


# ==========================================
# Header
# ==========================================
header = ctk.CTkFrame(
    app,
    corner_radius=0
)
header.pack(fill="x")

title = ctk.CTkLabel(
    header,
    text="🌿 AgriGuard AI",
    font=("Arial", 28, "bold")
)
title.pack(pady=(15, 0))

subtitle = ctk.CTkLabel(
    header,
    text="AI Powered Insect Detection System",
    font=("Arial", 15)
)
subtitle.pack(pady=(0, 15))


# ==========================================
# Main Content
# ==========================================
content = ctk.CTkFrame(app)
content.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# ==========================================
# Left Panel
# ==========================================
left_frame = ctk.CTkFrame(content)
left_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)

left_title = ctk.CTkLabel(
    left_frame,
    text="Image Preview",
    font=("Arial", 20, "bold")
)
left_title.pack(pady=15)

image_placeholder = ctk.CTkLabel(
    left_frame,
    text="No Image Selected",
    width=350,
    height=350,
    fg_color="#2B2B2B",
    corner_radius=12
)

image_placeholder.pack(
    expand=True,
    padx=20,
    pady=20
)


# ==========================================
# Right Panel
# ==========================================
right_frame = ctk.CTkFrame(content)

right_frame.pack(
    side="right",
    fill="both",
    expand=True
)

right_title = ctk.CTkLabel(
    right_frame,
    text="Detection Results",
    font=("Arial", 20, "bold")
)
right_title.pack(pady=15)

prediction_label = ctk.CTkLabel(
    right_frame,
    text="Prediction : ---",
    font=("Arial", 18)
)

prediction_label.pack(
    anchor="w",
    padx=20,
    pady=10
)

confidence_label = ctk.CTkLabel(
    right_frame,
    text="Confidence : ---",
    font=("Arial", 18)
)

confidence_label.pack(
    anchor="w",
    padx=20
)


# ==========================================
# Bottom Controls
# ==========================================
bottom = ctk.CTkFrame(app)

bottom.pack(
    fill="x",
    padx=20,
    pady=(0, 20)
)

upload_button = ctk.CTkButton(
    bottom,
    text="Upload Image",
    width=180,
    command=upload_image
)

upload_button.pack(
    side="left",
    padx=20,
    pady=15
)

detect_button = ctk.CTkButton(
    bottom,
    text="Detect Insect",
    width=180,
    state="disabled",
    command=detect_image
)

detect_button.pack(
    side="left",
    padx=10
)

status_label = ctk.CTkLabel(
    bottom,
    text="Status : Waiting for image..."
)

status_label.pack(
    side="right",
    padx=20
)


# ==========================================
# Run Application
# ==========================================
app.mainloop()
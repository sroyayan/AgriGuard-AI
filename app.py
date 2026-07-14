import customtkinter as ctk

# --------------------------------------------------
# App Settings
# --------------------------------------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# --------------------------------------------------
# Main Window
# --------------------------------------------------
app = ctk.CTk()

app.title("🌿 AgriGuard AI")
app.geometry("1000x700")
app.minsize(900, 650)

# --------------------------------------------------
# Header
# --------------------------------------------------
header = ctk.CTkFrame(app, corner_radius=0)
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

# --------------------------------------------------
# Main Content
# --------------------------------------------------
content = ctk.CTkFrame(app)
content.pack(fill="both", expand=True, padx=20, pady=20)

# Left Panel
left_frame = ctk.CTkFrame(content)
left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

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
image_placeholder.pack(expand=True, padx=20, pady=20)

# Right Panel
right_frame = ctk.CTkFrame(content)
right_frame.pack(side="right", fill="both", expand=True)

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
prediction_label.pack(anchor="w", padx=20, pady=10)

confidence_label = ctk.CTkLabel(
    right_frame,
    text="Confidence : ---",
    font=("Arial", 18)
)
confidence_label.pack(anchor="w", padx=20)

# --------------------------------------------------
# Bottom Controls
# --------------------------------------------------
bottom = ctk.CTkFrame(app)
bottom.pack(fill="x", padx=20, pady=(0, 20))

upload_button = ctk.CTkButton(
    bottom,
    text="Upload Image",
    width=180
)
upload_button.pack(side="left", padx=20, pady=15)

detect_button = ctk.CTkButton(
    bottom,
    text="Detect Insect",
    width=180
)
detect_button.pack(side="left", padx=10)

status_label = ctk.CTkLabel(
    bottom,
    text="Status : Ready"
)
status_label.pack(side="right", padx=20)

# --------------------------------------------------
# Run
# --------------------------------------------------
app.mainloop()
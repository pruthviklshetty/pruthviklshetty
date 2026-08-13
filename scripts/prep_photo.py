from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


# --------------------------------------------------
# Settings
# --------------------------------------------------

OUTPUT_FILE = Path("data/source-prepped.png")


# --------------------------------------------------
# Get input photo
# --------------------------------------------------

if len(sys.argv) < 2:
    print("Usage: python scripts/prep_photo.py source-photo.jpg")
    sys.exit(1)

input_file = Path(sys.argv[1])

if not input_file.exists():
    print(f"Photo not found: {input_file}")
    sys.exit(1)

print(f"Loading photo: {input_file}")


# --------------------------------------------------
# Remove background
# --------------------------------------------------

print("Removing background...")

image = Image.open(input_file).convert("RGBA")

foreground = remove(image)

print("Background removed.")


# --------------------------------------------------
# Put subject on white background
# --------------------------------------------------

white_background = Image.new(
    "RGBA",
    foreground.size,
    (255, 255, 255, 255),
)

white_background.alpha_composite(foreground)

rgb_image = white_background.convert("RGB")


# --------------------------------------------------
# Convert to OpenCV grayscale
# --------------------------------------------------

opencv_image = np.array(rgb_image)

gray = cv2.cvtColor(
    opencv_image,
    cv2.COLOR_RGB2GRAY,
)


# --------------------------------------------------
# Improve local contrast
# --------------------------------------------------

clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8),
)

enhanced = clahe.apply(gray)


# --------------------------------------------------
# Save prepared image
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

Image.fromarray(enhanced).save(
    OUTPUT_FILE
)

print(f"Prepared image saved to: {OUTPUT_FILE}")
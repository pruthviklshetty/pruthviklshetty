from pathlib import Path

import numpy as np
from PIL import Image


# --------------------------------------------------
# Settings
# --------------------------------------------------

INPUT_FILE = Path("data/source-prepped.png")
OUTPUT_FILE = Path("avi-ascii.svg")

# Width in ASCII characters
CHAR_WIDTH = 80

# Characters from bright -> dark
RAMP = " .`:-=+*cs#%@"

# Character appearance
FONT_SIZE = 10
CHAR_WIDTH_PX = 6
LINE_HEIGHT = 11

TEXT_COLOR = "#c9d1d9"


# --------------------------------------------------
# Load image
# --------------------------------------------------

print(f"Loading {INPUT_FILE}...")

image = Image.open(INPUT_FILE).convert("L")

original_width, original_height = image.size

print(
    f"Original image: "
    f"{original_width} x {original_height}"
)


# --------------------------------------------------
# Calculate ASCII dimensions
# --------------------------------------------------

aspect_ratio = original_height / original_width

char_height = int(
    CHAR_WIDTH * aspect_ratio * 0.5
)

char_height = max(char_height, 1)

print(
    f"ASCII size: "
    f"{CHAR_WIDTH} x {char_height}"
)


# --------------------------------------------------
# Resize image
# --------------------------------------------------

image = image.resize(
    (CHAR_WIDTH, char_height)
)

pixels = np.array(image)


# --------------------------------------------------
# Convert pixels to ASCII
# --------------------------------------------------

rows = []

for row in pixels:

    line = ""

    for brightness in row:

        # Bright pixel -> sparse character
        # Dark pixel -> dense character

        index = int(
            (255 - brightness)
            / 255
            * (len(RAMP) - 1)
        )

        index = max(
            0,
            min(index, len(RAMP) - 1)
        )

        line += RAMP[index]

    rows.append(line)


# --------------------------------------------------
# SVG dimensions
# --------------------------------------------------

svg_width = CHAR_WIDTH * CHAR_WIDTH_PX
svg_height = char_height * LINE_HEIGHT + 20


# --------------------------------------------------
# Start SVG
# --------------------------------------------------

svg = []

svg.append(
    f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">
'''
)


# --------------------------------------------------
# Background
# --------------------------------------------------

svg.append(
    '''
<rect
width="100%"
height="100%"
fill="#0d1117"
/>
'''
)


# --------------------------------------------------
# Animation
# --------------------------------------------------

svg.append(
    '''
<style>

.ascii-row {
    opacity: 0;
    animation:
        print-row 0.6s ease-out forwards;
}

@keyframes print-row {

    from {
        opacity: 0;
        transform: translateX(-12px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }

}

</style>
'''
)


# --------------------------------------------------
# Draw ASCII rows
# --------------------------------------------------

for row_index, line in enumerate(rows):

    y = 15 + row_index * LINE_HEIGHT

    delay = row_index * 0.035

    escaped_line = (
        line
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    svg.append(
        f'''
<text
class="ascii-row"
x="0"
y="{y}"
fill="{TEXT_COLOR}"
font-family="monospace"
font-size="{FONT_SIZE}px"
xml:space="preserve"
style="animation-delay: {delay:.3f}s;"
>{escaped_line}</text>
'''
    )


# --------------------------------------------------
# Finish SVG
# --------------------------------------------------

svg.append("</svg>")


# --------------------------------------------------
# Save
# --------------------------------------------------

OUTPUT_FILE.write_text(
    "".join(svg),
    encoding="utf-8",
)


print(
    f"ASCII SVG created: {OUTPUT_FILE}"
)
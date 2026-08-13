import json
from pathlib import Path
from datetime import datetime


# --------------------------------------------------
# Settings
# --------------------------------------------------

INPUT_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.svg")

CELL_SIZE = 14
GAP = 4

COLORS = [
    "#161b22",  # 0 contributions
    "#0e4429",  # level 1
    "#006d32",  # level 2
    "#26a641",  # level 3
    "#39d353",  # level 4
]

ANIMATION_DELAY = 0.025


# --------------------------------------------------
# Load contribution data
# --------------------------------------------------

with INPUT_FILE.open("r", encoding="utf-8") as file:
    contributions = json.load(file)

print(f"Loaded {len(contributions)} contribution records.")


# --------------------------------------------------
# Convert dates
# --------------------------------------------------

for item in contributions:
    item["date"] = datetime.strptime(
        item["date"],
        "%Y-%m-%d",
    ).date()


# Sort oldest → newest
contributions.sort(key=lambda item: item["date"])


# --------------------------------------------------
# Group dates into weeks
# --------------------------------------------------

weeks = []
current_week = []

for item in contributions:

    weekday = item["date"].weekday()

    # Monday = 0
    # Sunday = 6

    if weekday == 0 and current_week:
        weeks.append(current_week)
        current_week = []

    current_week.append(item)


if current_week:
    weeks.append(current_week)


print(f"Created {len(weeks)} weeks.")


# --------------------------------------------------
# SVG dimensions
# --------------------------------------------------

width = len(weeks) * (CELL_SIZE + GAP) + 40
height = 7 * (CELL_SIZE + GAP) + 60


# --------------------------------------------------
# Start SVG
# --------------------------------------------------

svg = []

svg.append(
    f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{width}"
    height="{height}"
    viewBox="0 0 {width} {height}">
'''
)


# --------------------------------------------------
# Animation CSS
# --------------------------------------------------

svg.append(
    '''
<style>
@keyframes reveal {
    from {
        opacity: 0;
        transform: translateY(-4px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
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
    rx="12"
/>
'''
)


# --------------------------------------------------
# Title
# --------------------------------------------------

svg.append(
    '''
<text
    x="20"
    y="25"
    fill="#c9d1d9"
    font-family="monospace"
    font-size="14">
    GitHub Contributions
</text>
'''
)


# --------------------------------------------------
# Draw contribution cells
# --------------------------------------------------

for week_index, week in enumerate(weeks):

    for item in week:

        weekday = item["date"].weekday()

        level = item["level"]

        # Keep level within palette
        level = max(
            0,
            min(level, len(COLORS) - 1),
        )

        x = 20 + week_index * (CELL_SIZE + GAP)

        y = 40 + weekday * (CELL_SIZE + GAP)

        color = COLORS[level]

        delay = (
            week_index * 7 + weekday
        ) * ANIMATION_DELAY

        svg.append(
            f'''
<rect
    x="{x}"
    y="{y}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    rx="3"
    fill="{color}"
    opacity="0"
    style="animation: reveal 0.4s ease-out {delay:.3f}s forwards;">
</rect>
'''
        )


# --------------------------------------------------
# Legend
# --------------------------------------------------

legend_y = height - 15

svg.append(
    f'''
<text
    x="20"
    y="{legend_y}"
    fill="#8b949e"
    font-family="monospace"
    font-size="10">
    Less
</text>
'''
)


for index, color in enumerate(COLORS):

    x = 55 + index * 20

    svg.append(
        f'''
<rect
    x="{x}"
    y="{legend_y - 10}"
    width="12"
    height="12"
    rx="2"
    fill="{color}">
</rect>
'''
    )


svg.append(
    f'''
<text
    x="{55 + len(COLORS) * 20 + 5}"
    y="{legend_y}"
    fill="#8b949e"
    font-family="monospace"
    font-size="10">
    More
</text>
'''
)


# --------------------------------------------------
# Finish SVG
# --------------------------------------------------

svg.append("</svg>")


OUTPUT_FILE.write_text(
    "".join(svg),
    encoding="utf-8",
)


print(f"Heatmap written to {OUTPUT_FILE}")
from pathlib import Path
from html import escape


OUTPUT_FILE = Path("info-card.svg")


# --------------------------------------------------
# YOUR PROFILE INFORMATION
# --------------------------------------------------

NAME = "Pruthvik L Shetty"
USERNAME = "@pruthviklshetty"

ROLE = "ISE Student | Software Engineering Aspirant"

STACK = "C++ • Java • Python • JavaScript • FastAPI"

FOCUS = "Backend • AI/ML • Cloud • System Design"

CURRENTLY = "DSA • Backend • Projects"

LOCATION = "Shivamogga, India"


# --------------------------------------------------
# SVG SETTINGS
# --------------------------------------------------

WIDTH = 490
HEIGHT = 330

BACKGROUND = "#0d1117"
BORDER = "#30363d"

TEXT = "#c9d1d9"
MUTED = "#8b949e"

GREEN = "#39d353"
BLUE = "#58a6ff"
PURPLE = "#bc8cff"


# --------------------------------------------------
# ESCAPE TEXT SAFELY FOR SVG/XML
# --------------------------------------------------

def safe(text):
    return escape(str(text))


# --------------------------------------------------
# START SVG
# --------------------------------------------------

svg = []

svg.append(
    f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">
'''
)


# --------------------------------------------------
# ANIMATION
# --------------------------------------------------

svg.append(
    '''
<style>

.card-line {
    opacity: 0;
    animation: fade-in 0.5s ease-out forwards;
}

@keyframes fade-in {

    from {
        opacity: 0;
        transform: translateX(-10px);
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
# TERMINAL WINDOW
# --------------------------------------------------

svg.append(
    f'''
<rect
x="0"
y="0"
width="{WIDTH}"
height="{HEIGHT}"
rx="12"
fill="{BACKGROUND}"
stroke="{BORDER}"
stroke-width="1"
/>
'''
)


# --------------------------------------------------
# TERMINAL BUTTONS
# --------------------------------------------------

svg.append(
    '''
<circle cx="20" cy="20" r="6" fill="#ff5f56"/>
<circle cx="40" cy="20" r="6" fill="#ffbd2e"/>
<circle cx="60" cy="20" r="6" fill="#27c93f"/>

<text
x="85"
y="25"
fill="#8b949e"
font-family="monospace"
font-size="13">
pruthvik@github ~
</text>
'''
)


# --------------------------------------------------
# TERMINAL COMMAND
# --------------------------------------------------

svg.append(
    f'''
<text
class="card-line"
x="25"
y="65"
fill="{GREEN}"
font-family="monospace"
font-size="17"
font-weight="bold"
style="animation-delay:0.1s">
$ whoami
</text>
'''
)


# --------------------------------------------------
# NAME
# --------------------------------------------------

svg.append(
    f'''
<text
class="card-line"
x="25"
y="100"
fill="{TEXT}"
font-family="monospace"
font-size="16"
font-weight="bold"
style="animation-delay:0.2s">
{safe(NAME)}
</text>

<text
class="card-line"
x="25"
y="120"
fill="{MUTED}"
font-family="monospace"
font-size="12"
style="animation-delay:0.3s">
{safe(USERNAME)}
</text>
'''
)


# --------------------------------------------------
# PROFILE ROWS
# --------------------------------------------------

rows = [
    ("role", ROLE, BLUE),
    ("stack", STACK, TEXT),
    ("focus", FOCUS, PURPLE),
    ("currently", CURRENTLY, GREEN),
    ("location", LOCATION, TEXT),
]


start_y = 155
spacing = 30


for index, (key, value, color) in enumerate(rows):

    y = start_y + index * spacing
    delay = 0.4 + index * 0.1

    svg.append(
        f'''
<text
class="card-line"
x="25"
y="{y}"
fill="{MUTED}"
font-family="monospace"
font-size="12"
style="animation-delay:{delay:.2f}s">
{safe(key)}:
</text>

<text
class="card-line"
x="120"
y="{y}"
fill="{color}"
font-family="monospace"
font-size="12"
style="animation-delay:{delay:.2f}s">
{safe(value)}
</text>
'''
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

svg.append(
    '''
<text
class="card-line"
x="25"
y="315"
fill="#8b949e"
font-family="monospace"
font-size="11"
style="animation-delay:1s">
&gt; turning ideas into code_
</text>
'''
)


# --------------------------------------------------
# FINISH SVG
# --------------------------------------------------

svg.append("</svg>")


# --------------------------------------------------
# SAVE FILE
# --------------------------------------------------

OUTPUT_FILE.write_text(
    "".join(svg),
    encoding="utf-8",
)


print(f"Info card created: {OUTPUT_FILE}")
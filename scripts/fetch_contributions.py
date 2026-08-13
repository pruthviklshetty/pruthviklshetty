import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "pruthviklshetty"

URL = f"https://github.com/users/{USERNAME}/contributions"


# --------------------------------------------------
# 1. Download contribution calendar
# --------------------------------------------------

print(f"Fetching contributions for {USERNAME}...")

response = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0",
    },
    timeout=30,
)

response.raise_for_status()

print("Contribution calendar downloaded successfully!")


# --------------------------------------------------
# 2. Parse HTML
# --------------------------------------------------

html = response.text

print(f"Downloaded {len(html):,} characters.")

soup = BeautifulSoup(html, "html.parser")


# --------------------------------------------------
# 3. Find contribution cells
# --------------------------------------------------

days = soup.select(".ContributionCalendar-day")

print(f"Found {len(days)} contribution days.")


# --------------------------------------------------
# 4. Extract contribution data
# --------------------------------------------------

contributions = []

for day in days:

    date = day.get("data-date")
    level = day.get("data-level", "0")

    if date:

        try:
            level = int(level)
        except ValueError:
            level = 0

        contributions.append(
            {
                "date": date,
                "level": level,
            }
        )


# --------------------------------------------------
# 5. Save JSON
# --------------------------------------------------

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

output_file = data_dir / "contributions.json"

output_file.write_text(
    json.dumps(contributions, indent=2),
    encoding="utf-8",
)


print(f"Saved {len(contributions)} contribution records.")
print(f"Contribution data saved to {output_file}")
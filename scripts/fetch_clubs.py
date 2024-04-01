import json

import requests
from bs4 import BeautifulSoup

club_detail_url = "https://www.golf.co.nz/club-detail"

clubs = {}

with open("unused_club_ids.json", "r") as f:
    unused_ids = json.load(f)


for club_id in range(100, 1000):
    if club_id in unused_ids:
        continue

    print(f"Fetching club {club_id}")

    params = {
        "clubid": club_id
    }

    page = requests.get(club_detail_url, params=params)
    soup = BeautifulSoup(page.content, "html.parser")
    html = soup.prettify()
    html_lines = html.split("\n")

    title = soup.find("title")
    club_name = title.text.strip()
    if "System error" in club_name:
        unused_ids.append(int(club_id))
        continue

    suffix = " - Golf New Zealand"
    clubs[int(club_id)] = title.text.strip()[:-len(suffix)]

with open("clubs.json", "w") as f:
    f.write(json.dumps(clubs, indent=2))

with open("unused_club_ids.json", "w") as f:
    f.write(json.dumps(unused_ids, indent=2))

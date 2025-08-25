import json

import pendulum
import requests
from bs4 import BeautifulSoup

from .clubs import CLUBS
from .logger import log


def get_tee_times(booking_date: pendulum.DateTime, club_id: int) -> dict:
    state = {
        "updated_at": pendulum.now(),
        "booking_date": booking_date.to_date_string(),
        "club_id": club_id,
        "club_name": None,
        "tee_times": {}
    }

    booking_url = "https://www.golf.co.nz/Teebooking/SearchSlots.aspx"
    params = {
        "ClubId": club_id,
        "CourseId": None,
        "Date": booking_date.to_date_string(),
    }

    page = requests.get(
        booking_url,
        params=params
    )

    soup = BeautifulSoup(page.content, "html.parser")
    
    # Extract club name from page headers
    club_name = None
    # Look for h2 or h3 tags with "SPECIAL OFFERS at" or "Showing All Slots at" patterns
    for header in soup.find_all(['h2', 'h3']):
        header_text = header.get_text(strip=True)
        if 'Showing All Slots at' in header_text:
            # Extract club name between "at" and "on"
            if ' at ' in header_text and ' on ' in header_text:
                club_name = header_text.split(' at ')[1].split(' on ')[0].strip()
                break
    
    # Fallback: try to extract from competition names
    if not club_name:
        comp_table = soup.find('table', id='MainContent_competitionsTable')
        if comp_table:
            first_comp = comp_table.find('td')
            if first_comp and first_comp.text.strip():
                # Assume first word of competition name is club name
                comp_name = first_comp.text.strip()
                if ' ' in comp_name:
                    club_name = comp_name.split()[0]
    
    state["club_name"] = club_name

    table = soup.find('table', id="MainContent_TimeslotsTable")
    rows = table.find_all('tr')

    for i, row in enumerate(rows):
        time = row.find('td', class_="xtime")
        if not time:
            continue
        tee_time = pendulum.parse(f"{booking_date.to_date_string()} {time.text.zfill(5)}:00")

        available_slots = row.find_all('td', class_="xavail")
        booked_slots = row.find_all('td', class_="xbooked")

        state["tee_times"][tee_time.to_datetime_string()] = {
            "available_slots": len(available_slots),
            "booked_slots": len(booked_slots),
            "slots": [],
        }

        slots = row.find_all(True, {'class': ['xavail', 'xbooked']})

        for slot in slots:
            img = slot.find("img")

            if not img:
                continue

            title = img.get("title")
            if title == "Available":
                # Look for booking link
                booking_link = slot.find("a", class_="book_here_link")
                booking_id = None
                booking_url = None
                
                if booking_link:
                    booking_id = booking_link.get("id")
                    # Generate direct booking URL
                    booking_url = f"https://www.golf.co.nz/Teebooking/SearchSlots.aspx?ClubId={club_id}&Date={booking_date.to_date_string()}#{booking_id}"
                
                state["tee_times"][tee_time.to_datetime_string()]["slots"].append(
                    {
                        "affiliated": None,
                        "holes": None,
                        "handicap": None,
                        "gender": None,
                        "status": title,
                        "booking_id": booking_id,
                        "booking_url": booking_url
                    }
                )
                continue
            else:
                gender = title

            # Example: <i> Playing 9 holes </i>
            holes = slot.find("i")
            if holes and len(holes.text.split()) > 1:
                try:
                    holes = int(holes.text.split()[1])
                except ValueError:
                    holes = None
                affiliated = True
            else:
                affiliated = False
                holes = None

            # Example <font size="-2"> (36.9) </font>
            # or  <font size="-2"> (PEND) </font>
            handicap = slot.find("font")
            if handicap:
                handicap = handicap.text.lstrip("(").rstrip(")")

                try:
                    handicap = round(float(handicap), 1)
                except ValueError:
                    handicap = None

            state["tee_times"][tee_time.to_datetime_string()]["slots"].append(
                {
                    "affiliated": affiliated,
                    "holes": holes,
                    "handicap": handicap,
                    "gender": gender,
                    "status": "Booked",
                    "booking_id": None,
                    "booking_url": None
                }
            )

        log.debug(json.dumps(state, indent=2, default=str))

    return state

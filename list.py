import json
import sys

from clubs import CLUBS

FIELDS = ["name", "club_id", "url", "booking_url"]


def list_(fields):
    if not fields:
        fields = FIELDS

    for club_id, club_info in CLUBS.items():
        club_info["club_id"] = club_id
        output = {}
        for field in fields:
            output[field] = club_info[field]

        sys.stdout.write(json.dumps(output))
        sys.stdout.write("\n")

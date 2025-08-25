import json
import os
import pathlib
from typing import Optional

import pendulum

from .logger import log

ARCHIVE_DIR = os.getenv("ARCHIVE_DIR", "./clubs")
pathlib.Path(ARCHIVE_DIR).mkdir(parents=True, exist_ok=True)


def get_previous_state(booking_date: pendulum.DateTime, club_id: int) -> Optional[dict]:
    path = f"{ARCHIVE_DIR}/{club_id}/{booking_date.to_date_string()}"

    if not os.path.exists(path):
        return None

    files = os.listdir(path)
    if not files:
        return None

    log.info(f"Found latest state file: {path}/{max(files)}")
    with open(f"{path}/{max(files)}", "r") as f:
        return json.load(f)


def save_state(state: dict):
    booking_date = pendulum.parse(state["booking_date"])
    club_id = state["club_id"]
    updated_at = pendulum.instance(state["updated_at"])
    path = f"{ARCHIVE_DIR}/{club_id}/{booking_date.to_date_string()}/"

    pathlib.Path(path).mkdir(exist_ok=True, parents=True)
    with open(f"{path}/tee_times_{updated_at.int_timestamp}.json", "w") as f:
        json.dump(state, f, indent=2, default=str)

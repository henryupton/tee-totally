#!/usr/bin/env python3
import json

import pendulum

from clubs import CLUBS
from compare import compare_states
from logger import log
from scrape import get_tee_times
from state import get_previous_state
from state import save_state


def get(
        booking_date: pendulum.DateTime,
        club_id: int,
):
    log.info(f"Checking tee times for {booking_date.format('dddd Do [of] MMMM YYYY')} at {CLUBS[club_id]['name']}...")

    current_state: dict = get_tee_times(booking_date, club_id)
    previous_state: dict = get_previous_state(booking_date, club_id)
    if not previous_state:
        log.warning("No previous state found, saving current state...")
        save_state(current_state)
        return

    diff = compare_states(previous_state, current_state)
    if diff["any_changes"]:
        log.warning("Changes detected!")
        log.warning(json.dumps(diff, indent=2, default=str))

        save_state(current_state)
    else:
        log.info("No changes detected, discarding state file...")

    log.info(f"{booking_date.format('dddd Do [of] MMMM YYYY')}, done!")

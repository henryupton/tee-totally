#!/usr/bin/env python3
import json
import sys

import pendulum

from .logger import log
from .scrape import get_tee_times


def find_available_tee_times(
        club_id: int,
        from_timestamp: pendulum.DateTime,
        to_timestamp: pendulum.DateTime,
        time_range: str = None,
        min_free_slots: int = 1,
        min_playing_partners: int = None,
        allowed_days_of_week: tuple = None
) -> None:
    """Find available tee times for a club within a timestamp range."""
    
    available_times = []
    
    # Parse time_range if provided
    time_filter_start = None
    time_filter_end = None
    if time_range:
        try:
            start_time_str, end_time_str = time_range.split('-')
            time_filter_start = pendulum.parse(start_time_str.strip()).time()
            time_filter_end = pendulum.parse(end_time_str.strip()).time()
        except ValueError:
            log.error(f"Invalid time range format: {time_range}. Expected HH:MM-HH:MM")
            return
    
    # Get date range to search
    start_date = from_timestamp.date()
    end_date = to_timestamp.date()
    
    current_date = start_date
    while current_date <= end_date:
        booking_date = pendulum.instance(current_date)
        
        # Check day-of-week filter if specified
        if allowed_days_of_week:
            day_name = booking_date.format('dddd').lower()
            if day_name not in allowed_days_of_week:
                current_date = current_date + pendulum.duration(days=1)
                continue
        
        log.info(f"Searching tee times for {booking_date.to_date_string()}...")
        
        try:
            # Get tee times for this date
            tee_time_data = get_tee_times(booking_date, club_id)
            
            # Check each tee time in the response
            for tee_time_str, tee_time_info in tee_time_data.get("tee_times", {}).items():
                tee_time = pendulum.parse(tee_time_str)
                
                # Check if this tee time is within our timestamp range
                if from_timestamp <= tee_time <= to_timestamp:
                    # Apply time range filter if specified
                    if time_filter_start and time_filter_end:
                        tee_time_only = tee_time.time()
                        if not (time_filter_start <= tee_time_only <= time_filter_end):
                            continue
                    
                    available_slots = tee_time_info.get("available_slots", 0)
                    booked_slots = tee_time_info.get("booked_slots", 0)
                    
                    # Check minimum free slots requirement
                    if available_slots < min_free_slots:
                        continue
                    
                    # Check minimum playing partners requirement
                    if min_playing_partners is not None and booked_slots < min_playing_partners:
                        continue
                    
                    available_times.append({
                        "tee_time": tee_time_str,
                        "available_slots": available_slots,
                        "booked_slots": booked_slots,
                        "total_slots": len(tee_time_info.get("slots", [])),
                        "date": booking_date.to_date_string()
                    })
        
        except Exception as e:
            log.error(f"Error getting tee times for {booking_date.to_date_string()}: {e}")
        
        current_date = current_date + pendulum.duration(days=1)
    
    # Output results
    if available_times:
        log.info(f"Found {len(available_times)} available tee times:")
        for time_slot in available_times:
            sys.stdout.write(json.dumps(time_slot, indent=2, default=str))
            sys.stdout.write("\n")
    else:
        log.info("No available tee times found in the specified range.")
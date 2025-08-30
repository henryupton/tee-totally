#!/usr/bin/env python3
import json
import sys

import pendulum

from .logger import log
from .scrape import get_tee_times
from .clubs import CLUBS


def find_available_tee_times(
        club_ids: list,
        from_timestamp: pendulum.DateTime,
        to_timestamp: pendulum.DateTime,
        time_range: str = None,
        min_free_slots: int = 1,
        min_playing_partners: int = None,
        allowed_days_of_week: tuple = None
) -> list:
    """Find available tee times for multiple clubs within a timestamp range."""
    
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
            return []
    
    # Get date range to search
    start_date = from_timestamp.date()
    end_date = to_timestamp.date()
    
    # Iterate through each club
    for club_id in club_ids:
        log.info(f"Searching club {club_id}...")
        
        current_date = start_date
        while current_date <= end_date:
            booking_date = pendulum.instance(current_date)
            
            # Check day-of-week filter if specified
            if allowed_days_of_week:
                day_name = booking_date.format('dddd').lower()
                if day_name not in allowed_days_of_week:
                    current_date = current_date + pendulum.duration(days=1)
                    continue
            
            log.info(f"Searching tee times for club {club_id} on {booking_date.to_date_string()}...")
            
            try:
                # Get tee times for this date and club
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
                        
                        # Collect available slots with booking links
                        available_slot_details = []
                        for slot in tee_time_info.get("slots", []):
                            if slot.get("status") == "Available":
                                available_slot_details.append({
                                    "booking_id": slot.get("booking_id"),
                                    "booking_url": slot.get("booking_url")
                                })
                        
                        # Get club information (prefer scraped name over hardcoded)
                        scraped_club_name = tee_time_data.get("club_name")
                        club_info = CLUBS.get(club_id, {})
                        club_name = scraped_club_name or club_info.get("name", f"Club {club_id}")
                        
                        # Generate unique ID: <club_id>-<unix_epoch_tee_time>
                        unique_id = f"{club_id}-{int(tee_time.timestamp())}"
                        
                        result = {
                            "id": unique_id,
                            "tee_time": tee_time_str,
                            "available_slots": available_slots,
                            "booked_slots": booked_slots,
                            "total_slots": len(tee_time_info.get("slots", [])),
                            "date": booking_date.to_date_string(),
                            "day_of_week": tee_time.format("dddd").lower(),
                            "club_name": club_name,
                            "club_id": club_id,
                            "booking_links": available_slot_details,
                            "search_url": f"https://www.golf.co.nz/Teebooking/SearchSlots.aspx?ClubId={club_id}&Date={booking_date.to_date_string()}"
                        }
                        
                        available_times.append(result)
        
            except Exception as e:
                log.error(f"Error getting tee times for club {club_id} on {booking_date.to_date_string()}: {e}")
            
            current_date = current_date + pendulum.duration(days=1)
    
    # Output results
    if available_times:
        log.info(f"Found {len(available_times)} available tee times:")
        for time_slot in available_times:
            sys.stdout.write(json.dumps(time_slot, indent=2, default=str))
            sys.stdout.write("\n")
    else:
        log.info("No available tee times found in the specified range.")
    
    # Return results for notifications and further processing
    return available_times
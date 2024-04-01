from main import compare_states

state_a = {
    "updated_at": "2024-03-29T20:36:18.822518+13:00",
    "booking_date": "2024-04-01",
    "club_id": 341,
    "tee_times": {
        "2024-04-01 10:34:00": {
            "available_slots": 0,
            "booked_slots": 4,
            "slots": [
                {
                    "member": True,
                    "holes": 18,
                    "handicap": None,
                    "gender": None,
                    "status": "Booked"
                },
                {
                    "member": True,
                    "holes": 18,
                    "handicap": None,
                    "gender": None,
                    "status": "Booked"
                },
                {
                    "member": True,
                    "holes": 18,
                    "handicap": None,
                    "gender": None,
                    "status": "Booked"
                },
                {
                    "member": True,
                    "holes": 18,
                    "handicap": None,
                    "gender": None,
                    "status": "Booked"
                }
            ]
        }
    }
}

state_b = {
    "updated_at": "2024-03-29T20:36:18.822518+13:00",
    "booking_date": "2024-04-01",
    "club_id": 341,
    "tee_times": {
        "2024-04-01 10:34:00": {
            "available_slots": 0,
            "booked_slots": 4,
            "slots": [
                {
                    "member": True,
                    "holes": 18,
                    "handicap": None,
                    "gender": None,
                    "status": "Booked"
                },
                {
                    "member": True,
                    "holes": 18,
                    "handicap": None,
                    "gender": None,
                    "status": "Booked"
                },
                {
                    "member": True,
                    "holes": 18,
                    "handicap": None,
                    "gender": None,
                    "status": "Booked"
                },
                {
                    "member": False,
                    "holes": 18,
                    "handicap": None,
                    "gender": None,
                    "status": "Booked"
                }
            ]
        }
    }
}


def test_compare_states():
    diff = compare_states(state_a, state_b)

    assert diff["changes"]["2024-04-01 10:34:00"]["slots"][3] == {'member': {'new': False, 'old': True}}

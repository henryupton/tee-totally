from logger import log


def compare_states(a: dict, b: dict) -> dict:
    diff = {
        "tee_times_added": set(),
        "tee_times_removed": set(),
        "tee_times_changed": set(),
        "any_changes": False,
        "changes": {}
    }

    tee_times_a = set(a["tee_times"])
    tee_times_b = set(b["tee_times"])
    tee_times_all = tee_times_a.union(tee_times_b)

    if tee_times_a == tee_times_b:
        log.debug("Both states being compared are identical!")
        pass
    elif tee_times_a.issubset(tee_times_b):
        diff["tee_times_removed"] = tee_times_a.difference(tee_times_b)

    elif tee_times_b.issubset(tee_times_a):
        log.debug("Tee times have been added since the last update!")
        diff["tee_times_added"] = tee_times_b.difference(tee_times_a)

    for tee_time in tee_times_all:
        tee_time_a = a["tee_times"][tee_time]
        tee_time_b = b["tee_times"][tee_time]

        if tee_time_a == tee_time_b:
            continue

        diff["changes"][tee_time] = {}
        diff["changes"][tee_time]["slots"] = [{} for _ in range(4)]
        for i, slots in enumerate(zip(tee_time_a["slots"], tee_time_b["slots"])):
            slot_a, slot_b = slots
            if slot_a == slot_b:
                continue

            diff["any_changes"] = True
            slot_attributes = list(slot_a)
            for slot_attribute in slot_attributes:
                if slot_a[slot_attribute] == slot_b[slot_attribute]:
                    continue
                diff["changes"][tee_time]["slots"][i][slot_attribute] = {
                    "old": slot_a[slot_attribute],
                    "new": slot_b[slot_attribute],
                }

    return diff

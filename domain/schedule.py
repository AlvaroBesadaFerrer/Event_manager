from domain.restrictions_data import generate_restrictions
from json_storage.save_load_data import load_data, save_data

RESTRICTIONS = generate_restrictions()

def add_event(event):
    events = load_data()
    if validate_event(event, events):
        events.append(event)
        save_data(events)
        return True
    else:
        return False

def validate_event(event, events):
    return check_time_conflicts(event, events) and check_restrictions(event)


def check_restrictions(event):
    for restriction in RESTRICTIONS:
        if not (restriction.is_satisfied(event)):
            return False
    return True


def check_time_conflicts(event, events):
    for e in events:
        if event.intersection(e):
            if not event.check_resources_availability(e):
                return False
    return True
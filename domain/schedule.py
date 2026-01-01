from .restrictions_data import restrictions_data
from json_storage.save_load_data import events
from .resources_data import RESOURCES
from json_storage.save_load_data import save_data


def add_event(event):
    if validate_event(event):
        events.append(event)
        save_data(events)

def validate_event(event):
    return check_time_conflicts(event) and check_restrictions(event)

def check_restrictions(event):
    for restriction in restrictions_data:
        if not (restriction.is_satisfied(event)):
            return False
    return True


def check_time_conflicts(event):
    for e in events:
        if event.intersection(e):
            if not event.check_resources_availability(e):
                return False
    return True
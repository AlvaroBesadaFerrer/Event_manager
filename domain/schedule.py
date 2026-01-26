from domain.restrictions_data import generate_restrictions
from json_storage.save_load_data import load_data, save_data
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from domain.event import Event


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

def set_possible_event_date_time(possible_event, start_time, end_time):
    possible_event.date=start_time.date()
    possible_event.start_time=start_time.time()
    possible_event.end_time=end_time.time()

    return possible_event


def auto_schedule_event(possible_event, duration):
    
    events = load_data()
    
    current_time = datetime.now(ZoneInfo("America/Havana"))
    start_time = current_time
    end_time = start_time + timedelta(minutes=duration)
    max_end_date = current_time + timedelta(days=7)

    possible_event = set_possible_event_date_time(possible_event, start_time, end_time)

    while not check_time_conflicts(possible_event, events):

        possible_event = set_possible_event_date_time(possible_event, start_time, end_time)
        
        if start_time > max_end_date:
            return False
        
        start_time += timedelta(minutes=5)
        end_time = start_time + timedelta(minutes=duration)

    events.append(possible_event)
    save_data(events)
    return True




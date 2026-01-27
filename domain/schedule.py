from domain.restrictions_data import generate_restrictions
from json_storage.save_load_data import load_data, save_data
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from domain.event import Event


RESTRICTIONS = generate_restrictions()

def add_event(event):
    events = load_data()
    response = validate_event(event, events)
    if not response:
        events.append(event)
        save_data(events)
    else:
        return response

def validate_event(event, events):

    time_conflict_error = check_time_conflicts(event, events)
    if time_conflict_error:
        return time_conflict_error
    
    restriction_error = check_restrictions(event)
    if restriction_error:
        return restriction_error


def check_restrictions(event):
    for restriction in RESTRICTIONS:
        conflict = restriction.is_satisfied(event)
        if conflict:
            return conflict


def check_time_conflicts(event, events):
    for e in events:
        if event.intersection(e):
            conflict = event.check_resources_availability(e)
            if conflict:
                return conflict

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

    while check_time_conflicts(possible_event, events):

        possible_event = set_possible_event_date_time(possible_event, start_time, end_time)
        
        if start_time > max_end_date:
            return False
        
        start_time += timedelta(minutes=5)
        end_time = start_time + timedelta(minutes=duration)

    events.append(possible_event)
    save_data(events)
    return True




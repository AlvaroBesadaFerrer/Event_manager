from domain.restrictions_data import generate_restrictions
from json_storage.save_load_data import load_data, save_data
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo


RESTRICTIONS = generate_restrictions()
events = load_data()


def add_event(event):
    events.append(event)
    save_data(events)
    return []

def validate_event(event):

    return check_time_conflicts(event) + check_restrictions(event)


def check_restrictions(event):
    return_errors = []
    for restriction in RESTRICTIONS:
        conflict = restriction.is_satisfied(event)
        if conflict:
            return_errors.append(conflict)
    return return_errors


def check_time_conflicts(event):
    return_errors = []
    for e in events:
        if event.intersection(e):
            conflict = event.check_resources_availability(e)
            if conflict:
                return_errors.extend(conflict)
    return return_errors

def set_possible_event_date_time(possible_event, start_time, end_time):
    possible_event.start_time=start_time
    possible_event.end_time=end_time

    return possible_event


def auto_schedule_event(possible_event, duration):
    
    current_time = datetime.now(ZoneInfo("America/Havana"))
    start_time = current_time
    end_time = start_time + timedelta(minutes=duration)
    max_end_date = current_time + timedelta(days=7)

    possible_event = set_possible_event_date_time(possible_event, start_time, end_time)

    while True:
        if start_time > max_end_date:
            return ["No se pudo encontrar un horario adecuado dentro de los próximos 7 días."]
        
        possible_event = set_possible_event_date_time(possible_event, start_time, end_time)
        if not check_time_conflicts(possible_event):
            break
        
        start_time += timedelta(minutes=5)
        end_time = start_time + timedelta(minutes=duration)

    events.append(possible_event)
    save_data(events)
    return []

def check_workers_requirements(workers):
    errors = []
    if not workers:
        errors.append("Debe seleccionar al menos un trabajador.")
    return errors

def check_time_requirements(use_auto_scheduler, start_time, end_time):
    errors = []

    if start_time is None or end_time is None:
        errors.append("Debe proporcionar una fecha y hora válidas.")
        return errors

    if not use_auto_scheduler and (end_time <= start_time):
        errors.append("La **hora de fin** debe ser posterior a la **hora de inicio**.")

    current_time = datetime.now(ZoneInfo("America/Havana"))
    if not use_auto_scheduler and start_time < current_time:
        errors.append("La **hora de inicio** tiene que ser posterior a la **hora actual**.")
    
    return errors

def check_work_hours(start_time, end_time):
    work_starts = time(8,0)
    work_ends = time(5,0)
    
    #TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    #ponerlo todo como datetime, no como date y time por separado
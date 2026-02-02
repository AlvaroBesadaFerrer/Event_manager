from json_storage.save_load_data import load_data, save_data
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from schedule_events.validators import check_time_conflicts, check_restrictions, check_work_hours


events = load_data()

def add_event(event):
    """Agrega un evento después de validar conflictos de tiempo y restricciones"""
    events.append(event)
    save_data(events)
    return []


def validate_event(event):
    """Valida un evento comprobando conflictos de tiempo y restricciones"""

    return check_time_conflicts(event, events) + check_restrictions(event)


def set_possible_event_date_time(possible_event, start_time, end_time):
    """Va cambiando la fecha y hora de inicio y fin de un evento cuando se esta programando automáticamente"""

    possible_event.start_time = start_time
    possible_event.end_time = end_time

    return possible_event
    

def auto_schedule_event(possible_event, duration):
    """Programa automáticamente un evento buscando un horario adecuado dentro de los próximos 7 días"""

    current_time = datetime.now(ZoneInfo("America/Havana"))
    start_time = current_time
    end_time = start_time + timedelta(minutes=duration)
    max_end_date = current_time + timedelta(days=7)

    possible_event = set_possible_event_date_time(possible_event, start_time, end_time)

    while True:
        if start_time > max_end_date:
            return ["No se pudo encontrar un horario adecuado dentro de los próximos 7 días."]
        
        possible_event = set_possible_event_date_time(possible_event, start_time, end_time)
        if not check_time_conflicts(possible_event, events) and not check_work_hours(start_time, end_time):
            break
        
        start_time += timedelta(minutes=5)
        end_time = start_time + timedelta(minutes=duration)

    events.append(possible_event)
    save_data(events)
    return []

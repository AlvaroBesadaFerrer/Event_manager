from domain.restrictions_data import generate_restrictions
from datetime import time


RESTRICTIONS = generate_restrictions()

def check_restrictions(event):
    """Valida todas las restricciones para un evento y devuelve una lista de mensajes de error si alguna no se cumple"""
    return_errors = []
    for restriction in RESTRICTIONS:
        conflict = restriction.is_satisfied(event)
        if conflict:
            return_errors.append(conflict)
    return return_errors


def check_time_conflicts(event, events):
    """Valida conflictos de tiempo entre un evento y la lista de eventos y devuelve una lista de mensajes de error para todos los conflictos encontrados"""
    return_errors = []
    for e in events:
        if event.intersection(e):
            conflict = event.check_resources_availability(e)
            if conflict:
                return_errors.extend(conflict)
    return return_errors


def check_work_hours(start_time, end_time):
    """Valida que un evento esté dentro del horario laboral (8:00 am a 5:00 pm) y devuelve un mensaje de error si no lo está"""
    work_starts = time(8,0)
    work_ends = time(17,0)
    
    if (start_time.time() < work_starts or end_time.time() > work_ends) or (start_time.date() != end_time.date()):
        return ["Hora de inicio o de fin fuera del horario de trabajo (de 8:00 am a 5:00 pm)"]
    else:
        return []


def check_workers_requirements(workers):
    """Valida que se haya seleccionado al menos un trabajador para el evento"""
    errors = []
    if not workers:
        errors.append("Debe seleccionar al menos un trabajador.")
    return errors


def check_time_requirements(use_auto_scheduler, start_time, end_time):
    """Valida que las horas de inicio y fin sean correctas según si se usa o no el programador automático"""
    errors = []

    if start_time is None or end_time is None:
        errors.append("Debe proporcionar una fecha y hora válidas.")
        return errors

    if not use_auto_scheduler and (end_time <= start_time):
        errors.append("La **hora de fin** debe ser posterior a la **hora de inicio**.")

    # current_time = datetime.now(ZoneInfo("America/Havana"))
    # if not use_auto_scheduler and start_time < current_time:
    #    errors.append("La **hora de inicio** tiene que ser posterior a la **hora actual**.")
    
    return errors

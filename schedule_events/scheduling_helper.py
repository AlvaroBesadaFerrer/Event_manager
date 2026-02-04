from utils.time_utils import parse_start_end_date_time
from utils.format_utils import create_possible_event
from schedule_events.schedule import add_event, auto_schedule_event,  validate_event
from schedule_events.validators import check_work_hours, check_restrictions, check_time_requirements, check_workers_requirements


def schedule_event_helper(
    use_auto_scheduler,
    spot,
    event_type,
    workers,
    resources,
    color,
    date=None,
    start_time=None,
    end_time=None,
    duration=0,
):
    """Función auxiliar para programar un evento, ya sea usando el planificador automático o ingresando los datos manualmente"""
    
    errors = []
    if use_auto_scheduler:  # Si se usa el planificador automático, se validan los trabajadores y restricciones, y se intenta programar automáticamente el evento
        errors.extend(check_workers_requirements(workers))

        possible_event = create_possible_event(
            spot=spot,
            event_type=event_type,
            workers=workers,
            resources=resources,
            color=color,
        )
        
        errors.extend(check_restrictions(possible_event))
        
        if not errors:
            errors.extend(auto_schedule_event(possible_event, duration))
        
    else:  # Si no se usa el planificador automático, se validan los datos ingresados y se intenta agregar el evento en el horario seleccionado
        submit_start, submit_end = parse_start_end_date_time(date, start_time, end_time)
        
        errors.extend(check_workers_requirements(workers))
        errors.extend(check_work_hours(submit_start, submit_end))
        errors.extend(check_time_requirements(use_auto_scheduler, submit_start, submit_end))

        possible_event = create_possible_event(
            spot=spot,
            event_type=event_type,
            workers=workers,
            resources=resources,
            color=color,
            start_time=submit_start,
            end_time=submit_end,
        )

        errors.extend(validate_event(possible_event))

        if not errors:
            errors.extend(add_event(possible_event))
    return errors
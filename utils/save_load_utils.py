from uuid import uuid4
from domain.event import Event
from utils.filter_utils import filter_resource_by_id, filter_resources_list_by_id
from domain.resources_data import get_resources
from utils.time_utils import datetime_to_str, str_to_datetime


def resources_to_list(resources):
    """Convierte una lista de recursos en una lista de IDs de recursos"""
    return [r.resource_id for r in resources]


def parse_event_with_ids(event):
    """Convierte un objeto Event en un diccionario con los IDs de los recursos en lugar de objetos de recursos completos"""
    return {
        "id": event.id,
        "spot": event.spot.resource_id,
        "event_type": event.event_type.resource_id,
        "workers": resources_to_list(event.workers),
        "resources": resources_to_list(event.resources),
        "start_time": datetime_to_str(event.start_time) if event.start_time else None,
        "end_time": datetime_to_str(event.end_time) if event.end_time else None,
        "color": event.color,
    }


def parse_save_data(event_data):
    """Convierte los datos de eventos en un formato más fácil para guardar"""
    parsed_data = []

    for event in event_data:
        
        parsed_data.append(
            parse_event_with_ids(event)
        )
        
    return parsed_data


def to_object(data):
    """Convierte un diccionario de datos guardados en un objeto Event"""

    spot = filter_resource_by_id(get_resources(), data["spot"])
    event_type = filter_resource_by_id(get_resources(), data["event_type"])

    if spot is None or event_type is None:
        return None
    
    try:
        start_time = str_to_datetime(data["start_time"]) if data.get("start_time") else None
        end_time = str_to_datetime(data["end_time"]) if data.get("end_time") else None
        
        return Event(
            id=data.get("id", str(uuid4())),
            spot=spot,
            event_type=event_type,
            workers=filter_resources_list_by_id(get_resources(), data["workers"]),
            resources=filter_resources_list_by_id(get_resources(), data["resources"]),
            start_time=start_time,
            end_time=end_time,
            color=data["color"],
        )
    except (KeyError, ValueError, TypeError) as e:  # Para manejar de errores si faltan claves o hay errores en el JSON porque no se guardó bien o se editó mal
        return None

def load_events_from_dict(event_data):
    """Carga una lista de eventos desde una lista de diccionarios de datos guardados"""
    
    return_data = []
    for e in event_data:
        obj = to_object(e)
        if obj:
            return_data.append(obj)

    return return_data
from domain.event import Event
from utils.filter_utils import filter_resource_by_id, filter_resources_list_by_id
from domain.resources_data import get_resources
from utils.time_utils import parse_date, parse_time

def resource_to_dict(resource):
    return resource.resource_id

def resources_to_dict(resources):
    return [resource_to_dict(r) for r in resources]


def parse_event(event):
    
    return {
        "id": event.id,
        "spot": resource_to_dict(event.spot),
        "event_type": resource_to_dict(event.event_type),
        "workers": resources_to_dict(event.workers),
        "resources": resources_to_dict(event.resources),
        "start_date": event.date.strftime('%Y-%m-%d'),
        "start_time": event.start_time.strftime('%H:%M:%S'),
        "end_time": event.end_time.strftime('%H:%M:%S'),
        "color": event.color,
    }


def parse_save_data(event_data):
    parsed_data = []

    for event in event_data:
        
        parsed_data.append(
            parse_event(event)
        )
        
    return parsed_data


def to_object(data):
    try:
        return Event(
            id=data["id"],
            spot=filter_resource_by_id(get_resources(), data["spot"]),
            event_type=filter_resource_by_id(get_resources(), data["event_type"]),
            workers=filter_resources_list_by_id(get_resources(), data["workers"]),
            resources=filter_resources_list_by_id(get_resources(), data["resources"]),
            date=parse_date(data["start_date"]),
            start_time=parse_time(data["start_time"]),
            end_time=parse_time(data["end_time"]),
            color=data["color"],
        )
    except KeyError as e:
        raise ValueError(f"Invalid saved data, missing key: {e}")

def load_events_from_dict(event_data):
    
    return_data = []
    for e in event_data:
        return_data.append(to_object(e))
    
    return return_data
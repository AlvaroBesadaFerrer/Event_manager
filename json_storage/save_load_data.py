import json
from utils.save_load_utils import parse_save_data, load_events_from_dict


def save_data(event_data):

    data = parse_save_data(event_data)
    
    with open("event_data.json", "w") as f:
        json.dump(data, f, indent=4)


def load_data():

    try:
        with open("event_data.json", "r") as f:
            event_data = json.load(f)
    except FileNotFoundError:
        event_data = []
    
    events = load_events_from_dict(event_data)
    return events

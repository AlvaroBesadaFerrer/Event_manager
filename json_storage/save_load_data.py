import json
from utils.save_load_utils import parse_save_data, load_events_from_dict


def save_data(event_data):
    """Guarda los datos de eventos en un archivo JSON"""

    data = parse_save_data(event_data)
    
    with open("event_data.json", "w") as f:
        json.dump(data, f, indent=4)


def load_data():
    """Carga los datos de eventos desde el archivo JSON"""

    try:
        with open("event_data.json", "r") as f:
            event_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):  # Maneja el caso donde el archivo no existe o está corrupto
        return []

    # Valida que los datos cargados sean una lista
    if not isinstance(event_data, list):
        return []
    
    events = load_events_from_dict(event_data)
    return events

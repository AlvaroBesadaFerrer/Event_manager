import json

def save_data(event_data):
    with open("event_data.json", "w") as f:
        json.dump(event_data, f)

def load_data():
    try:
        with open("event_data.json", "r") as f:
            event_data = json.load(f)
    except FileNotFoundError:
        event_data = []
    return event_data
import json
from domain.event import Event


events = []

def save_data(event_data):

    data = []
    for event in event_data:
        data.append(
            {
                "id": event.id,
                "spot": event.spot,
                "event_type": event.event_type,
                "workers": event.workers,
                "resources": event.resources,
                "start_date": event.date,
                "start_time": event.start_time,
                "end_time": event.end_time,
                "color": event.color,
            }
        )

    with open("event_data.json", "w") as f:
        json.dump(data, f, indent=4)


def load_data():
    try:
        with open("event_data.json", "r") as f:
            event_data = json.load(f)
    except FileNotFoundError:
        event_data = []
    
    for event in event_data:
        events.append(
            Event(
                id=event["id"],
                spot=event["spot"],
                event_type=event["event_type"],
                workers=event["workers"],
                resources=event["resources"],
                date=event["start_date"],
                end_time=event["end_time"],
                start_time=event["start_time"],
                color=event["color"]
            )
        )
from domain.event import Event
from uuid import uuid4

def list_to_string(lista):
    # Cambiamos las listas por strings porque los st.dataframe y st.table no soportan listas y da un warning en la consola
    output = ""
    n = len(lista)

    for i in range(n):
        if i != 0:
            output+= ", "
        output+=lista[i].name

    return output.strip()


def show_details(event):

    return {
        "spot": event.spot.name,
        "event_type": event.event_type.name,
        "workers": list_to_string(event.workers),
        "resources": list_to_string(event.resources),
        "start_date": event.date.strftime('%Y-%m-%d'),
        "start_time": event.start_time.strftime('%H:%M:%S'),
        "end_time": event.end_time.strftime('%H:%M:%S'),
    }

def create_possible_event(spot, event_type, workers, resources, color, date=None, start_time=None, end_time=None):
    return Event(
        id=str(uuid4()),
        spot=spot,
        event_type=event_type,
        workers=workers,
        resources=resources,
        date=date,
        start_time=start_time,
        end_time=end_time,
        color=color,
    )
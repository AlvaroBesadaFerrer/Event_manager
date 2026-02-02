from domain.event import Event
from uuid import uuid4
from json_storage.save_load_data import load_data
from domain.resources_data import get_resources
from utils.filter_utils import filter_resource_by_id

def list_to_string(lista):
    """Cambiamos las listas por strings porque los st.dataframe y st.table no soportan listas y muestra una advertencia en la consola"""
    output = ""
    n = len(lista)

    for i in range(n):
        if i != 0:
            output+= ", "
        output+=lista[i].name

    return output.strip()


def show_details(event):
    """Muestra los detalles de un evento en un formato legible"""
    return {
        "spot": event.spot.name,
        "event_type": event.event_type.name,
        "workers": list_to_string(event.workers),
        "resources": list_to_string(event.resources),
        "start_time": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
    }


def show_resources_details():
    """
    Muestra los detalles de los recursos en un formato legible
    Recorre todos los eventos y agrupa la información de los eventos por recurso.
    Devuelve un diccionario donde las claves son los nombres de los recursos y los valores son cadenas de texto con los detalles de los eventos asociados a cada recurso.
    Los detalles de cada evento son el tipo de evento, la hora de inicio y la hora de fin.
    """
    events = load_data()
    resources = get_resources()

    response = {}

    for e in events:
        all_resources = e.resources + e.workers + [e.spot] + [e.event_type]

        event_info = f"{e.event_type.name}, {e.start_time.strftime('%Y-%m-%d %H:%M:%S') if e.start_time else 'N/A'}, {e.end_time.strftime('%Y-%m-%d %H:%M:%S') if e.end_time else 'N/A'}"

        for item in all_resources:

            res = filter_resource_by_id(resources, getattr(item, 'resource_id', None))
            if not res:
                res_name = getattr(item, 'name', 'Desconocido')
            else:
                res_name = res.name

            if res_name not in response:
                response[res_name] = []

            response[res_name].append(event_info)

    for key in list(response.keys()):  # Convertir listas a cadenas de texto porque los st.dataframe y st.table no soportan mostrar listas
        response[key] = '; '.join(response[key])

    return response

def create_possible_event(spot, event_type, workers, resources, color, start_time=None, end_time=None):
    """Crea un evento posible con los parámetros dados y un ID único"""
    return Event(
        id=str(uuid4()),
        spot=spot,
        event_type=event_type,
        workers=workers,
        resources=resources,
        start_time=start_time,
        end_time=end_time,
        color=color,
    )
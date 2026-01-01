import streamlit as st
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from domain.event import Event
from domain.resources_data import get_resources
from uuid import uuid4
from utils.filter_utils import filter_resources_by_type
from domain.resource import ResourcesType
from domain.schedule import add_event


st.set_page_config(page_title="Agregar evento", page_icon=":hammer_and_wrench:")


st.markdown("# Agregar evento :red_car:")
st.subheader("Detalles del evento")

spot = st.selectbox(
    "Lugar del evento:",
    options = filter_resources_by_type(get_resources(), ResourcesType.Area_de_trabajo),
    format_func = lambda x: x.name,
)
event_type = st.selectbox(
    "Tipo de evento:",
    options = filter_resources_by_type(get_resources(), ResourcesType.Tipo_de_evento),
    format_func = lambda x: x.name,
)
workers = st.multiselect(
    "Trabajadores:",
    options = filter_resources_by_type(get_resources(), ResourcesType.Trabajador),
    format_func = lambda x: x.name,
)
st.markdown("Herramientas:")

resources = []
for i in filter_resources_by_type(get_resources(), ResourcesType.Herramienta):
    if st.checkbox(i.name):
        resources.append(i)

color = st.color_picker("Color del evento:", value="#3498db")

current_time = datetime.now(ZoneInfo('America/Havana'))

date = str(st.date_input("Fecha: ", value= current_time))
start_time = str(st.time_input("Hora de inicio: ", value= current_time))
end_time = str(st.time_input("Hora de fin: ", value= current_time + timedelta(minutes = 30)))

button = st.button("Agregar evento", on_click=None)

if button:

    response = add_event(
        Event(
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
    )

    if response:
        st.success("Evento guardado con éxito!", icon="✅")
    else: 
        st.error("Error en las restricciones", icon="🚨")



# TODO: Add validation for time inputs (end time should be after start time) and midnight work?
# Add all validations before saving the event
# Add business logic to avoid overlapping events in the same spot
# Consider adding a description field for more event details
# Implement editing and deleting events functionality
# Implement when clicking an event in the timeline, show its details
# AI integration for suggesting how to optimize scheduling based on past events
# Mark as done
# Font color adjustment based on background color for better readability
# Emojis de los recursos en la seleccion
import streamlit as st
from datetime import datetime, timedelta
from json_storage.save_load_data import save_data
from zoneinfo import ZoneInfo
from domain.event import Event
from main import events
from enums import TRABAJADORES, EVENTS, SPOTS, RESOURCES


st.set_page_config(page_title="Agregar evento", page_icon=":hammer_and_wrench:")


st.markdown("# Agregar evento :red_car:")

st.subheader("Detalles del evento")
spot = st.selectbox("Lugar del evento:", options = SPOTS)
event_type = st.selectbox("Tipo de evento:", options = EVENTS)
workers = st.multiselect("Trabajadores:", options = TRABAJADORES)
st.markdown("Recursos:")

resources = []
for i in RESOURCES:
    if st.checkbox(i):
        resources.append(i)

color = st.color_picker("Color del evento:", value="#3498db")

current_time = datetime.now(ZoneInfo('America/Havana'))

date = str(st.date_input("Fecha: ", value= current_time))
start_time = str(st.time_input("Hora de inicio: ", value= current_time))
end_time = str(st.time_input("Hora de fin: ", value= current_time + timedelta(minutes = 30)))

button = st.button("Agregar evento", on_click=None)

if button:
    st.success("Evento guardado con éxito!", icon="✅")

    events.append(
        Event(
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

    save_data(events)


# TODO: Add validation for time inputs (end time should be after start time) and midnight work?
# Add all validations before saving the event
# Add business logic to avoid overlapping events in the same spot
# Consider adding a description field for more event details
# Implement editing and deleting events functionality
# Implement when clicking an event in the timeline, show its details
# AI integration for suggesting how to optimize scheduling based on past events
# Mark as done
# Font color adjustment based on background color for better readability

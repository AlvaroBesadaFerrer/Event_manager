import streamlit as st
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from domain.event import Event
from domain.resources_data import get_resources
from uuid import uuid4
from utils.filter_utils import filter_resources_by_type
from domain.resource import ResourcesType
from domain.schedule import add_event, auto_schedule_event, check_restrictions


st.set_page_config(page_title="Agregar evento", page_icon=":hammer_and_wrench:")

st.markdown("# Agregar evento :red_car:")
st.subheader("Detalles del evento")


all_resources = get_resources()


use_auto_scheduler = st.toggle("Usar planificador automático?", value=False)

date = None
start_time = None
end_time = None
duration = 0


def error_message(errors):
    if not errors:
        st.success("Evento guardado con éxito!", icon="✅")
    else:
        for e in errors:
            st.error(f'**Error:** {e}', icon="🚨")


with st.form("add_event_form"):
    spot = st.selectbox(
        "Lugar del evento:",
        options=filter_resources_by_type(all_resources, ResourcesType.Area_de_trabajo),
        format_func=lambda x: x.name,
    )

    event_type = st.selectbox(
        "Tipo de evento:",
        options=filter_resources_by_type(all_resources, ResourcesType.Tipo_de_evento),
        format_func=lambda x: x.name,
    )

    workers = st.multiselect(
        "Trabajadores:",
        options=filter_resources_by_type(all_resources, ResourcesType.Trabajador),
        format_func=lambda x: x.name,
    )

    st.markdown("Herramientas:")
    resources = []
    for i in filter_resources_by_type(all_resources, ResourcesType.Herramienta):
        if st.checkbox(i.name, key=f"tool_{i.resource_id}"):
            resources.append(i)

    color = st.color_picker("Color del evento:", value="#3498db")
    
    current_time = datetime.now(ZoneInfo("America/Havana"))
    
    if not use_auto_scheduler:
        date = st.date_input("Fecha: ", value=current_time)
        start_time = st.time_input("Hora de inicio: ", value=current_time)
        end_time = st.time_input("Hora de fin: ", value=current_time + timedelta(minutes=30))
    else:
        duration = st.slider("Duración del evento (minutos):", min_value=20, max_value=180, value=60)

    submitted = st.form_submit_button("Agregar evento")

if submitted:
    errors = []
    if not workers:
        errors.append("Debe seleccionar al menos un trabajador.")
    
    if not use_auto_scheduler and (end_time <= start_time):
        errors.append("La hora de fin debe ser posterior a la hora de inicio.")

    if use_auto_scheduler:
        possible_event = Event(
            id=str(uuid4()),
            spot=spot,
            event_type=event_type,
            workers=workers,
            resources=resources,
            date=None,
            start_time=None,
            end_time=None,
            color=color
        )
        
        errors.extend(check_restrictions(possible_event))
        
        if not errors:
            errors.extend(auto_schedule_event(possible_event, duration))
        
        error_message(errors)
        
    else:
        errors.extend(
            add_event(
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
        )

        error_message(errors)


# TODO: Add validation for time inputs (end time should be after start time) and midnight work?
#X Add all validations before saving the event
#X Add business logic to avoid overlapping events in the same spot
# Consider adding a description field for more event details
#X Implement editing and deleting events functionality
#X Implement when clicking an event in the timeline, show its details
# AI integration for suggesting how to optimize scheduling based on past events
# Mark as done
#X Font color adjustment based on background color for better readability
# Emojis de los recursos en la seleccion
# Review las restricciones bien
# Hacer Readme con todo lo q tienen q instalar para correrlo
# comentarios y tipos de datos
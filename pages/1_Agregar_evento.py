import streamlit as st
from domain.resources_data import get_resources
from utils.filter_utils import filter_resources_by_type
from utils.time_utils import parse_start_end_date_time
from utils.format_utils import create_possible_event
from domain.resource import ResourcesType
from domain.schedule import add_event, auto_schedule_event, check_work_hours, check_restrictions, validate_event, check_time_requirements, check_workers_requirements


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
            st.error(e, icon="🚨")


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
    
    
    if not use_auto_scheduler:
        date = st.date_input("Fecha: ")
        start_time = st.time_input("Hora de inicio: ")
        end_time = st.time_input("Hora de fin: ")
    else:
        duration = st.slider("Duración del evento (minutos):", min_value=20, max_value=480, value=60)

    submitted = st.form_submit_button("Agregar evento")

if submitted:
    
    errors = []

    if use_auto_scheduler:
        errors.extend(check_workers_requirements(workers))

        possible_event = create_possible_event(
            spot=spot,
            event_type=event_type,
            workers=workers,
            resources=resources,
            color=color,
        )
        
        errors.extend(check_restrictions(possible_event))
        
        if not errors:
            errors.extend(auto_schedule_event(possible_event, duration))
        
        error_message(errors)
        
    else:
        submit_start, submit_end = parse_start_end_date_time(date, start_time, end_time)
        
        errors.extend(check_workers_requirements(workers))
        errors.extend(check_work_hours(submit_start, submit_end))
        errors.extend(check_time_requirements(use_auto_scheduler, submit_start, submit_end))

        possible_event = create_possible_event(
            spot=spot,
            event_type=event_type,
            workers=workers,
            resources=resources,
            color=color,
            start_time=submit_start,
            end_time=submit_end,
        )

        errors.extend(validate_event(possible_event))

        if not errors:
            errors.extend(add_event(possible_event))

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
# Add 2-3 more workers
# Poner un .py que cuando se ejecute resetee el json y ponga unos datos de prueba en el json con un hora actual
import streamlit as st
from domain.resources_data import get_resources
from utils.filter_utils import filter_resources_by_type
from utils.time_utils import parse_start_end_date_time
from utils.format_utils import create_possible_event
from domain.resource import ResourcesType
from schedule_events.schedule import add_event, auto_schedule_event,  validate_event
from schedule_events.validators import check_work_hours, check_restrictions, check_time_requirements, check_workers_requirements


st.set_page_config(page_title="Agregar evento", page_icon=":hammer_and_wrench:")

st.markdown("# Agregar evento :red_car:")
st.subheader("Detalles del evento")


all_resources = get_resources()


use_auto_scheduler = st.toggle("Usar planificador automático?", value=False)  # Botón para usar el planificador automático

date = None
start_time = None
end_time = None
duration = 0


def error_message(errors):
    """Muestra mensajes de éxito o error según la lista de errores, cada error por separado y todos los errores al mismo tiempo"""
    
    if not errors:
        st.success("Evento guardado con éxito!", icon="✅")
    else:
        for e in errors:
            st.error(e, icon="🚨")


with st.form("add_event_form"):  # Formulario con cada uno de los campos para agregar un evento
    spot = st.selectbox(
        "Lugar del evento:",
        options=filter_resources_by_type(all_resources, ResourcesType.Area_de_trabajo),
        format_func=lambda x: x.name,  # Muestra el nombre del recurso en lugar del objeto completo
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
    for i in filter_resources_by_type(all_resources, ResourcesType.Herramienta):  # Muestra una casilla de verificación para cada herramienta
        if st.checkbox(i.name, key=f"tool_{i.resource_id}"):
            resources.append(i)

    color = st.color_picker("Color del evento:", value="#3498db")  # Selector de color para el evento
    
    
    if not use_auto_scheduler:  # Si no se usa el planificador automático, se muestran los campos para la fecha y hora de inicio y fin, de lo contrario se muestra el campo para la duración
        date = st.date_input("Fecha: ")
        start_time = st.time_input("Hora de inicio: ")
        end_time = st.time_input("Hora de fin: ")
    else:
        duration = st.slider("Duración del evento (minutos):", min_value=20, max_value=480, value=60)

    submitted = st.form_submit_button("Agregar evento")

if submitted:
    
    errors = []

    if use_auto_scheduler:  # Si se usa el planificador automático, se validan los trabajadores y restricciones, y se intenta programar automáticamente el evento
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
        
    else:  # Si no se usa el planificador automático, se validan los datos ingresados y se intenta agregar el evento en el horario seleccionado
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


# Hacer Readme con todo lo q tienen q instalar para correrlo
# comentarios y tipos de datos
# Add 2-3 more workers
# Poner un .py que cuando se ejecute resetee el json y ponga unos datos de prueba en el json con un hora actual
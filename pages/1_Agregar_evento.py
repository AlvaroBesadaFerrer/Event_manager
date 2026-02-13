import streamlit as st
from domain.resources_data import get_resources
from utils.filter_utils import filter_resources_by_type
from domain.resource import ResourcesType
from schedule_events.scheduling_helper import schedule_event_helper


st.set_page_config(page_title="Agregar evento", page_icon=":hammer_and_wrench:")

st.markdown("# Agregar evento :red_car:")

st.markdown("**Modo manual:** Especifica fecha y horario exacto. **Planificador automático:** Solo indica duración y el sistema busca el próximo horario disponible.")

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
    
    errors = schedule_event_helper(
        use_auto_scheduler,
        spot,
        event_type,
        workers,
        resources,
        color,
        date,
        start_time,
        end_time,
        duration,
    )
    
    error_message(errors)


# Hacer Readme con todo lo q tienen q instalar para correrlo y un requirements.txt
# tipos de datos
# Poner un .py que cuando se ejecute resetee el json y ponga unos datos de prueba en el json con un hora actual
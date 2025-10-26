import streamlit as st
from datetime import datetime
from save_load_data import save_data

st.set_page_config(page_title="Agregar evento", page_icon=":hammer_and_wrench:")

SPOTS = [
    "Rampa",
    "Pintura",
    "Normal",
    "Normal 2",
]
EVENTS = [
    "Electricidad",
    "Soldadura",
    "Mecánica",
    "Aspiradora",
    "Pintar",
    "Cambio de aceite",
    "Tramar dirección",
    "Transmisión",
    "Soldar tubo de escape",
]
TRABAJADORES =  [
    "Juan",
    "Pedro",
    "Jose",
]
RESOURCES = [
    "Compresor",
    "Caja de herramientas",
    "Planta de soldar",
    "Guantes",
    "Careta",
]


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

start_date = str(st.date_input("Fecha: ", value= datetime.now()))
start_time = str(st.time_input("Hora de inicio: ", value= datetime.now()))
end_time = str(st.time_input("Hora de fin: ", value= datetime.now()))

button = st.button("Agregar evento", on_click=None)

if button:
    st.success("Evento guardado con éxito!", icon="✅")
    
    data = {}

    data["event_1"] = {
        "spot": spot,
        "event_type": event_type,
        "workers": workers,
        "resources": resources,
        "start_date": start_date,
        "start_time": start_time,
        "end_time": end_time,
    }

    save_data(data)
import streamlit as st
from streamlit_timeline import st_timeline
from utils.time_utils import parse_date, parse_time, parse_start_end_date_time
from utils.color_utils import get_text_color
from json_storage.save_load_data import load_data
from uuid import uuid4


st.set_page_config(page_title="Ver eventos", page_icon=":calendar:")
st.markdown("# Eventos :blue_car:")

events = load_data()
items = []


for event in events:
    try:
        start_datetime, end_datetime = parse_start_end_date_time(event)

        items.append({
            "id": str(uuid4()),
            "content": event.event_type,
            "start": start_datetime.isoformat(),
            "end": end_datetime.isoformat(),
            "style": f"color: {get_text_color(event.color)}; background-color: {event.color}; border-color: {event.color}",
        })
    except (KeyError, ValueError) as e:
        st.warning(f"Error parsing event: {e}")
        continue

if items:
    timeline = st_timeline(items, groups=[], options={}, height="300px")
else:
    st.info("No hay eventos para mostrar. Agrega eventos en la seccion 'Agregar evento'.")

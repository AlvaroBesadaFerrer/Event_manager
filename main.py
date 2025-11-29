import streamlit as st
from streamlit_timeline import st_timeline
from datetime import datetime, timedelta
from uuid import uuid4
from save_load_data import load_data


def parse_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S').time()

def parse_date(time_str):
    return datetime.strptime(time_str, '%Y-%m-%d').date()

st.set_page_config(layout="wide")

st.markdown("# Eventos :blue_car:")

data = load_data()
items = []

min_date = None
max_date = None


for event in data.values():
    try:
        date_event = parse_date(event["start_date"])
        start_datetime = datetime.combine(date_event, parse_time(event["start_time"]))
        end_datetime = datetime.combine(date_event, parse_time(event["end_time"]))
        
        if min_date is None or start_datetime < min_date:
            min_date = start_datetime
        if max_date is None or end_datetime > max_date:
            max_date = end_datetime
        
        event_color = event.get("color", "#3498db")

        items.append({
            "id": str(uuid4()),
            "content": event["event_type"],
            "start": start_datetime.isoformat(),
            "end": end_datetime.isoformat(),
            "style": f"background-color: {event_color}; border-color: {event_color}",
        })
    except (KeyError, ValueError) as e:
        st.warning(f"Error parsing event: {e}")
        continue

if items:
    timeline = st_timeline(items, style = f"background-color: {event_color}; border-color: {event_color}", groups=[], options={}, height="300px")
else:
    st.info("No hay eventos para mostrar. Agrega eventos en la seccion 'Agregar evento'.")

import streamlit as st
from streamlit_timeline import st_timeline
from utils.filter_utils import remove_event_by_id, filter_event_by_id
from utils.time_utils import parse_start_end_date_time
from utils.color_utils import get_text_color
from json_storage.save_load_data import load_data, save_data
from utils.format_utils import show_details


st.markdown("# Eventos :blue_car:")

events = load_data()

items = []

for event in events:
    try:
        start_time = event.start_time
        end_time = event.end_time
        items.append({
            "id": event.id,
            "content": event.event_type.name,
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "selectable": True,
            "style": f"color: {get_text_color(event.color)}; background-color: {event.color}; border-color: {event.color}",
        })
    except (KeyError, ValueError) as e:
        st.warning(f"Error parsing event: {e}")
        continue

if items:
    timeline = st_timeline(items, groups=[], options={}, height="300px")

    if timeline:
        delete_button = st.button(label=f'Eliminar evento {timeline["content"]} seleccionado?')

        st.dataframe(show_details(filter_event_by_id(events, timeline["id"])))

        if delete_button:
            events = remove_event_by_id(events, timeline["id"])
            save_data(events)
            # st.success("Evento eliminado. Los cambios van a ser visibles al refrescar")
            st.rerun()

else:
    st.info("No hay eventos para mostrar. Agrega eventos en la seccion 'Agregar evento'.")


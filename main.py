import streamlit as st
from streamlit_timeline import st_timeline
from utils.filter_utils import remove_event_by_id, filter_event_by_id
from utils.color_utils import get_text_color
from json_storage.save_load_data import load_data, save_data
from utils.format_utils import show_details


st.markdown("# Eventos :blue_car:")
st.markdown("Visualiza todos los eventos programados. Selecciona uno para ver detalles o eliminarlo. También puedes desplazarte en la línea del tiempo")

events = load_data()

items = []

for event in events:  # Recorre cada evento cargado y lo agrega a la lista de items para mostrarlo en la línea de tiempo
    try:
        start_time = event.start_time
        end_time = event.end_time
        items.append({
            "id": event.id,
            "content": event.event_type.name,
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "selectable": True,
            "style": f"color: {get_text_color(event.color)}; background-color: {event.color}; border-color: {event.color}",  # Aquí establecemos el color del texto y el fondo de cada evento en la línea de tiempo
        })
    except (KeyError, ValueError) as e:
        st.warning(f"Error parsing event: {e}")
        continue

if items:  # Si hay eventos para mostrar, renderiza la línea de tiempo
    timeline = st_timeline(items, groups=[], options={}, height="300px")

    if timeline:  # Si se selecciona un evento en la línea de tiempo, muestra sus detalles y la opción de eliminarlo
        delete_button = st.button(label=f'Eliminar evento {timeline["content"]} seleccionado?')

        st.dataframe(show_details(filter_event_by_id(events, timeline["id"])))

        if delete_button:
            events = remove_event_by_id(events, timeline["id"])
            save_data(events)
            # st.success("Evento eliminado. Los cambios van a ser visibles al refrescar")
            st.rerun()

else:
    st.info("No hay eventos para mostrar. Agrega eventos en la seccion 'Agregar evento'.")


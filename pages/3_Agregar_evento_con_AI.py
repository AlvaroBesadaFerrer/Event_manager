import streamlit as st
import json
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from datetime import datetime

from gemini_scheduler.prompt import get_system_instruction
from gemini_scheduler.ai_validators import validate_ai_response
from utils.filter_utils import filter_resource_by_id
from domain.resources_data import get_resources
from utils.time_utils import str_to_datetime
from gemini_scheduler.ai_helpers import ai_json_dumps, explain_error_with_ai, update_session_state
from schedule_events.scheduling_helper import schedule_event_helper

load_dotenv()

if "GEMINI_API_KEY" not in os.environ:
    st.error("GEMINI_API_KEY not found in environment")
    st.stop()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

st.set_page_config(page_title="Agregar evento con IA", page_icon=":robot_face:")
st.title("Agregar evento con IA")

# Inicializar estado de sesión para persistencia de eventos
if 'current_event' not in st.session_state:
    st.session_state['current_event'] = None

if 'previous_response' not in st.session_state:
    st.session_state['previous_response'] = ''

if 'event_json' not in st.session_state:
    st.session_state['event_json'] = '{}'

system_instruction = get_system_instruction()

st.markdown("""
Describe el evento de forma natural y la IA lo procesará. Puedes hacer cambios iterativos:
- "Reparación de motor con Juan mañana a las 10 am por 2 horas en el Espacio con Rampa"
- "Agrega María también"
- "Cambia la hora a las 2 pm"
""")

prompt = st.text_input("¿Qué evento necesitas agendar?")
color_picker = st.color_picker("Elige un color para el evento")


schema_config = {
    "type": "OBJECT",
    "description": "Schema for extracting car-repair shop scheduling event. ONLY extract information explicitly mentioned by the user. Leave fields empty if not mentioned.",
    "properties": {
        "spot": {
            "type": "STRING",
            "description": "Work area ID where the job will be done. Valid values: area_1, area_2, area_3, area_4"
        },
        "event_type": {
            "type": "STRING", 
            "description": "Event type ID. Valid values: event_1 through event_9"
        },
        "workers": {
            "type": "ARRAY",
            "description": "List of worker IDs. Valid values: worker_1 through worker_6",
            "items": {
                "type": "STRING"
            }
        },
        "resources": {
            "type": "ARRAY",
            "description": "List of tool IDs. Valid values: tool_1 through tool_7",
            "items": {
                "type": "STRING"
            }
        },
        "start_time": {
            "type": "STRING",
            "description": "Start timestamp in format YYYY-MM-DD HH:MM:SS or empty string"
        },
        "end_time": {
            "type": "STRING",
            "description": "End timestamp in format YYYY-MM-DD HH:MM:SS or empty string"
        },
        "duration": {
            "type": "STRING",
            "description": "Duration in minutes or empty string"
        },
    },
    "required": []
}


def merge_event_data(new_data, current_data):
    """Fusionar datos nuevos con datos existentes, preservando campos no mencionados en la entrada nueva"""
    if not current_data:
        return new_data
    
    merged = dict(current_data)
    
    # Actualizar campos con nuevos datos
    for key, value in new_data.items():
        # Tratar arrays explícitamente (incluso arrays vacíos deben usarse)
        if isinstance(value, list):
            # Si la IA extrajo explícitamente un array, usarlo (incluso si está vacío)
            merged[key] = value
        elif value and value != "":
            # Para strings y otros valores no vacíos
            merged[key] = value
        elif not value or value == "":
            # Para valores vacíos que no son listas
            if key not in current_data or not current_data[key]:
                merged[key] = value
    
    return merged


def event_successfully_created():
    st.success("✅ **Evento creado exitosamente!**")
    # Limpiar el estado de sesión después de crear el evento
    st.session_state['current_event'] = None
    st.session_state['event_json'] = '{}'
    st.session_state['previous_response'] = ''


def display_event_summary(event_data):
    """Mostrar un resumen formateado del evento"""
    st.info("📋 **Resumen del evento:**")
    
    resources = get_resources()
    
    col1, col2 = st.columns(2)
    
    with col1:
        spot = filter_resource_by_id(resources, event_data.get("spot"))
        st.write(f"**Área:** {spot.name if spot else 'No especificada'}")
        
        event_type = filter_resource_by_id(resources, event_data.get("event_type"))
        st.write(f"**Tipo:** {event_type.name if event_type else 'No especificado'}")
        
        if event_data.get("start_time"):
            st.write(f"**Inicio:** {event_data.get('start_time')}")
        
        if event_data.get("end_time"):
            st.write(f"**Fin:** {event_data.get('end_time')}")
    
    with col2:
        workers_names = []
        for w_id in event_data.get("workers", []):
            worker = filter_resource_by_id(resources, w_id)
            if worker:
                workers_names.append(worker.name)
        st.write(f"**Trabajadores:** {', '.join(workers_names) if workers_names else 'Ninguno'}")
        
        if event_data.get("duration"):
            st.write(f"**Duración:** {event_data.get('duration')} minutos")
        
        if event_data.get("color"):
            st.write(f"**Color:** {event_data.get('color')}")


if st.button("Procesar con IA"):
    if not prompt:
        st.error("Por favor, describe el evento")
    else:
        with st.spinner("Procesando con Gemini..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        response_mime_type="application/json",
                        response_schema=schema_config
                    )
                )
                
                new_event_data = json.loads(response.text)
                new_event_data["color"] = color_picker
                # Fusionar con datos de evento existentes para preservar selecciones anteriores
                if st.session_state['current_event']:
                    current_event = json.loads(st.session_state['event_json'])
                    event_data = merge_event_data(new_event_data, current_event)
                else:
                    event_data = new_event_data
                
                # Validar el evento
                event_data, validation_errors, use_auto_scheduler = validate_ai_response(event_data)
                
                # Actualizar estado de sesión para persistir entre interacciones
                update_session_state(
                    response=response.text,
                    event_json=ai_json_dumps(event_data),
                    current_event=event_data
                )
                
                st.success("✅ Datos procesados exitosamente")
                
                # Mostrar resumen
                display_event_summary(event_data)
                
                # Mostrar JSON completo del evento que se va a tratar de crear
                with st.expander("📋 Ver JSON completo"):
                    st.json(event_data)
                
                if validation_errors:
                    explain_error_with_ai(validation_errors, prompt, event_data, client)
                else:
                    st.success("✅ **Evento validado correctamente**")
                    # Intentar crear el evento
                    st.info("Creando evento en el sistema...")
                    
                    try:                        
                        # Llamar a schedule_event_helper con los parámetros correctos
                        errors = schedule_event_helper(
                            use_auto_scheduler=use_auto_scheduler,
                            spot=event_data.get("spot"),
                            event_type=event_data.get("event_type"),
                            workers=event_data.get("workers", []),
                            resources=event_data.get("resources", []),
                            color=event_data.get("color"),
                            start_time=event_data.get("start_time"),
                            end_time=event_data.get("end_time"),
                            duration=event_data.get("duration"),
                        )
                        
                        if errors:
                            explain_error_with_ai(errors, prompt, event_data, client)
                        else:
                            event_successfully_created()
                    
                    except Exception as e:
                        st.error(f"Error al crear el evento: {str(e)}")
            
            except json.JSONDecodeError as e:
                st.error(f"Error al procesar respuesta de IA: {str(e)}")
            except Exception as e:
                error_str = str(e)
                # Check for 403 Forbidden error (geolocation/VPN issue)
                if "403" in error_str or "Forbidden" in error_str:
                    st.error("❌ **Tienes que usar un VPN**")
                    st.info("La API de Gemini no está disponible en tu región. Usa una VPN.")
                else:
                    st.error(f"Error inesperado: {error_str}")
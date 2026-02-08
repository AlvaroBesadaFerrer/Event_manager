import streamlit as st
import json
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from uuid import uuid4
from datetime import datetime

from schedule_events.scheduling_helper import schedule_event_helper
from gemini_scheduler.prompt import get_system_instruction 
from utils.save_load_utils import to_object
from schedule_events.validators import check_time_requirements, check_work_hours, check_workers_requirements, check_restrictions, check_time_conflicts
from json_storage.save_load_data import load_data
from utils.format_utils import create_possible_event
from domain.resources_data import get_resources
from utils.filter_utils import filter_resource_by_id
from gemini_scheduler.ai_validators import validate_ai_response

load_dotenv()

if "GEMINI_API_KEY" not in os.environ:
    st.error("GEMINI_API_KEY not found in environment")
    st.stop()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

st.set_page_config(page_title="Agregar evento con IA", page_icon=":hammer_and_wrench:")
st.title("Agregar evento con IA")

system_instruction = get_system_instruction()

prompt = st.text_input("Describe el evento (ej: 'Reparación de transmisión con Juan y Maria mañana a las 10 am por 1 hora en el Espacio con Rampa')")


schema_config = {
    "type": "OBJECT",
    "description": "Schema for extracting car-repair shop scheduling event. ONLY extract information explicitly mentioned by the user. Leave fields empty if not mentioned.",
    "properties": {
        "spot": {
            "type": "STRING",
            "description": "Work area ID where the job will be done. ONLY set if user explicitly mentions a specific area/location. Leave empty string if not mentioned. Valid values: area_1, area_2, area_3, area_4"
        },
        "event_type": {
            "type": "STRING", 
            "description": "Event type ID. ONLY set if user explicitly mentions a specific service/repair type. Leave empty string if not mentioned. Valid values: event_1, event_2, event_3, event_4, event_5, event_6, event_7, event_8, event_9"
        },
        "workers": {
            "type": "ARRAY",
            "description": "List of worker names/IDs. ONLY include workers explicitly mentioned by name. Leave empty array if no workers mentioned.",
            "items": {
                "type": "STRING"
            }
        },
        "resources": {
            "type": "ARRAY",
            "description": "List of tools/equipment mentioned. ONLY include resources explicitly mentioned. Leave empty array if no resources mentioned.",
            "items": {
                "type": "STRING"
            }
        },
        "start_time": {
            "type": "STRING",
            "description": "Start timestamp in format YYYY-MM-DD HH:MM:SS. ONLY set if user explicitly mentions a start time. Leave empty string if not mentioned."
        },
        "end_time": {
            "type": "STRING",
            "description": "End timestamp in format YYYY-MM-DD HH:MM:SS. ONLY set if user explicitly mentions an end time. Leave empty string if not mentioned."
        },
        "duration": {
            "type": "STRING",
            "description": "Duration in minutes as string (e.g., '60'). ONLY set if user explicitly mentions duration. Leave empty string if not mentioned."
        },
        "color": {
            "type": "STRING",
            "description": "Color identifier for the event. ONLY set if user explicitly mentions a color. Leave empty string if not mentioned."
        }
    },
    "required": []
}


if st.button("Generar con IA") and prompt:
    with st.spinner("Procesando..."):
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=schema_config
            )
        )
        
        try:
            event_data = json.loads(response.text)
            
            st.success("Datos extraídos por IA:")
            st.json(event_data)

            validation_errors, use_auto_scheduler = validate_ai_response(event_data)

            # Mostrar errores
            if validation_errors:
                pass # Explicar error con IA
            else:
                errors = schedule_event_helper(
                    use_auto_scheduler=use_auto_scheduler,
                    spot=event_data["spot"],
                    event_type=event_data["event_type"],
                    workers=event_data["workers"],
                    resources=event_data["resources"],
                    start_time=event_data["start_time"],
                    end_time=event_data["end_time"],
                    duration=event_data["duration"],
                    color=event_data["color"],
                )
                if errors:
                    st.error("Error al programar el evento:")
                    for error in errors:
                        st.write(f"- {error}")
                else:
                    st.success("Evento programado exitosamente")
        except json.JSONDecodeError:
            st.error("Error al interpretar la respuesta de la IA. Intenta ser más específico.")
            st.write(response.text)


# TODO
# Agregar al req y readme
# python-dotenv
# google-genai
# .env file with GEMINI_API_KEY

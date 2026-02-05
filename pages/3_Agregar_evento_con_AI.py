import streamlit as st
import json
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

from gemini_scheduler.prompt import get_system_instruction 

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
    "description": "Strict schema for extracting a car-repair shop scheduling event. Always include all keys.",
    "properties": {
        "spot": {
            "type": "STRING",
            "description": "Work area ID where the job will be done. Must be one of: area_1, area_2, area_3, area_4.",
            "enum": ["area_1", "area_2", "area_3", "area_4"]
        },
        "event_type": {
            "type": "STRING",
            "description": "Event type ID.",
            "enum": [
                "event_1", "event_2", "event_3", "event_4", "event_5",
                "event_6", "event_7", "event_8", "event_9"
            ]
        },
        "workers": {
            "type": "ARRAY",
            "description": "List of worker IDs assigned to the job.",
            "items": {
                "type": "STRING",
                "enum": [
                    "worker_1", "worker_2", "worker_3",
                    "worker_4", "worker_5", "worker_6"
                ]
            }
        },
        "resources": {
            "type": "ARRAY",
            "description": "List of tool/equipment IDs needed.",
            "items": {
                "type": "STRING",
                "enum": [
                    "tool_1", "tool_2", "tool_3", "tool_4",
                    "tool_5", "tool_6", "tool_7"
                ]
            }
        },
        "start_time": {
            "type": "STRING",
            "description": "Start timestamp in format YYYY-MM-DD HH:MM:SS, or empty string \"\" if not provided."
        },
        "end_time": {
            "type": "STRING",
            "description": "End timestamp in format YYYY-MM-DD HH:MM:SS, or empty string \"\" if not provided."
        },
        "duration": {
            "type": "STRING",
            "description": "Duration in minutes as a string integer (e.g., \"60\"), or empty string \"\" if not provided."
        },
        "color": {
            "type": "STRING",
            "description": "Color identifier for the event (e.g., hex code or color name)."
        }
    },
    "additionalProperties": False
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
            
            st.success("Datos extraídos:")
            st.json(event_data)
            
        except json.JSONDecodeError:
            st.error("Error al interpretar la respuesta de la IA. Intenta ser más específico.")
            st.write(response.text)


# TODOOOOOOOOOO
# Agregar al req y readme
# python-dotenv
# google-genai
# streamlit
# .env file with GEMINI_API_KEY

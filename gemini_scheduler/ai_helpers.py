import streamlit as st
import json

from utils.time_utils import datetime_to_str

def update_session_state(response, event_json, current_event):
    """Persiste datos del evento y respuesta de la IA en el estado de sesión para edición iterativa."""
    st.session_state['current_event'] = current_event
    st.session_state['previous_response'] = response
    st.session_state['event_json'] = event_json

def explain_error_with_ai(validation_errors, prompt, event_data, client):
    """Muestra errores de validación y pide a la IA sugerencias para corregirlos."""
    st.warning("⚠️ **Problemas encontrados:**")

    for error in validation_errors:
        st.write(f"• {error}")
    
    # Pedir a la IA que explique y sugiera correcciones
    st.info("Pidiendo ayuda a la IA para corregir los errores...")
    
    explanation_prompt = (
        "Eres un asistente que ayuda a corregir errores en la creación de eventos para un taller de autos. "
        "Responde en español, de forma clara y breve. "
        "Explica: 1) Qué está mal o qué falta, 2) Cómo corregirlo, 3) Un ejemplo con valores válidos.\n\n"
        f"Entrada del usuario: {prompt}\n\n"
        f"JSON del evento: {json.dumps(event_data, ensure_ascii=False, indent=2)}\n\n"
        f"Errores: {', '.join(validation_errors)}"
    )
    
    ai_explanation = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=explanation_prompt
    )
    st.markdown(ai_explanation.text)
    

def ai_json_dumps(event_data):
    """Convierte datos del evento a JSON con campos datetime formateados."""
    e = event_data
    if e["start_time"]:
        e["start_time"] = datetime_to_str(e["start_time"])
    if e["end_time"]:
        e["end_time"] = datetime_to_str(e["end_time"])
    return json.dumps(e, ensure_ascii=False)
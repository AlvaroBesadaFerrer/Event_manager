import streamlit as st
from datetime import datetime
from datetime import timedelta


# Validar y procesar los datos
def validate_ai_response(event_data):
    validation_errors = []
    
    # Convertir strings vacíos a None
    for key in ["spot", "event_type", "start_time", "end_time", "duration", "color"]:
        if key in event_data and event_data[key] == "":
            event_data[key] = None
    
    # Validar duración
    duration = event_data.get("duration")
    if duration is not None:
        if isinstance(duration, str):
            try:
                duration = int(duration)
                event_data["duration"] = duration
            except (ValueError, TypeError):
                validation_errors.append("La **duración** debe ser un número válido en minutos.")
                duration = None
        
        if duration is not None and isinstance(duration, int) and duration <= 0:
            validation_errors.append("La **duración** debe ser mayor a 0 minutos.")
    
    # Validar que tenemos los campos requeridos
    if not event_data.get("spot"):
        validation_errors.append("Debe especificar un área de trabajo (ej: 'Espacio con Rampa', 'Espacio para pintura').")
    
    if not event_data.get("event_type"):
        validation_errors.append("Debe especificar un tipo de evento/servicio (ej: 'Reparación eléctrica', 'Pintura exterior').")
    
    if not event_data.get("workers"):
        validation_errors.append("Debe especificar al menos un trabajador.")
    
    if not event_data.get("color"):
        validation_errors.append("Debe especificar un color para el evento.")
    
    # Validar tiempos
    start_time_str = event_data.get("start_time")
    end_time_str = event_data.get("end_time")
    
    if start_time_str:
        try:
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            validation_errors.append(f"La **hora de inicio** '{start_time_str}' no está en formato válido (YYYY-MM-DD HH:MM:SS).")
            start_time = None
    else:
        start_time = None
    
    if end_time_str:
        try:
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            validation_errors.append(f"La **hora de fin** '{end_time_str}' no está en formato válido (YYYY-MM-DD HH:MM:SS).")
            end_time = None
    else:
        end_time = None
    
    # Validar que start_time y end_time sean coherentes con duration
    if start_time and end_time and duration and isinstance(duration, int):
        time_diff = (end_time - start_time).total_seconds() / 60
        if time_diff != duration:
            validation_errors.append(f"La **duración** ({duration} min) no coincide con la diferencia entre hora de inicio y fin ({int(time_diff)} min). Usa la duración para calcular la hora de fin.")
    
    # Validar que si solo tenemos start_time y duration, calcular end_time
    if start_time and duration and not end_time:
        end_time = start_time + timedelta(minutes=duration)
        event_data["end_time"] = end_time.strftime("%Y-%m-%d %H:%M:%S")
        st.info(f"Se calculará la hora de fin como: {start_time} + {duration} minutos")
    
    # Validar que si solo tenemos end_time y duration, calcular start_time
    if end_time and duration and not start_time:
        start_time = end_time - timedelta(minutes=duration)
        event_data["start_time"] = start_time.strftime("%Y-%m-%d %H:%M:%S")
        st.info(f"Se calculará la hora de inicio restando {duration} minutos de la hora de fin")
    
    # Si no hay hora de inicio ni fin, ni duration
    if not start_time and not end_time and not duration:
        validation_errors.append("Debes especificar una hora de inicio, una hora de fin, o una duración del evento.")
    
    auto_schedule = not start_time and not end_time and duration
    
    return event_data, validation_errors, auto_schedule
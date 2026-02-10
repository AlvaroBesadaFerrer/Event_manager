import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from utils.time_utils import str_to_datetime


# Validar y procesar los datos
def validate_ai_response(event_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str], bool]:
    """Valida completamente la respuesta de IA y calcula tiempos faltantes"""
    validation_errors: List[str] = []
    auto_schedule = False
    print("dekkkkkkkkkkkk")
    # Paso 1: Convertir strings vacíos a None
    empty_string_to_None(event_data)
    
    # Paso 2: Extraer y validar tiempos
    start_time, end_time, duration = extract_and_validate_times(event_data, validation_errors)
    
    # Paso 3: Validar duración
    validation_errors.extend(validate_duration(duration))
    
    # Paso 4: Validar campos requeridos
    validation_errors.extend(validate_required_fields(event_data))
    
    # Paso 5: Validar consistencia entre tiempos
    validation_errors.extend(validate_time_with_duration(start_time, end_time, duration))
    
    # Paso 6: Calcular tiempos faltantes
    start_time, end_time, duration = calculate_missing_times(
        start_time, end_time, duration
    )
    
    # Paso 7: Validar que hay información mínima de tiempo
    validation_errors.extend(validate_empty_time_and_duration(start_time, end_time, duration))
    
    # Paso 8: Actualizar event_data con tiempos calculados
    if start_time:
        event_data["start_time"] = start_time
    else:
        event_data["start_time"] = None
        
    if end_time:
        event_data["end_time"] = end_time
    else:
        event_data["end_time"] = None
        
    if duration:
        event_data["duration"] = duration
    else:
        event_data["duration"] = 0
    
    # Paso 9: Determinar si puede auto-agendar (solo si no hay errores)
    auto_schedule = check_auto_schedule(validation_errors)
    
    return event_data, validation_errors, auto_schedule


def empty_string_to_None(event_data: Dict[str, Any]) -> None:
    """Convertir strings vacíos a None"""
    for key in ["spot", "event_type", "start_time", "end_time", "duration", "color"]:
        if key in event_data and event_data[key] == "":
            event_data[key] = None


def extract_and_validate_times(
    event_data: Dict[str, Any],
    validation_errors: List[str]
) -> Tuple[Optional[datetime], Optional[datetime], Optional[int]]:
    """Extrae y valida los tiempos del evento_data."""
    start_time = None
    end_time = None
    duration = None
    
    start_time_str = event_data.get("start_time")
    end_time_str = event_data.get("end_time")
    duration_str = event_data.get("duration")
    
    # Validar start_time
    if start_time_str:
        try:
            start_time = str_to_datetime(start_time_str)
        except (ValueError, TypeError):
            validation_errors.append(
                f"La **hora de inicio** '{start_time_str}' no está en formato válido (YYYY-MM-DD HH:MM:SS)."
            )
            start_time = None
    
    # Validar end_time
    if end_time_str:
        try:
            end_time = str_to_datetime(end_time_str)
        except (ValueError, TypeError):
            validation_errors.append(
                f"La **hora de fin** '{end_time_str}' no está en formato válido (YYYY-MM-DD HH:MM:SS)."
            )
            end_time = None
    
    # Validar duration (será validado más adelante por validate_duration)
    if duration_str is not None and duration_str != "":
        try:
            duration = int(duration_str)
        except (ValueError, TypeError):
            # Los errores de conversión se capturan en validate_duration
            duration = None
    
    return start_time, end_time, duration


def validate_duration(duration: Optional[int]) -> List[str]:
    """Valida que la duración sea válida."""

    validation_errors: List[str] = []
    if duration is None:
        # La duración es opcional en esta etapa
        return validation_errors
    
    if not isinstance(duration, int):
        validation_errors.append("La **duración** debe ser un número válido en minutos.")
        return validation_errors
    
    if duration <= 0:
        validation_errors.append("La **duración** debe ser mayor a 0 minutos.")
    
    return validation_errors


def validate_required_fields(event_data: Dict[str, Any]) -> List[str]:
    """Valida que los campos requeridos estén presentes."""
    validation_errors: List[str] = []
    
    if not event_data.get("spot"):
        validation_errors.append(
            "Debe especificar un área de trabajo (ej: 'Espacio con Rampa', 'Espacio para pintura')."
        )
    
    if not event_data.get("event_type"):
        validation_errors.append(
            "Debe especificar un tipo de evento/servicio (ej: 'Reparación eléctrica', 'Pintura exterior')."
        )
    
    if not event_data.get("workers"):
        validation_errors.append("Debe especificar al menos un trabajador.")
    
    if not event_data.get("color"):
        validation_errors.append("Debe especificar un color para el evento.")
    
    return validation_errors


def validate_time_with_duration(
    start_time: Optional[datetime],
    end_time: Optional[datetime],
    duration: Optional[int]
) -> List[str]:
    """Valida que start_time, end_time y duration sean coherentes."""
    validation_errors: List[str] = []
    
    # Solo validar si tenemos todos los tres valores
    if start_time and end_time and duration and isinstance(duration, int):
        time_diff = int((end_time - start_time).total_seconds() / 60)
        if time_diff != duration:
            validation_errors.append(
                f"La **duración** ({duration} min) no coincide con la diferencia entre "
                f"hora de inicio y fin ({time_diff} min). Usa la duración para calcular la hora de fin."
            )
    
    return validation_errors


def calculate_missing_times(
    start_time: Optional[datetime],
    end_time: Optional[datetime],
    duration: Optional[int]
) -> Tuple[Optional[datetime], Optional[datetime], Optional[int]]:
    """
    Calcula tiempos faltantes basado en los tiempos disponibles.
    
    Estrategia:
    - Si tenemos start_time + duration: calcular end_time
    - Si tenemos end_time + duration: calcular start_time
    - Si tenemos start_time + end_time: calcular duration
    """
    # Si falta end_time pero tenemos start_time y duration
    if start_time and duration and not end_time:
        end_time = start_time + timedelta(minutes=duration)
        st.info(f"✓ Se calculó la hora de fin: {start_time.strftime('%H:%M')} + {duration} min = {end_time.strftime('%H:%M')}")
    
    # Si falta start_time pero tenemos end_time y duration
    if end_time and duration and not start_time:
        start_time = end_time - timedelta(minutes=duration)
        st.info(f"✓ Se calculó la hora de inicio: {end_time.strftime('%H:%M')} - {duration} min = {start_time.strftime('%H:%M')}")
    
    # Si falta duration pero tenemos start_time y end_time
    if start_time and end_time and not duration:
        duration = int((end_time - start_time).total_seconds() / 60)
        if duration > 0:
            st.info(f"✓ Se calculó la duración: {end_time.strftime('%H:%M')} - {start_time.strftime('%H:%M')} = {duration} minutos")
        else:
            duration = None
    
    return start_time, end_time, duration


def validate_empty_time_and_duration(
    start_time: Optional[datetime],
    end_time: Optional[datetime],
    duration: Optional[int]
) -> List[str]:
    """Valida que hay información mínima de tiempo."""
    validation_errors: List[str] = []
    
    # Contar cuántos campos de tiempo tenemos
    time_fields_count = sum([start_time is not None, end_time is not None, duration is not None])
    
    if time_fields_count == 0 or ((start_time and not end_time) or (not start_time and end_time)):
        validation_errors.append(
            "Debes especificar una hora de inicio, una hora de fin, o una duración del evento."
        )
        
    return validation_errors


def check_auto_schedule(validation_errors: List[str]) -> bool:
    """Determina si el evento puede auto-agendarse."""

    return len(validation_errors) == 0

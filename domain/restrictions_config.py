# Lista de restricciones para cada recurso o evento en el dominio
# Cada evento tiene una lista de recursos requeridos y una lista de recursos prohibidos
"""
Todas las restricciones posibles se pueden configurar entre áreas de trabajo, trabajadores, tipos de evento y herramientas
en este diccionario. Cada clave es el ID de un recurso (trabajadores, áreas de trabajo, herramientas, tipos de evento),
y su valor es otro diccionario con dos listas:
- "required": lista de IDs de recursos que deben estar presentes si el recurso clave está presente.
- "forbidden": lista de IDs de recursos que no deben estar presentes si el recurso clave está presente.
Estas restricciones se utilizan para generar las instancias de las clases de restricción en `restrictions_data.py`.
"""

RESTRICTIONS_CONFIG = {

    "event_1": {
        "required": ["worker_1"],
        "forbidden": ["area_2"],
    },
    "event_2": {
        "required": ["worker_3", "tool_6", "tool_3", "tool_5"],
        "forbidden": ["area_2"],
    },
    "event_3": {
        "required": ["worker_2", "tool_2"],
        "forbidden": ["area_1", "area_2"],
    },
    "event_4": {
        "required": ["tool_1"],
        "forbidden": ["area_1", "area_2"],
    },
    "event_5": {
        "required": ["area_2", "tool_1", "tool_7"],
        "forbidden": ["worker_2"],
    },
    "event_6": {
        "required": ["tool_4"],
        "forbidden": ["area_2"],
    },
    "event_7": {
        "required": ["area_1", "tool_2", "tool_4"],
        "forbidden": ["worker_1"],
    },
    "event_8": {
        "required": ["area_1", "tool_2"],
        "forbidden": [],
    },
    "event_9": {
        "required": ["area_1", "worker_3", "tool_3", "tool_6", "tool_5"],
        "forbidden": [],
    },
    "worker_4": {
        "required": ["tool_5"],
        "forbidden": ["event_3", "event_5"],
    },
    "worker_5": {
        "required": [],
        "forbidden": ["worker_1", "event_7", "tool_1"],
    },
}

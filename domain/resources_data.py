from .resource import Resource, ResourcesType


RESOURCES = [
    Resource("tool_1", "Compresor", ResourcesType.Herramienta),
    Resource("tool_2", "Caja de herramientas", ResourcesType.Herramienta),
    Resource("tool_3", "Planta de soldar", ResourcesType.Herramienta),
    Resource("tool_4", "Gato hidráulico", ResourcesType.Herramienta),
    Resource("tool_5", "Guantes", ResourcesType.Herramienta),
    Resource("tool_6", "Careta", ResourcesType.Herramienta),
    Resource("tool_7", "Lentes de seguridad", ResourcesType.Herramienta),
    Resource("area_1", "Espacio con rampa", ResourcesType.Area_de_trabajo),
    Resource("area_2", "Espacio de pintura", ResourcesType.Area_de_trabajo),
    Resource("area_3", "Espacio normal", ResourcesType.Area_de_trabajo),
    Resource("area_4", "Espacio normal 2", ResourcesType.Area_de_trabajo),
    Resource("event_1", "Electricidad", ResourcesType.Tipo_de_evento),
    Resource("event_2", "Soldadura", ResourcesType.Tipo_de_evento),
    Resource("event_3", "Mecánica", ResourcesType.Tipo_de_evento),
    Resource("event_4", "Aspiradora", ResourcesType.Tipo_de_evento),
    Resource("event_5", "Pintar", ResourcesType.Tipo_de_evento),
    Resource("event_6", "Cambio de aceite", ResourcesType.Tipo_de_evento),
    Resource("event_7", "Tramar dirección", ResourcesType.Tipo_de_evento),
    Resource("event_8", "Transmisión", ResourcesType.Tipo_de_evento),
    Resource("event_9", "Soldar tubo de escape", ResourcesType.Tipo_de_evento),
    Resource("worker_1", "Juan", ResourcesType.Trabajador),
    Resource("worker_2", "Pedro", ResourcesType.Trabajador),
    Resource("worker_3", "Jose", ResourcesType.Trabajador),
]


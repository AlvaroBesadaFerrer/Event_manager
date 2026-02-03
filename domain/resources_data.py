from .resource import Resource, ResourcesType

# Lista de objetos todos los objetos Resource de este dominio
RESOURCES = [
    Resource("tool_1", "Compresor", ResourcesType.Herramienta),
    Resource("tool_2", "Caja de herramientas", ResourcesType.Herramienta),
    Resource("tool_3", "Planta de soldar", ResourcesType.Herramienta),
    Resource("tool_4", "Gato hidráulico", ResourcesType.Herramienta),
    Resource("tool_5", "Guantes de trabajo", ResourcesType.Herramienta),
    Resource("tool_6", "Careta para soldar", ResourcesType.Herramienta),
    Resource("tool_7", "Lentes de seguridad", ResourcesType.Herramienta),
    Resource("area_1", "Espacio con rampa", ResourcesType.Area_de_trabajo),
    Resource("area_2", "Espacio para pintura", ResourcesType.Area_de_trabajo),
    Resource("area_3", "Espacio de trabajo 1", ResourcesType.Area_de_trabajo),
    Resource("area_4", "Espacio de trabajo 2", ResourcesType.Area_de_trabajo),
    Resource("event_1", "Reparaciones eléctricas", ResourcesType.Tipo_de_evento),
    Resource("event_2", "Soldadura en la carrocería", ResourcesType.Tipo_de_evento),
    Resource("event_3", "Arreglo de Mecánica", ResourcesType.Tipo_de_evento),
    Resource("event_4", "Aspirar interior del auto", ResourcesType.Tipo_de_evento),
    Resource("event_5", "Pintar exterior del auto", ResourcesType.Tipo_de_evento),
    Resource("event_6", "Cambio de aceite del motor", ResourcesType.Tipo_de_evento),
    Resource("event_7", "Arreglar dirección", ResourcesType.Tipo_de_evento),
    Resource("event_8", "Revisar transmisión", ResourcesType.Tipo_de_evento),
    Resource("event_9", "Soldadura en el tubo de escape", ResourcesType.Tipo_de_evento),
    Resource("worker_1", "Juan", ResourcesType.Trabajador),
    Resource("worker_2", "Pedro", ResourcesType.Trabajador),
    Resource("worker_3", "José", ResourcesType.Trabajador),
    Resource("worker_4", "Luisa", ResourcesType.Trabajador),
    Resource("worker_5", "Sofía", ResourcesType.Trabajador),
    Resource("worker_6", "Frank", ResourcesType.Trabajador),
]


def get_resources():
    """Retorna una copia (para evitar sobreescribirla por error) de la lista de recursos"""
    return list(RESOURCES)


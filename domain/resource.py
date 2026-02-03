from enum import Enum


class ResourcesType(Enum):
    # Tipos de recursos disponibles en el dominio. Es una clase enumerada para que sea más fácil de manejar
    Herramienta = "Herramienta"
    Area_de_trabajo = "Area_de_trabajo"
    Tipo_de_evento = "Tipo de evento"
    Trabajador = "Trabajador"


class Resource():
    """Clase que representa un recurso en el sistema de gestión de eventos"""

    def __init__(self, resource_id: str, name: str, resource_type: ResourcesType):

        self.resource_id = resource_id
        self.name = name

        if not isinstance(resource_type, ResourcesType):
            raise TypeError("resource_type must be an instance of ResourcesType")
        self.resource_type = resource_type
    
    # Métodos para comparar recursos y representarlos como cadenas
    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.resource_id == other.resource_id
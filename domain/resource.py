from enum import Enum


class ResourcesType(Enum):
    Herramienta = "Herramienta"
    Area_de_trabajo = "Area_de_trabajo"
    Tipo_de_evento = "Tipo de evento"
    Trabajador = "Trabajador"


class Resource():

    def __init__(self, resource_id: str, name: str, resource_type: ResourcesType):

        self.resource_id = resource_id
        self.name = name

        if not isinstance(resource_type, ResourcesType):
            raise TypeError("resource_type must be an instance of ResourcesType")
        self.resource_type = resource_type
    
    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.resource_id == other.resource_id
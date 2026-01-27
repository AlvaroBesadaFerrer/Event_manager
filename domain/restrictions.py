from domain.resource import Resource

class Restriction():
    def __init__(self, resource_a: Resource, resource_b: Resource):
        self.resource_a = resource_a
        self.resource_b = resource_b

    def is_satisfied(self, event) -> str|None:
        raise NotImplementedError()


class MutualExclusion(Restriction):
    def is_satisfied(self, event) -> str|None:
        resources = [
            event.spot,
            event.event_type,
            *event.workers,
            *event.resources
        ]

        if (self.resource_a in resources and self.resource_b in resources):
            return f'{self.resource_a} no pueden estar a la vez en un evento con {self.resource_b}'

class CoRequisite(Restriction):
    def is_satisfied(self, event) -> str|None:

        resources = [
            event.spot,
            event.event_type,
            *event.workers,
            *event.resources
        ]

        if self.resource_a in resources and  not (self.resource_b in resources):
            return f'{self.resource_a} necesita estar con {self.resource_b} en el evento'
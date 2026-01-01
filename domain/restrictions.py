from domain.resource import Resource

class Restriction():
    def __init__(self, resource_a: Resource, resource_b: Resource):
        self.resource_a = resource_a
        self.resource_b = resource_b

    def is_satisfied(self, event) -> bool:
        raise NotImplementedError()


class MutualExclusion(Restriction):
    def is_satisfied(self, event) -> bool:
        resources = [event.spot] + [event.event_type] + event.workers + event.resources
        print(resources)
        print(self.resource_a, self.resource_b)
        return not (self.resource_a in resources and self.resource_b in resources)

class CoRequisite(Restriction):
    def is_satisfied(self, event) -> bool:
        resources = [event.spot] + [event.event_type] + event.workers + event.resources
        print(resources)
        print(self.resource_a, self.resource_b)
        return self.resource_a in resources and self.resource_b in resources
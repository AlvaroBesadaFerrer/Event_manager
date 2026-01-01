from uuid import uuid4

class Event():
    def __init__(self, id, spot, event_type, workers, resources, date, end_time, start_time, color):
        self.id = id
        self.spot = spot
        self.event_type = event_type
        self.workers = workers
        self.resources = resources
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.color = color

    def intersection(self, other_event):
        return self.start_time >= other_event.start_time and self.start_time < other_event.end_time

    def check_resources_availability(self, other_event):

        if self.spot == other_event.spot:
            return False
        
        for w in self.workers:
            if w in other_event.workers:
                return False
        
        for r in self.resources:
            if r in other_event.resources:
                return False

        return True
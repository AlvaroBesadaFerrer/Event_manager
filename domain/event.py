from uuid import uuid4

class Event():
    def __init__(self, spot, event_type, workers, resources, date, end_time, start_time, color):
        self.id = str(uuid4())
        self.spot = spot
        self.event_type = event_type
        self.workers = workers
        self.resources = resources
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.color = color


class Event():
    def __init__(
            self, 
            id, 
            spot, 
            event_type,
            workers,
            resources,
            end_datetime,
            start_datetime,
            color
        ):
        self.id = id
        self.spot = spot
        self.event_type = event_type
        self.workers = workers
        self.resources = resources
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.color = color

    def intersection(self, other_event):
        if self.start_datetime is None or self.end_datetime is None or other_event.start_datetime is None or other_event.end_datetime is None:
            return False
        
        same_date = self.start_datetime.date() == other_event.start_datetime.date()
        overlaps = self.start_datetime < other_event.end_datetime and self.end_datetime > other_event.start_datetime
        return same_date and overlaps

    def check_resources_availability(self, other_event):
        problems = []
        if self.spot == other_event.spot:
            problems.append(f'Un evento de **{other_event.event_type}** esta usando el mismo espacio **{self.spot.name}** a esa hora')
        
        for w in self.workers:
            if w in other_event.workers:
                problems.append(f'**{w.name}** ya estara trabajando en evento de **{other_event.event_type}** a esa hora')
        
        for r in self.resources:
            if r in other_event.resources:
                problems.append(f'**{r.name}** ya se estara usando en evento de **{other_event.event_type}** a esa hora')
        
        return problems
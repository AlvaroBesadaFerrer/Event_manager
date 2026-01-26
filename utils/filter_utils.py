def filter_resources_by_type(resources, resource_type):
    return [r for r in resources if r.resource_type == resource_type]

def filter_resource_by_id(resources, resource_id):
    for r in resources:
        if r.resource_id == resource_id:
            return r
    return None

def filter_resources_list_by_id(resources, resources_id):
    
    result = []
    for id in resources_id:
        r = filter_resource_by_id(resources, id)
        if r is not None:
            result.append(r)
    return result

def filter_event_by_id(events, event_id):
    for e in events:
        if e.id == event_id:
            return e
    return None

def remove_event_by_id(events, event_id):
    for e in events:
        if e.id == event_id:
            events.remove(e)
    return events
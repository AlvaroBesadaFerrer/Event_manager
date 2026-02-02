def filter_resources_by_type(resources, resource_type):
    """Filtra una lista de recursos por tipo de recurso y devuelve una lista de recursos que coinciden con ese tipo de recurso"""
    return [r for r in resources if r.resource_type == resource_type]

def filter_resource_by_id(resources, resource_id):
    """Filtra una lista de recursos por ID y devuelve el recurso que coincide con el ID dado"""
    for r in resources:
        if r.resource_id == resource_id:
            return r
    return None

def filter_resources_list_by_id(resources, resources_id):
    """Filtra una lista de recursos por una lista de IDs y devuelve una lista de recursos que coinciden con los IDs dados"""
    result = []
    for id in resources_id:
        r = filter_resource_by_id(resources, id)
        if r is not None:
            result.append(r)
    return result

def filter_event_by_id(events, event_id):
    """Filtra una lista de eventos por ID y devuelve el evento que coincide con el ID dado"""
    for e in events:
        if e.id == event_id:
            return e
    return None

def remove_event_by_id(events, event_id):
    """Elimina un evento de una lista de eventos por ID y devuelve la lista de eventos sin el evento que se quería eliminar"""
    return [e for e in events if e.id != event_id]
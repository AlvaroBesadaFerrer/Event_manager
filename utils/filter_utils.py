def filter_resources_by_type(resources, resource_type):
    return [r for r in resources if r.resource_type == resource_type]

def filter_resources_by_id(resources, resource_id):
    return [r for r in resources if r.resource_id == resource_id]
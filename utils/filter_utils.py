def filter_resources_by_type(resources, resource_type):
    return [r.name for r in resources if r.resource_type == resource_type]

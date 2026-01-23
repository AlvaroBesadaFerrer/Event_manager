from domain.restrictions import MutualExclusion, CoRequisite
from utils.filter_utils import filter_resource_by_id
from .resources_data import get_resources
from .restrictions_config import RESTRICTIONS_CONFIG as config


def generate_restrictions():
    resources = get_resources()
    restrictions = []

    for object_id, rules in config.items():
        object = filter_resource_by_id(resources, object_id)

        for required_id in rules.get("required", []):
            restrictions.append(
                CoRequisite(
                    object, # type: ignore
                    filter_resource_by_id(resources, required_id), # type: ignore
                )
            )

        for forbidden_id in rules.get("forbidden", []):
            restrictions.append(
                MutualExclusion(
                    object, # type: ignore
                    filter_resource_by_id(resources, forbidden_id), # type: ignore
                )
            )

    return restrictions

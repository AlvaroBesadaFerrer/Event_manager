from domain.restrictions import MutualExclusion, CoRequisite
from utils.filter_utils import filter_resource_by_id
from .resources_data import get_resources


restrictions_data = [
    MutualExclusion(
        filter_resource_by_id(
            get_resources(),
            "event_1"
        ),
        filter_resource_by_id(
            get_resources(),
            "worker_2"
        )
    ),
    CoRequisite(
        filter_resource_by_id(
            get_resources(),
            "event_2"
        ),
        filter_resource_by_id(
            get_resources(),
            "tool_3"
        )
    ),
]
from domain.restrictions import MutualExclusion, CoRequisite
from utils.filter_utils import filter_resources_by_id
from .resources_data import RESOURCES


restrictions_data = [
    MutualExclusion(
        filter_resources_by_id(
            RESOURCES,
            "event_1"
        )[0],
        filter_resources_by_id(
            RESOURCES,
            "worker_2"
        )[0]
    ),
    CoRequisite(
        filter_resources_by_id(
            RESOURCES,
            "event_2"
        )[0],
        filter_resources_by_id(
            RESOURCES,
            "tool_3"
        )[0]
    ),
]
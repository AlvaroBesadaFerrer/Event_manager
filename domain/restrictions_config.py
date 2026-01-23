RESTRICTIONS_CONFIG = {

    "event_1": {
        "required": ["worker_1"],
        "forbidden": ["area_2"],
    },
    "event_2": {
        "required": ["worker_3", "tool_6", "tool_3", "tool_5"],
        "forbidden": ["area_2"],
    },
    "event_3": {
        "required": ["worker_2", "tool_2"],
        "forbidden": ["area_1", "area_2"],
    },
    "event_4": {
        "required": ["tool_1"],
        "forbidden": ["area_1", "area_2"],
    },
    "event_5": {
        "required": ["area_2", "tool_1", "tool_7"],
        "forbidden": ["worker_2"],
    },
    "event_6": {
        "required": ["tool_4"],
        "forbidden": ["area_2"],
    },
    "event_7": {
        "required": ["area_1", "tool_2", "tool_4"],
        "forbidden": ["worker_1"],
    },
    "event_8": {
        "required": ["area_1", "tool_2"],
        "forbidden": [],
    },
    "event_9": {
        "required": ["area_1", "worker_3", "tool_3", "tool_6", "tool_5"],
        "forbidden": [],
    },
}

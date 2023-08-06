import copy
import dataclasses
from inspect import getsource
from typing import Callable


def general_to_dict(data):
    if hasattr(data, 'to_dict'):
        return general_to_dict(getattr(data, 'to_dict')())
    elif dataclasses.is_dataclass(data):
        return dataclasses.asdict(data, dict_factory=explainaboard_dict_factory)
    elif isinstance(data, dict):
        return {k: general_to_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [general_to_dict(v) for v in data]
    # sanitize functions
    elif isinstance(data, Callable):
        return getsource(data)
    else:
        return copy.deepcopy(data)


def explainaboard_dict_factory(data):
    """
    This can be used to serialize data through the following command:
    serialized_data = dataclasses.asdict(data, dict_factory=explainaboard_dict_factory)
    """
    return {field: general_to_dict(value) for field, value in data}

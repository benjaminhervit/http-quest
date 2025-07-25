from enum import Enum
from typing import Type

@staticmethod
def get_enum_values_as_list(enum: Type[Enum]):
    return [e.value for e in enum]
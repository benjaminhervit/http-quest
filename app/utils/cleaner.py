from enum import Enum
from typing import Type


def get_enum_values_as_list(enum: Type[Enum]):
    return [e.value for e in enum]


def get_clean_list_from_string(string: str, separator: str):
    #converts string to list without empty values based on separator
    return [s.strip() for s in string.split(separator) if s.strip()]
from collections import namedtuple
from enum import Enum


class ChoicesEnum(Enum):
    """Adds utility function to enum for easy use in MultipleChoice field
    """
    @classmethod
    def as_choices(cls):
        return [(item.name, item.value) for item in cls]


class PricePair(namedtuple('PricePair', ['method', 'price'])):
    """Ties payment method and associated price together
    """

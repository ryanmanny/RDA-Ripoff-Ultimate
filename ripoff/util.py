from enum import Enum


# Adds utility function to enum for easy use in MultipleChoice model
class ChoicesEnum(Enum):
    @classmethod
    def as_choices(cls):
        return [(item.name, item.value) for item in cls]

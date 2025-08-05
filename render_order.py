from enum import auto, Enum


# an enum is a set of named values that won't change, so it's great for stuff like this
# auto() assigns incrementing integer values automatically
class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()

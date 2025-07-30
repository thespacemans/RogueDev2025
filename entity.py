from typing import Tuple


class Entity:
    """Generic object class to represent players, enemies, items, etc."""

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        # notice how the types are hinted next to each argument
        # create attributes as named by the dot operator
        self.x = x
        self.y = y
        self.char = char  # character we use to represent the entity
        self.color = color  # color of the entity, as an RGB tuple

    def move(self, dx: int, dy: int) -> None:
        """Move the entity by a given amount in the x and y directions"""
        self.x += dx
        self.y += dy

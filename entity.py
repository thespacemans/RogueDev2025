"""Module for defining game entities."""

from __future__ import annotations

import copy
from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """Generic object class to represent players, enemies, items, etc."""

    # note how types are hinted next to each argument
    # if no value is provided when calling the function, it defaults to
    # the provided value (of format : `int = 0,` for example)
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
    ):
        # these arguments are pretty straightforward
        # coordinates, the string used to represent the entity, its color, its name,
        # and whether it blocks movement
        # in future, enemies will block movements, while things like consumables/equipment
        # will be traversable by the player

        # assign attributes provided by init to self
        self.x = x
        self.y = y
        self.char = char  # character we use to represent the entity
        self.color = color  # color of the entity, as an RGB tuple
        self.name = name  # name of the entity
        self.blocks_movement = blocks_movement  # whether the entity blocks movement

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""

        # takes a GameMap instance, along with x and y for locations
        # then creates a clone of the instance of Entity, whatever that instance is
        # then assigns the x and y variables to it, and adds the entity to the gamemap's set
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        gamemap.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        """Move the entity by a given amount in the x and y directions"""
        self.x += dx
        self.y += dy

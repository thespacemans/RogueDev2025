"""Module for defining game entities."""

from __future__ import annotations

import copy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """Generic object class to represent players, enemies, items, etc."""

    # define a gamemap attribute and hint to its type GameMap
    gamemap: GameMap

    # note how types are hinted next to each argument
    # if no value is provided when calling the function, it defaults to the provided value
    # (of format "x: int = 0," for example)
    def __init__(
        self,
        gamemap: Optional[GameMap] = None,
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
        # "if gamemap" checks if gamemap exists
        if gamemap:
            # if the gamemap hasn't been provided yet, it will be set later
            # if it HAS been provided, then assign it to self and add this entity to that map
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""

        # takes a GameMap instance, along with x and y for locations
        # then creates a clone of the instance of Entity, whatever that instance is
        # then assigns the x and y variables and the gamemap, and adds the entity to the gamemap's set
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Places this `entity` at a new location.  Also handles moving between `GameMaps`."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(
                self, "gamemap"
            ):  # gamemap may be Not Initialized. if it is, execute:
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)
            # if the entity has a gamemap already, remove the entity from that map and place it
            # in the one provided by the place(args)

    def move(self, dx: int, dy: int) -> None:
        """Move the entity by a given amount in the x and y directions"""
        self.x += dx
        self.y += dy

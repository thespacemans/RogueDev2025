"""Module that defines class GameMap."""

from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity


class GameMap:
    """Class that defines the game map, which is a 2D array of tiles of specified types"""

    # accepts width, height, and the array of game entities
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
        # this line creates a 2D array filled with the same values, in this case the Wall tile
        # this fills self.tiles with wall tiles
        # now we can utilize a procedural generator to populate this wall array with walkable rooms
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # array containing the tiles the player can currently see
        # fill them with value "false" for now
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # array containing the tiles the player has seen before

    # this method will check if given x and y coordinates are within the bounds of the map
    # ensures the player doesn't wander off into the void
    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of
        this map's specified width and height"""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """Renders the map, using Console class's .rgb method"""

        # if a tile is in the "visible" array, draw it with "light" colors
        # if it isnt, but it exists in the "explored" array, draw it with "dark" colors
        # otherwise, the default is "SHROUD"
        console.rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )
        # np.select lets us conditionally draw the tiles we want, based on what is specified in
        # the Condition list (condlist).
        # it increments through the arrays we have that constitute the map/
        # if its visible, it uses the first value in choicelist (light)
        # if it is not visible, but explored, use the second value (dark)
        # otherwise, use SHROUD, which we define as default

        # iterate through self.entities (which refers to the Engine class's {entities})
        for entity in self.entities:
            # only print entities in the FOV, hence the IF
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

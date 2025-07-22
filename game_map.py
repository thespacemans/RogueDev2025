import numpy as np  # type: ignore
from tcod.console import Console

import tile_types


class GameMap:
    """Class that defines the game map, which is a 2D array of tiles of specified types"""

    # takes width and height integers and assigns them in one line
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        # this line creates a 2D array filled with the same values, in this case the Floor tile
        # this fills self.tiles with floor tiles
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")

        # this line replaces the floor at certain indices
        # with a small, three-tile wide wall
        # this ain't normally hard-coded so WILL REMOVE LATER
        self.tiles[30:33, 22] = tile_types.wall

    # this method will check if given x and y coordinates are within the bounds of the map
    # ensures the player doesn't wander off into the void
    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of
        this map's specified width and height"""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """Using the Console class's tiles_rgb method, render the map to console"""
        # this is much faster than using the console.print method that is used
        # for individual entities
        console.rgb[0 : self.width, 0 : self.height] = self.tiles["dark"]

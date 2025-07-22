"""File that contains tile types for the game"""

from typing import Tuple

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb
# the dtype method creates a datatype within numpy, it behaves like a struct in C
# this type contains three parts
# ch: the character, in integer format, translated into unicode
# fg: foreground color, in RGB format (3B means 3 unsigned bytes)
# bg: background color, also in RGB format
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically-defined tile data.
# this is another dtype from numpy, which is used to describe the properties of a single tile
# walkable: whether the tile can be walked over
# transparent: whether the tile blocks field of view
# dark: the graphic for when the tile is not in field of view
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over
        ("transparent", np.bool),  # True if this tile doesn't block FOV
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV
        # this last one uses the previously defined graphic_dt, which holds the character to print,
        # foreground color, and background color as you recall
        # why is it called dark? because later we'll want to differentiate between tiles that
        # are and aren't in the FOV
    ]
)


# creates a numpy array of just one tile_dt element and returns it
# star character is used to enforce keyword arguments
# it can accept any number of non-kwargs, but they won't matter because
# they don't correspond to any parameter, so you MUST use keywords to specify the parameters
def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark), dtype=tile_dt)


# here's a few tile types, more can be added as needed with more properties later
# the types presented here are self-explanatory
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
)

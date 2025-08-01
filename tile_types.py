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
        ("ch", np.int32),  # Unicode codepoint, aka a LETTER OR SYMBOL
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors; fg for foreground color
        ("bg", "3B"),  # bg for background color
    ]
)

# Tile struct (aka datatype constructor) used for statically-defined tile data
# as opposed to dynamically defined, like enemies moving over tiles
# this is a dtype from numpy, which is used to describe the properties of a single tile
# walkable: whether the tile can be walked over (true/false)
# transparent: whether the tile blocks field of view (true/false)
# dark: graphic for when the tile is not in field of view (type of graphic_dt as defined above)
# light: graphic for when the tile is in field of view (type of graphic_dt)
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over
        ("transparent", np.bool),  # True if this tile doesn't block FOV
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV
        ("light", graphic_dt),  # graphics for when the tile is in FOV
        # the latter two take graphic_dt, which holds the symbol,
        # and fg and bg color (as defined above)
    ]
)


# creates a numpy array of just one tile_dt element and returns it
# star character is used to enforce keyword arguments
# it can accept any number of non-kwargs, but they won't matter because
# they don't correspond to any parameter, so you MUST use keywords to specify the parameters
def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    # for a given tile type, we stipulate whether it is walkable/transparent, and provide
    # dark and light colors for said tile
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles (fog of war, essentially)
# it just draws a black tile
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

# here's a few tile types, more can be added as needed with more properties later
# the types presented here are self-explanatory
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)

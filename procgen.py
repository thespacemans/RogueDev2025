"""Module that procedurally generates dungeons."""

from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

import entity_factories
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity


class RectangularRoom:
    """Defines properties and methods for a single rectangular room.

    Init takes arguments of `x` and `y` coordinates, as well as `width` and `height` of the room.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        # takes the x and y coordinates of the top left corner, and
        # computes the bottom right based on width and height params
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    # properties are like read-only variables for this Class
    # this one describes the x and y coordinates of the center of a room
    @property
    def center(self) -> Tuple[int, int]:
        """Returns the x-y coordinates of the center of a room."""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    # this property returns two "slices", which represent the inner portion of the room
    # this is the part that is "dug out" for the room in the dungeon generator
    # so this gives us an easy way to get the area we need to carve out
    @property
    def inner(self) -> Tuple[slice, slice]:
        """Returns the inside area of a room as 2D array indices."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
        # the +1 ensures there's always at least one tile of wall between two rooms
        # it does this by basically resizing each room to be one tile smaller on each axis

    def intersects(self, other: RectangularRoom) -> bool:
        """Returns true if this room overlaps with another rectangular room."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def place_entities(
    room: RectangularRoom, dungeon: GameMap, maximum_monsters: int
) -> None:
    """Places entities inside individual rooms"""
    number_of_monsters = random.randint(0, maximum_monsters)

    # the _ means a variable that is intentionally ignored (ex: only used as a for-loop index)
    for _ in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entity_factories.orc.spawn(dungeon, x, y)
            else:
                entity_factories.troll.spawn(dungeon, x, y)


# function takes two arguments, both tuples of two integers
# returns iterator of a tuple of two integers
# all the tuples are x and y coords on the map
def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Returns an L-shaped tunnel between two given points."""

    # get the coords out of the tuples
    x1, y1 = start
    x2, y2 = end

    # decide the path shape randomly
    if random.random() < 0.5:  # aka 50% chance
        # move horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # move vertically, then horizontally
        corner_x, corner_y = x1, y2

    # generate coordinates for this tunnel
    # this uses tcod's built in Bresenham line generator (usually used for LOS calculations)
    # it's useful here to get a line from one point to another
    # we take one line to the corner, then another to the end of the line
    # creates an L-shaped tunnel!
    # and tolist() converts the points in the line into a list
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
    # yield is an interesting case
    # essentially lets you return a generator
    # rather than returning the values and exiting the fucntion altogether,
    # we return the values but keep the local state
    # this lets the function pick up where it left off when called again, rather than starting over
    # this is useful because we need to iterate over these x,y values to dig out the tunnel


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    max_monsters_per_room: int,
    player: Entity,
) -> GameMap:
    """Generates a new dungeon map."""
    # initialize a gamemap called dungeon with specified indices
    dungeon = GameMap(map_width, map_height, entities=[player])

    # keep a running list of all the rooms
    rooms: List[RectangularRoom] = []

    # iterate from 0 to max_rooms - 1
    # the algorithm may or may not place a room pending intersection status
    # so we don't know how many rooms we'll end up with
    for _ in range(max_rooms):

        # set the room's dimensions randomly within the provided ranges
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        # attempt to place the room within the dungeon map
        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # turn this room into an instance of the RectangularRoom class
        # it makes rectangles easier to work with, because of the methods it possesses
        new_room = RectangularRoom(x, y, room_width, room_height)

        # run through other rooms and see if they intersect with this one
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # this room intersects, so go to the next attempt
        # if no intersections then the room is valid

        # dig out this room's inner area
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # the first room, where the player starts
            player.x, player.y = new_room.center
        else:  # all rooms after the first
            # dig out a tunnel between this room and the previous one
            # the negative index (-1) lets us use the previous room for
            # the tunnel_between function
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        place_entities(new_room, dungeon, max_monsters_per_room)

        # finally, append the new room to the list
        # so the next iteration can use it
        rooms.append(new_room)

    return dungeon

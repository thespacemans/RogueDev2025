"""Module that defines engine properties."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
    from input_handlers import EventHandler
    from entity import Actor
    from game_map import GameMap

    # from tcod.context import Context


class Engine:
    """Class that deals with computing, rendering, and event handling.

    Init takes object of type `Entity`, the player.
    """

    game_map: GameMap

    # upon initialization, this engine object represents the game's state
    # and it is utilized and modified on each game loop iteration
    # for the default state we use the default control handler
    def __init__(self, player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (int(0), int(0))
        self.player = player

    def handle_enemy_turns(self) -> None:
        """Handles the turns of all entities, except the `player`."""

        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    # sets the game_map's visible tiles to equal the result of compute_fov
    # give compute_fov three arguments:
    # transparency, to which we pass the array "self.game_map.tiles["transparent"]"
    #   this arg takes a 2d array and considers any nonzero values to be transparent
    # pov, which is the origin of the field of view (just a 2D index, uses player's x-y position)
    # radius, which is how far the FOV extends in tiles
    def update_fov(self) -> None:
        """Recomputes the visible area based on player's point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"], (self.player.x, self.player.y), radius=8
        )
        # if a tile is "visible", it should be added to "explored"
        # the |= operand sets the explored array to include everything in the visible array,
        # plus whatever it already contained
        # so any tile the player can see automatically becomes one that has been explored
        self.game_map.explored |= self.game_map.visible

    # passing a colon as argument (see above) retrieves all the elements of the array
    # so it runs the function on the visible array
    # and modifies the elements of it in a certain "location" on that array
    #   this makes sense if we imagine the array as a 2D map, which is what the game does.
    #   how about that lmao
    # the location on that array is defined by the player's location and the radius

    def render(self, console: Console) -> None:
        """Draws the game map, entities, and more to the game window."""
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        # renders health bar
        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        # renders entity names at the mouse's location
        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)

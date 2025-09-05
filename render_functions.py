from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    """Retrieves an `entity`'s name at the given `x, y` coordinates."""

    # check to ensure the spot is within bounds, AND are currently visible
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    # if they are, then create a string that contains all the entity names at that spot
    # separated by a comma of course
    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    # then return the string, capitalized for cleanliness
    return names.capitalize()


def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
):
    """Renders the health bar to a hard-coded position on screen.

    Accepts `console` [to utilize `draw_rect`], the player's `current_value` of HP,
    their `maximum_value` of HP, the desired `total_width` of the bar.
    """
    bar_width = int(float(current_value) / maximum_value * total_width)

    # utilize draw_rect functions from tcod to draw rectangular bars
    # we draw two, one atop the other
    # the first one, here, is the background (and it's red, in this case)
    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=color.bar_empty)

    # the second bar, here, is the foreground (and it's green)
    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    # also print the HP value over the bar, so the player can know the exact number
    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
    )


def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    """Renders entity names at the mouse's position in the game window.

    `x` and `y` are the mouse's current tile coordinates."""

    # takes the console, xy coords, and the engine
    # from the engine, it gets the mouse's current x and y positions
    # (which can be altered by the input handler modifications we made)
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=names_at_mouse_location)

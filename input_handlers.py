"""Module that defines event handling classes."""

from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

import tcod
from actions import Action, BumpAction, EscapeAction, WaitAction

if TYPE_CHECKING:
    from engine import Engine

# define global constant of movement keys so we don't have to futz with this shit later
MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_9: (1, -1),
}

WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
}


# create EventHandler as a Protocol
# this will let us define other ways to interact with the game later
# ex: like moving a cursor inside a menu or interface, vs maneuvering around the map
class EventHandler(Protocol):
    """Generic interface definition for all event handlers."""

    def __init__(self, engine: Engine):
        pass

    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        """Generic definition for the `on_event` method of protocol `EventHandler`."""

    def handle_events(self, context: tcod.context.Context):
        """Generic definition for `handle_events` method of protocol `EventHandler`."""

    def handle_key(self, sym: tcod.event.KeySym, /) -> Optional[Action]:
        """Generic definition for `handle_key` method of protocol `EventHandler`."""

    def on_render(self, console: tcod.console.Console):
        """Generic definition for `on_render` method of protocol `EventHandler`."""
        pass

    def find_mouse_position(self, event: tcod.event.MouseMotion) -> None:
        pass


# this class ducktypes as EventHandler via the protocol
# this one is specifically for moving the player character in the map space
class MainGameEventHandler(EventHandler):
    """Handles events while inside the default play space."""

    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, context: tcod.context.Context) -> None:
        """Loops through `tcod.event.wait()` for events.

        If the event matches with a defined action, finds that action, then performs that action.

        After, handles enemy turns and updates the player's FOV."""
        for event in tcod.event.wait():

            # use context.convert_event to give the event object knowledge on the mouse's position
            #   convert_event "returns an event with mouse pixel coordinates
            #   converted into tile coordinates"
            context.convert_event(event)
            # then dispatch the event to be handled like normal
            action = self.on_event(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action.

    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        """Accepts control events and routes them to relevant methods."""
        match event:
            case tcod.event.Quit():
                raise SystemExit()
            case tcod.event.KeyDown():
                return self.handle_key(event.sym)
            case tcod.event.MouseMotion():
                return self.find_mouse_position(event)
            case _:
                pass

    def handle_key(self, sym: tcod.event.KeySym, /) -> Optional[Action]:
        """Accepts keypress events and outputs the relevant action."""

        action: Optional[Action] = None

        player = self.engine.player

        if sym in MOVE_KEYS:
            dx, dy = MOVE_KEYS[sym]
            action = BumpAction(player, dx, dy)
        elif sym in WAIT_KEYS:
            action = WaitAction(player)
        elif sym == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(player)

        # No valid key was pressed
        return action

    def on_render(self, console: tcod.console.Console) -> None:
        """Tells the `Engine` class to call its render method, using the given console."""
        self.engine.render(console)

    def find_mouse_position(self, event: tcod.event.MouseMotion) -> None:
        mouse_x, mouse_y = int(event.tile.x), int(event.tile.y)
        if self.engine.game_map.in_bounds(mouse_x, mouse_y):
            self.engine.mouse_location = mouse_x, mouse_y


class GameOverEventHandler(EventHandler):
    """Handles events when the player has died."""

    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, context: tcod.context.Context) -> None:
        """Loops through `tcod.event.wait()` for events.

        If the event matches with a defined action, finds that action, then performs that action.

        After, handles enemy turns and updates the player's FOV."""

        for event in tcod.event.wait():
            context.convert_event(event)
            action = self.on_event(event)

            if action is None:
                continue

            action.perform()

    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        """Accepts quit events and routes them to the correct method."""
        match event:
            case tcod.event.Quit():
                raise SystemExit()
            case tcod.event.KeyDown():
                return self.handle_key(event.sym)
            case tcod.event.MouseMotion():
                return self.find_mouse_position(event)
            case _:
                pass

    def handle_key(self, sym: tcod.event.KeySym, /) -> Optional[Action]:
        """Detects the user hitting the escape key."""
        action: Optional[Action] = None

        if sym == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(self.engine.player)

        # No valid key was pressed
        return action

    def find_mouse_position(self, event: tcod.event.MouseMotion) -> None:
        mouse_x, mouse_y = int(event.tile.x), int(event.tile.y)
        if self.engine.game_map.in_bounds(mouse_x, mouse_y):
            self.engine.mouse_location = mouse_x, mouse_y

    def on_render(self, console: tcod.console.Console) -> None:
        """Tells the `Engine` class to call its render method, using the given console."""
        self.engine.render(console)

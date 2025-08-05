"""Module that defines event handling classes."""

from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

import tcod.event
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

    def handle_events(self):
        """Generic definition for `handle_events` method of protocol `EventHandler`."""


# this class ducktypes as EventHandler via the protocol
# this one is specifically for moving the player character in the map space
class DefaultControlHandler(EventHandler):
    """Handles events while inside the default play space."""

    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        """Loops through tcod.event.wait() for events.

        If the event matches with a defined action, finds that action.

        Then performs that action.

        After, handles enemy turns and updates the player's FOV."""
        for event in tcod.event.wait():
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


class GameOverEventHandler(EventHandler):
    """Handles events when the player has died."""

    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        """Loops through tcod.event.wait() for events.

        If the event matches with a defined action, finds that action.

        Then performs that action.

        After, handles enemy turns and updates the player's FOV."""

        for event in tcod.event.wait():
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
            case _:
                pass

    def handle_key(self, sym: tcod.event.KeySym, /) -> Optional[Action]:
        """Detects the user hitting the escape key."""
        action: Optional[Action] = None

        if sym == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(self.engine.player)

        # No valid key was pressed
        return action

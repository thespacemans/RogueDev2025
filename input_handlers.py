"""Module that defines event handling classes."""

from __future__ import annotations

from typing import Optional, Protocol, TYPE_CHECKING

import tcod.event
from actions import Action, BumpAction, EscapeAction

if TYPE_CHECKING:
    from engine import Engine


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
class DefaultControlHandler:
    """Handles events while inside the default play space."""

    def __init__(self, engine: Engine):
        self.engine = engine

    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        """Accepts events and routes them to relevant methods."""
        match event:
            case tcod.event.Quit():
                raise SystemExit()
            case tcod.event.KeyDown():
                return self.handle_key(event.sym)
            case _:
                pass

    def handle_key(self, sym: tcod.event.KeySym, /) -> Optional[Action]:
        """Accepts keypress events and outputs the related action."""

        action: Optional[Action] = None
        player = self.engine.player

        match sym:
            case tcod.event.KeySym.UP:
                action = BumpAction(player, dx=0, dy=-1)
            case tcod.event.KeySym.DOWN:
                action = BumpAction(player, dx=0, dy=1)
            case tcod.event.KeySym.LEFT:
                action = BumpAction(player, dx=-1, dy=0)
            case tcod.event.KeySym.RIGHT:
                action = BumpAction(player, dx=1, dy=0)
            case tcod.event.KeySym.ESCAPE:
                action = EscapeAction(player)

        return action

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.on_event(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action.

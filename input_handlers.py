"""Module that defines event handling classes."""

from __future__ import annotations

# utilize python's type hinting system here
# optional denotes something that could be set to None
from typing import Optional, Protocol

import tcod.event
from actions import Action, EscapeAction, BumpAction


# create EventHandler as a Protocol
# this will let us define other ways to interact with the game later
# ex: like moving a cursor inside a menu or interface, vs maneuvering around the map
class EventHandler(Protocol):
    """Interface definition for all event handlers."""

    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        """Generic definition for valid method of class EventHandler."""


# this class ducktypes as EventHandler via the protocol
# this one is specifically for moving the player character in the map space
class DefaultControlHandler:
    """Handles events while inside the default play space."""

    def __init__(self):
        pass

    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        """Intercepts events and routes them to relevant methods."""
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

        match sym:
            case tcod.event.KeySym.UP:
                action = BumpAction(dx=0, dy=-1)
            case tcod.event.KeySym.DOWN:
                action = BumpAction(dx=0, dy=1)
            case tcod.event.KeySym.LEFT:
                action = BumpAction(dx=-1, dy=0)
            case tcod.event.KeySym.RIGHT:
                action = BumpAction(dx=1, dy=0)
            case tcod.event.KeySym.ESCAPE:
                action = EscapeAction()

        return action

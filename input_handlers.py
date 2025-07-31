"""File that handles events like user keypresses"""

# utilize python's type hinting system here
# optional denotes something that could be set to None
from typing import Optional, Protocol

import tcod.event

from actions import Action, EscapeAction, MovementAction


# create EventHandler as a Protocol
# this will let us define other ways to interact with the game later
# ex: like moving a cursor inside a menu or interface, vs maneuvering around the map
class EventHandler(Protocol):
    """Interface definition for all event handlers"""

    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]: ...


# this class ducktypes as EventHandler via the protocol
# this one is specifically for moving the player character in the map space
class DefaultControlHandler:
    """Handles events while in the default play space"""

    def __init__(self):
        pass

    def on_event(self, event: tcod.event.Event, /) -> Optional[Action]:
        match event:
            case tcod.event.Quit():
                raise SystemExit()
            case tcod.event.KeyDown():
                return self.handle_key(event.sym)
            case _:
                pass

    def handle_key(self, sym: tcod.event.KeySym, /) -> Optional[Action]:
        action: Optional[Action] = None

        match sym:
            case tcod.event.KeySym.UP:
                action = MovementAction(dx=0, dy=-1)
            case tcod.event.KeySym.DOWN:
                action = MovementAction(dx=0, dy=1)
            case tcod.event.KeySym.LEFT:
                action = MovementAction(dx=-1, dy=0)
            case tcod.event.KeySym.RIGHT:
                action = MovementAction(dx=1, dy=0)
            case tcod.event.KeySym.ESCAPE:
                action = EscapeAction()

        return action

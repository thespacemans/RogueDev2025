"""File that handles events like user keypresses"""

# part of Python’s type hinting system
# Optional denotes something that could be set to None
from typing import Optional

# import tcod's event system, since we only need that (and not all of tcod)
import tcod.event

# import the action classes we just made
from actions import Action, EscapeAction, MovementAction


# create EventHandler, which is a subclass of tcod's EventDispatch class
# it allows us to send an event to its proper method based on what type of event it is
class EventHandler(tcod.event.EventDispatch[Action]):
    """Handles events such as user keypresses and mouse clicks"""

    # here we use a method from EventDispatch:
    # ev_quit is defined in that class, but we are overriding it in our EventHandler subclass
    # ev_quit is called when a quit event is received, which comes from clicking [X]
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    # another overridden method here
    # this method receives key press events, and returns returns either the relevant Action
    # or None if no valid key was pressed
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:

        # this is the variable that will hold whatever subclass of Action we end up assigning to it
        # if no valid keypress is found, remain set to None
        action: Optional[Action] = None

        # this contains the actual key that was pressed
        # note that it doesn't include modifiers like shift or alt!
        key = event.sym

        # this goes through all the possible keys that we want to watch for
        # and assigns the correct movement to its indices
        if key == tcod.event.KeySym.UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT:
            action = MovementAction(dx=1, dy=0)

        # if user presses escape, return EscapeAction to exit the game
        # this will probably be replaced by a pause menu later
        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        # will return any of the possible action cases above, or None if none apply
        return action

from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler


class Engine:
    """Game engine loop, responsible for rendering and handling events"""

    def __init__(
        self, entities: Set[Entity], event_handler: EventHandler, player: Entity
    ):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player

    # some notes:
    # {entities} is a *set* (of entities), which behaves kind of like a list that
    # enforces uniqueness. ergo, we cannot add an Entity to the set twice,
    # whereas a list would allow that. in this case, having an entity in
    # {entities} twice does not make sense.

    # event_handler is the same event_handler that we used in main.py.
    # player is the player instance of the Entity class.
    # having a separate reference to it is handy cause we need to access it
    # more often than any other random entity

    def handle_events(self, events: Iterable[Any]) -> None:
        """Handles user-input events like keypresses"""
        # send the event to the event_handler's "dispatch" method,
        # which sends the event to the proper place
        # here, a keyboard event will be send to the ev_keydown method we wrote
        # that method returns an action and gets assigned to the action variable here
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue
            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)
            elif isinstance(action, EscapeAction):
                raise SystemExit()

    def render(self, console: Console, context: Context) -> None:
        """Draws entities and other objects to the game window"""
        # iterate through self.entities (which refers to the Engine class's {entities})
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)
        context.present(console)
        console.clear()

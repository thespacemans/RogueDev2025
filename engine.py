from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    """Game engine class, responsible for rendering and handling events"""

    # upon initialization, represents the game's state
    # and is utilized and modified on each game loop iteration

    def __init__(
        self,
        entities: Set[Entity],
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
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

            # takes the place of unwieldy if statements
            # basically handles inputs! wow!
            action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        """Draws entities and other objects to the game window"""
        self.game_map.render(console)
        # iterate through self.entities (which refers to the Engine class's {entities})
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)
        context.present(console)
        console.clear()

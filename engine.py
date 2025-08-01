"""Module that defines engine properties."""

from __future__ import annotations

from typing import Set, Iterable, Any, TYPE_CHECKING
from tcod.map import compute_fov

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap
    from input_handlers import EventHandler
    from tcod.context import Context
    from tcod.console import Console


class Engine:
    """Class that deals with computing, rendering, and event handling."""

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
        self.update_fov()

    # some notes:
    # {entities} is a `set` (of entities), which behaves kind of like a list that
    # enforces uniqueness. ergo, we cannot add an Entity to the set twice,
    # whereas a list would allow that. in this case, having a singular entity in
    # {entities} twice does not make sense. we need two separate entities to represent
    # two different enemies, for example

    # event_handler is the same event_handler that we used in main.py.
    # player is the player instance of the Entity class.
    # having a separate reference to it is handy cause we need to access it
    # more often than any other random entity

    def handle_events(self, events: Iterable[Any]) -> None:
        """Handles user-input events, such as keypresses."""
        # send the event to the event_handler's "dispatch" method,
        # which sends the event to the proper place
        # here, a keyboard event will be send to the ev_keydown method we wrote
        # that method returns an action and gets assigned to the action variable here
        for event in events:
            action = self.event_handler.on_event(event)

            if action is None:
                continue

            # takes the place of unwieldy if statements
            # basically handles inputs! wow!
            action.perform(self, self.player)

            self.update_fov()  # update the FOV before the player's next action

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

    def render(self, console: Console, context: Context) -> None:
        """Draws the game map, entities, and more to the game window."""
        self.game_map.render(console)

        # iterate through self.entities (which refers to the Engine class's {entities})
        for entity in self.entities:
            # only print entities in the FOV, hence the IF
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        # this part actually outputs the various arrays we've toodled with
        # to the console window
        context.present(console)
        # and this just empties the console to be filled with array stuff later
        # this seems like frame generation and disposal, just for a text-based display
        console.clear()

"""File to initialize action classes for the game."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    """Generic base class for actions in the game"""

    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


# subclass of Action
class EscapeAction(Action):
    """Action subclass that allows the player to exit the game."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


# subclass of Action
# dx and dy will be used to describe the nature of the MovementAction
# (essentially where the player wants to go, represented in a class)
class MovementAction(Action):
    """Action subclass that quantifies movement in the game based on user keypress"""

    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    # each subclass of action having a perform() method is actually genius
    # because the action that invokes it has access to its Self parameter,
    # it will always utilize the correct perform action based on what key is pressed
    # and so as we define more subclasses of Action, they can self-sort as they call
    # the perform method in Engine.handle_events()
    # very elegant!
    # apparently this is called polymorphism
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        # Check if the destination is within bounds and walkable
        # if either is not true, do not perform the action
        # (return breaks out of the perform method)
        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.

        entity.move(self.dx, self.dy)

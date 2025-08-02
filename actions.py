"""Module that initializes action classes."""

from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action(Protocol):
    """Generic base class for actions in the game."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

    # each subclass of action having a perform() method is actually genius
    # because the action that invokes it has access to its Self parameter,
    # it will always utilize the correct perform action based on what key is pressed
    # and so as we define more subclasses of Action, they can self-sort as they call
    # the perform method in Engine.handle_events()
    # very elegant!
    # apparently this is called polymorphism


# subclass of Action
class EscapeAction(Action):
    """`Action` subclass that allows the player to exit the game."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


# subclass of Action
# dx and dy are used to describe the direction
class ActionWithDirection(Action):
    """`Action` subclass that defines an action's direction."""

    def __init__(self, dx: int, dy: int):

        # calls the init method of the parent class (in this case, Action)
        # from within the subclass
        # this ensures that any init code in the parent class runs before the
        # subclass adds its own initialization
        # this is vital for proper inheritance
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


# subclass of ActionWithDirection
class MeleeAction(ActionWithDirection):
    """`ActionWithDirection` subclass that attacks a blocking entity."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            return  # No entity to attack

        print(f"You kissy the {target.name}. Mwah!")


# subclass of ActionWithDirection
class MovementAction(ActionWithDirection):
    """`ActionWithDirection` subclass that facilitates movement, with conditions."""

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        # Check if the destination is within bounds and walkable
        # if either is not true, do not perform the action
        # (return breaks out of the perform method and thus aborts the move)
        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        entity.move(self.dx, self.dy)


# subclass of ActionWithDirection
class BumpAction(ActionWithDirection):
    """`ActionWithDirection` subclass that routes a directed action to its appropriate method."""

    # this class also inherits from ActionWithDirection, but its perform method doesn't
    # do anything except decide between which class (between MeleeAction and MovementAction)
    # that must be utilized
    # those classes actually do the work. this one just chooses the appropriate one to call
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)

        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)

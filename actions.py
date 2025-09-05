"""Module that initializes action classes."""

from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import color

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity


# in hindsight, changing this file so drastically to use Protocols was a brave choice.
# have since reverted to the tutorial baseline, so that this refactor in part 6 is
# even a little bit achievable for my skill level and knowledge


class Action:
    """Base class for action types."""

    # its okay to call super() here even if Action has no parent because
    # we never call a plain Action() class anywhere in the code
    # so that super is only used by the subclasses that inherit it
    # and it eventually refers to THIS VERY CLASS
    # we replace the type hint with Actor because only Actors should be taking actions anyway
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Returns the `engine` object that this `action` belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


# recall that subclasses inherit the methods of the parent class
# and because we didn't overwrite init, it uses the parent's init
# and so it has access to those instance-specific attributes just by being a subclass
class EscapeAction(Action):
    """Subclass of `Action` that allows us to close the game."""

    def perform(self) -> None:
        raise SystemExit()


class WaitAction(Action):
    """Subclass of `Action` that is used to pass a turn."""

    # represents an actor saying "I'll do nothing this turn"
    def perform(self) -> None:
        pass


class ActionWithDirection(Action):
    """Subclass of `Action` that contains that action's desired direction in x-y space."""

    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    # @property lets you define a method that can be ACCESSED like an ATTRIBUTE
    # you can access the result of that method just by using dot notation,
    # no need to call it as a function
    # e.g.: self.dest_xy returns a pair of x-y values in a tuple
    # useful for creating read-only or computed attributes
    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this `Action`'s destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking `Entity` at this `Action`'s destination."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)
        # recall that the * is the unpacking operator
        # it lets you turn iterables into a series of positional arguments
        # way better than using for loops or whatever else to iterate the contents of an array

    @property
    def target_actor(self) -> Optional[Actor]:
        """Returns the actor at this `action`'s destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)
        # this gives us an easy way to find the actor at the destination we're referring to

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    """Subclass of `ActionWithDirection` that attempts a melee attack on a blocking entity."""

    # calculate the damage (attacker power minus defenders defense), assign a description to the attack
    # and if it's greater than 0 we apply it
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            return  # No entity to attack.

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # Destination is blocked by a tile.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        # if none of the above breaks us out of the function, finally move the entity
        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

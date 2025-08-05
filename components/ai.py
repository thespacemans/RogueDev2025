from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
import tcod

from actions import Action, MeleeAction, MovementAction, WaitAction
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action, BaseComponent):

    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError()

    # uses the "walkable" tiles in our map, along with some tcod pathfinding tools,
    # to get the bath from the BaseAI's parent entity to whatever the target might be
    # in the tutorial that target will always be the player, but that can be changed
    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Computes and returns a path to the target position.

        If there is no valid path, then returns an empty list.
        """
        # first copy the array of walkable tiles from the current gamemap
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        # cost refers to how "costly" (time consuming) it will be to get to the target
        # if a piece of terrain takes longer to traverse, the cost will be higher
        # in this tutorial all parts of the map have the same cost, but
        # the cost array allows us to take other entities into account
        for entity in self.entity.gamemap.entities:
            # check that an entity blocks movement and the cost isn't zero (blocking)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position
                # A lower number means more enemies will crowd behind each other in hallways
                # A higher number means enemies will take longer paths in order to surround the player
                cost[entity.x, entity.y] += 10
        # essentially: if an entity exists at a spot on the map, we increase the cost of moving there to 10
        # what this does is encourage the entity to move around the blocking entity

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]


class HostileEnemy(BaseAI):
    """Subclass of `BaseAI` that is hostile to the player."""

    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        # set hostile enemy target as the player
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance

        # if the player is right next to the entity, attack the player
        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()

            self.path = self.get_path_to(target.x, target.y)

        # if the player can see the entity, but the entity is too far to attack, move towards player
        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity,
                dest_x - self.entity.x,
                dest_y - self.entity.y,
            ).perform()

        # if the entity is not in the player's vision, just wait
        return WaitAction(self.entity).perform()

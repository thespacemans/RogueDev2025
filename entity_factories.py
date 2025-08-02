"""Module for defining entities."""

# this makes it more extensible: we can just define whatever entities we want later
# these are the instances we clone to create our new entities with the Entity.spawn() method

from entity import Entity

player = Entity(char="@", color=(255, 255, 255), name="Player", blocks_movement=True)

orc = Entity(char="R", color=(63, 127, 63), name="Robot", blocks_movement=True)
troll = Entity(char="D", color=(0, 127, 0), name="Drone", blocks_movement=True)

from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from input_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


# we import and inherit from BaseComponent, which gives access to
# the parent entity and the engine
class Fighter(BaseComponent):
    """Component applied to any entity that will fight.

    Constructor takes `hp: int`, `defense: int`, and `power: int`.
    """

    entity: Actor

    # hp is hit points
    # defense is how much taken damage will be reduced
    # power is the entity's raw attack power
    def __init__(
        self,
        hp: int,
        defense: int,
        power: int,
    ):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    # the underscore before _hp indicates its for internal use
    # hints to other developers that the variable is not part of the class's interface
    # and nominally cannot be accessed (though you still can, the underscore is just for human readers)
    # hence why we define a getter and setter method to make it rigidly defined

    # we define both a getter and setter for hp, which allows the class to access hp like
    # a normal variable. the getter just returns the HP value
    # the setter lets us modify the value as its set within the method
    # the 'getter':
    @property
    def hp(self) -> int:
        return self._hp

    # the 'setter':
    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(
            0, min(value, self.max_hp)
        )  # this line means that _hp will never be set less than 0, but also won't ever go higher than the max_hp attribute
        if self._hp == 0 and self.entity.ai:
            self.die()

    # when an actor dies, we use the die method to do a lot of things at once
    # print out a message indicating the entity's death
    # set its color to red
    # set blocks_movement to false so it can be passed over
    # remove ai from the entity so it'll be marked as dead and won't take any more turns
    # change the name to "remains of name"

    def die(self) -> None:
        if self.engine.player is self.entity:
            death_message = "You died...?"
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.entity.name} is dead!"

        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.render_order = RenderOrder.CORPSE
        self.entity.name = f"remains of {self.entity.name}"

        print(death_message)

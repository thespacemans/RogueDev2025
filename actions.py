"""File to initialize action classes for the game."""


class Action:
    """TBD"""


# subclass of Action
class EscapeAction(Action):
    """TBD"""


# subclass of Action
# dx and dy will be used to describe the nature of the MovementAction
# (essentially where the player wants to go, represented in a class)
class MovementAction(Action):
    """Action that quantifies movement in the game based on user keypress"""

    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

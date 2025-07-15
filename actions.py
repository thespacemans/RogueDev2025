class Action:
    pass


# subclass of Action
class EscapeAction(Action):
    pass


# subclass of Action
# dx and dy will be used to describe the nature of the MovementAction
# (essentially where the player wants to go, represented in a class)
class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

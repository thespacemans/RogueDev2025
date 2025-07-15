#!/usr/bin/env python
import tcod


# import the two classes we need from actions
# and the event handler we created before too
# so we can use those functions here in main
from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def main() -> None:  # the arrow and None typing do

    # variables for screen size
    screen_width = 80
    screen_height = 50

    # variables to track player position
    # be sure to cast to int since python 3 doesn't truncate division automatically
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # telling tcod which font to use, reading from the dejavu tileset in the project folder
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # this creates an instance of our EventHandler class
    # by creating it, that makes it usable to receive events and process them
    # because otherwise it's just a class. it doesn't do anything unless instanced and utilized, duh
    event_handler = EventHandler()

    # creates the screen, given width and height and a window title
    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        # creates the console, which is what we draw to
        # set this console to the same width and height as the new terminal window
        # that way they overlap nicely
        # 'order' arg affects the order of x,y variables in numpy to make them more human-readable
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        # starts the game loop
        while True:
            # tells the console where to place the @ symbol
            root_console.print(x=player_x, y=player_y, text="@")

            # this line is what actually prints to the screen
            context.present(root_console)

            # clears the console after each draw so it doesn't leave leftovers
            root_console.clear()

            # check for keypress event in the buffer every "frame"
            for event in tcod.event.wait():
                # send the event to the event_handler's "dispatch" method,
                # which sends the event to the proper place
                # here, a keyboard event will be send to the ev_keydown method we wrote
                # that method returns an action and gets assigned to the action variable here
                action = event_handler.dispatch(event)

            if action is None:
                continue

            # check if the action is an instance of the class MovementAction
            # if yes, move the player's coordinates
            # remember that those are used by the console above to place the player
            if isinstance(action, MovementAction):
                player_x += action.dx
                player_y += action.dy

            # if hit escape key, quit the game
            elif isinstance(action, EscapeAction):
                raise SystemExit()


# boilerplate code to prevent main from being run unless we specifically invoke it from main
# if this module was called by another script, the name would not match,
# and so we would not want to run main
if __name__ == "__main__":
    main()

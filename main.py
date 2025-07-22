"""This file initializes the game and runs the main loop."""

#!/usr/bin/env python
import tcod


# import the various classes we need from the other files
from engine import Engine
from input_handlers import EventHandler
from entity import Entity


def main() -> None:
    """Main function to run the game loop."""
    # "-> None" is a kind of type annotation in python
    # it is used here because the main() function does not return a value at all
    # there are also ways to do it within function args

    # variables for screen size
    screen_width = 80
    screen_height = 50

    # telling tcod which font to use, reading from the dejavu tileset in the project folder
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # this creates an instance of our EventHandler class
    # by creating it, that makes it usable to receive events and process them
    # because otherwise it's just a class sitting in a file
    # it doesn't do anything unless instanced and utilized in the scope of main()
    event_handler = EventHandler()

    # create a player and an NPC entity, place both in a set
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    # utilize an instance of the Engine class to handle event processing
    # and rendering to the game window
    engine = Engine(entities=entities, event_handler=event_handler, player=player)

    # creates the screen, given width and height and a window title
    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Pylon Delta",
        vsync=True,
    ) as context:
        # creates the console, which is what we draw to
        # set this console to the same width and height as the new terminal window
        # that way they overlap nicely
        # 'order' arg affects the order of x,y variables in numpy to make them more human-readable
        root_console = tcod.console.Console(screen_width, screen_height, order="F")

        # starts the game loop
        while True:
            # renders entities and map to the game window
            engine.render(console=root_console, context=context)

            # catches events as they occur during the game loop
            events = tcod.event.wait()

            # handles those events (wow! fancy that!)
            engine.handle_events(events)


# boilerplate code to prevent main from being run unless we specifically invoke it from main
# if this module was called by another script, the name would not match,
# and so we would not want to run main
if __name__ == "__main__":
    main()

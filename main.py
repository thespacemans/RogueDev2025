"""This file initializes the game and runs the main loop."""

#!/usr/bin/env python
# import the various classes we need from the other files
from typing import TYPE_CHECKING
import tcod
from engine import Engine
from input_handlers import DefaultControlHandler
from entity import Entity
from procgen import generate_dungeon

if TYPE_CHECKING:
    from input_handlers import EventHandler


def main() -> None:
    """Main function to run the game loop"""
    # "-> None" is a kind of type annotation in python
    # it is used here because the main() function does not return a value at all
    # there are also ways to do it within function args

    # variables for screen size
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # telling tcod which font to use, reading from the dejavu tileset in the project folder
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    # this creates an instance of our EventHandler class
    # by creating it, that makes it usable to receive events and process them
    # because otherwise it's just a class sitting in a file
    # it doesn't do anything unless instanced and utilized in the scope of main()
    event_handler = DefaultControlHandler()

    # create, position, and color a player and an NPC entity, place both in a set
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "$", (255, 255, 0))
    entities = {npc, player}

    # create an instance of the GameMap class for use in the game loop
    # this time using the new generate_dungeon() function we made
    # now including all the arguments we need to utilize our enhanced procgen function
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player,
    )

    # initialize an instance of the Engine class
    # this handles event processing
    # and rendering to the game window
    engine = Engine(
        entities=entities, event_handler=event_handler, game_map=game_map, player=player
    )

    # creates the window, given width and height and a window title
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
            # this renders the contents of Engine
            #   e.g. entities, map, visibility status, etc
            # to the game windows
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

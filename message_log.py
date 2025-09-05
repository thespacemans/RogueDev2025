from typing import List, Reversible, Tuple
import textwrap

import tcod

import color


class Message:
    """Class used to save and display messages in our log.

    Contains the `plain_text` of the message, the `fg` (foreground color) of the message, and
    the `count` (used for displaying repeated messages in one line)."""

    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1

    # this property returns the text with its count, if the count is greater than 1
    # otherwise it just returns the message as-is
    @property
    def full_text(self) -> str:
        """Contains the full text of this message, including the count if necessary."""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    """Class that keeps a list of `Message` entries."""

    # creates the "messages" attribute and places the Message list within it
    def __init__(self) -> None:
        self.messages: List[Message] = []

    # note that text is required, but the fg will default to white if no color is supplied
    # stack tels us whether to stakc messages or not, which allows us to disable the behavior
    def add_message(
        self,
        text: str,
        fg: Tuple[int, int, int] = color.white,
        *,
        stack: bool = True,
    ) -> None:
        """Adds a message to this log. `text` is the message text, `fg` is text color.

        If `stack` is True, then message can stack with a previous message of the same text.
        """
        # if we allow stacking, and the added message matches the previous emssage, we just
        # increment the previous message's count by 1. otherwise we just add it to the list
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
        self,
        console: tcod.console.Console,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        """Render this log over the given area.

        `x`, `y`, `width`, `height` is the rectangular region to render onto the `console`.
        """
        # calls the render_messages static method, which is what actually renders it to the screen
        # notably in reverse order, to make it appear that messages are scrolling in an upward direction
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def render_messages(
        console: tcod.console.Console,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: Reversible[Message],
    ) -> None:
        """Render the messages provided.

        The `messages` are rendered in reverse order,
        starting at the last message and working backwards.
        """

        # since there's a limited amount of space to print messages, we limit the amount of
        # lines that can be printed and stop printing when that space limit is reached
        y_offset = height - 1

        for message in reversed(messages):
            for line in reversed(textwrap.wrap(message.full_text, width)):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return  # no more space to print messages.

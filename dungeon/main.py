"""Dungeon game: main"""

from blessed import Terminal

from lethal.lethal import Input, Output
from .dungeon_module import DungeonModule


def main() -> int:
    """the main"""
    term = Terminal()
    output = Output(term)

    # init module state
    dm = DungeonModule()  # pylint: disable=invalid-name
    state = dm.create()

    with term.cbreak(), term.fullscreen(), term.hidden_cursor():
        while True:
            # Render
            print(term.home + term.clear, end="")
            dm.draw(state, output)
            output.clear_offset()  # just incase someone forgot to pop

            key = term.inkey()
            if key.is_sequence and key.name == "KEY_ESCAPE":
                # Exit on ESC
                break

            # Generate Input
            user_input = Input([Input.key_to_str(key)])

            # Update
            state = dm.update(state, user_input, 0)

    return 0


if __name__ == "__main__":
    exit(main())

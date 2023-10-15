"""Dungeon game: main"""

from typing import Generic, TypeVar

from blessed import Terminal

from .input import Input
from .output import Output


M = TypeVar("M")
S = TypeVar("S")


class Driver(Generic[M, S]):
    """Terminal game driver"""

    module: M
    state: S
    term: Terminal
    output: Output

    def __init__(self, module: M):
        self.module = module
        self.state = self.module.create()
        self.term = Terminal()
        self.output = Output(self.term)

    def loop(self) -> None:
        """i/o loop"""
        term = self.term
        with term.cbreak(), term.fullscreen(), term.hidden_cursor():
            while True:
                # Render
                print(term.home + term.clear, end="")
                self.module.draw(self.state, self.output)
                self.output.clear_offset()  # just incase someone forgot to pop

                key_str = self._next_key_str()

                if key_str == "KEY_ESCAPE":
                    # Exit on ESC
                    break

                # Update State
                self.state = self.module.update(self.state, Input([key_str]), 0)

    def _next_key_str(self) -> str:
        key = self.term.inkey()
        return Input.key_to_str(key)

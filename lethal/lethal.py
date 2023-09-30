"""Lethal: this time it's terminal"""

from dataclasses import dataclass
from typing import TypeVar, Generic
from blessed import Terminal


@dataclass
class Pos:
    """x,y coord pair"""

    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name

    def add(self, pos: "Pos") -> "Pos":
        """Compute a new Pos by adding the x,y coords"""
        return Pos(self.x + pos.x, self.y + pos.y)


@dataclass
class Output:
    """For drawing to the screen, passed the Module.draw"""

    term: Terminal

    def print(self, thing: str) -> None:
        """Print a string in the view"""
        print(thing, end="")

    # pylint: disable=invalid-name
    def print_at(self, pos: Pos, thing: str) -> None:
        """Print a string in the view at a specific location"""
        print(self.term.move_xy(pos.x, pos.y) + thing)


@dataclass
class Input:
    """User input passed to Module.update"""

    keys: list[str]

    @classmethod
    def key_to_str(cls, key):
        """Convert keystroke objects to strings"""
        if key.is_sequence:
            return key.name
        return str(key)


T = TypeVar("T")


class Module(Generic[T]):
    """Module baseclass"""

    def create(self) -> T:
        """Create a new instance of this module's state"""
        raise Exception("implement me")

    def update(self, state: T, user_input: Input, delta: float) -> T:
        """Computes the next state based in inputs"""
        return state

    def draw(self, state: T, output: Output):
        """Computes the next state based in inputs"""

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

    def __eq__(self, other: "Pos") -> bool:
        return self.x == other.x and self.y == other.y


class OutputOffsetMgr:
    """Lets you do:  with output.offset(Pos(1,1)): ..."""

    output: "Output"
    pos: Pos

    def __init__(self, output: "Output", pos: Pos):
        self.output = output
        self.pos = pos

    def __enter__(self) -> Pos:
        self.output.push(self.pos)
        return self.pos

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.output.pop()


class Output:
    """For drawing to the screen, passed the Module.draw"""

    term: Terminal
    offset_stack: list[Pos]

    def __init__(self, term: Terminal):
        self.term = term
        self.offset_stack = []

    def push(self, pos: Pos) -> Pos:
        """Push an offset onto the stack"""
        self.offset_stack.append(pos)
        return pos

    def pop(self) -> Pos:
        """Pop an offset from the stack"""
        pos = self.offset_stack.pop()
        return pos

    def get_offset(self) -> Pos:
        """Return the current offset, or Pos(0,0)"""
        if len(self.offset_stack) > 0:
            return self.offset_stack[-1]
        return Pos(0, 0)

    def clear_offset(self) -> None:
        self.offset_stack = []

    def offset(self, pos: Pos) -> OutputOffsetMgr:
        return OutputOffsetMgr(self, pos)

    def print(self, thing: str) -> None:
        """Print a string in the view"""
        print(thing, end="")

    # pylint: disable=invalid-name
    def print_at(self, pos: Pos, thing: str) -> None:
        """Print a string in the view at a specific location"""
        rel = self.get_offset().add(pos)
        print(self.term.move_xy(rel.x, rel.y) + thing)


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

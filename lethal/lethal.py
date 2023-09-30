"""Lethal: this time it's terminal"""

from dataclasses import dataclass
from typing import TypeVar, Generic
from blessed import Terminal

T = TypeVar("T")


@dataclass
class Output:
    """For drawing to the screen, passed the Module.draw"""

    term: Terminal


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

"""Lethal: this time it's terminal"""

from typing import TypeVar, Generic

from .output import Output
from .input import Input


T = TypeVar("T")


class Module(Generic[T]):
    """Module baseclass"""

    def create(self) -> T:
        """Create a new instance of this module's state"""
        raise NotImplementedError("Modules need to implement create()")

    def update(self, state: T, user_input: Input, delta: float) -> T:
        """Computes the next state based in inputs"""
        return state

    def draw(self, state: T, output: Output):
        """Computes the next state based in inputs"""

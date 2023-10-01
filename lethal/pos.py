"""Pos"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Pos:
    """x,y coord pair"""

    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name

    def add(self, pos: "Pos") -> "Pos":
        """Compute a new Pos by adding the x,y coords"""
        return Pos(self.x + pos.x, self.y + pos.y)

    def copy_from(self, pos) -> "Pos":
        """Update this pos's values from the givn pos"""
        self.x = pos.x
        self.y = pos.y
        return self

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Pos) and self.x == other.x and self.y == other.y

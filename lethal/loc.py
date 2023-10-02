"""Basic ECS component for x,y coords.
We're defining one in the base library because our Output implemenation likes Pos
so we're building-in some conveniences.
"""

from .ecs import Component
from .pos import Pos


class Loc(Component):
    """2D location Component"""

    x: int
    y: int

    def add(self, other: "Loc") -> "Loc":
        """Move this Loc by other.x,other.y, return this Loc"""
        self.x += other.x
        self.y += other.y
        return self

    def to_pos(self) -> Pos:
        """Generate a Pos based on this x,y"""
        return Pos(self.x, self.y)

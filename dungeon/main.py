"""Dungeon game: main"""

import sys

from lethal import Driver

from .dungeon_module import DungeonModule
from .dungeon_state import DungeonState


class DungeonDriver(Driver[DungeonModule, DungeonState]):
    """The driver"""


if __name__ == "__main__":
    DungeonDriver(DungeonModule()).loop()
    sys.exit(0)

from dataclasses import dataclass

from lethal import Estore


@dataclass
class DungeonState:
    """State of the D"""

    estore: Estore
    my_player_id: str
    messages: list[str]

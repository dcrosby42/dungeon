from dataclasses import dataclass

from lethal.ecs import EntityStore


@dataclass
class DungeonState:
    """State of the D"""

    estore: EntityStore
    my_player_id: str
    messages: list[str]

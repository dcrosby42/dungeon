from pydantic.dataclasses import dataclass

from lethal import SideEffect


class MsgSideEffect(SideEffect):
    """Send a log msg to the ui"""

    text: str


@dataclass
class InputEvent:
    """Event base class"""


@dataclass
class ControllerEvent(InputEvent):
    """Player input event"""

    player_id: str
    action_name: str


@dataclass
class DungeonInput:
    """Input suitable for the dungeon ecs systems"""

    events: list[InputEvent]

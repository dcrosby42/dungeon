from lethal import System, SideEffect
from pydantic.dataclasses import dataclass


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
class TimeEvent(InputEvent):
    """Indicates time passage"""

    player_id: str
    action_name: str
    delta: float


@dataclass
class DungeonInput:
    """Input suitable for the dungeon ecs systems"""

    events: list[InputEvent]


class DungeonSystem(System[DungeonInput]):
    """Extended ECS system adds helpers for our particular game setup"""

    def _message(self, text) -> SideEffect:
        return self.add_side_effect(MsgSideEffect(text=text))

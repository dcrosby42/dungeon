from pydantic import Field
from dungeon.dungeon_comps import Player
from dungeon.dungeon_system import DungeonInput, ControllerEvent

from lethal import Component
from lethal.ecs import SideEffect
from lethal.ecs2 import Estore


class Controller(Component):
    """Controller state"""

    up: bool | None = Field(default=False)
    down: bool | None = Field(default=False)
    left: bool | None = Field(default=False)
    right: bool | None = Field(default=False)
    take: bool | None = Field(default=False)
    drop: bool | None = Field(default=False)
    action: bool | None = Field(default=False)

    def clear(self) -> None:
        """Set all attrs to False"""
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.take = False
        self.drop = False
        self.action = False


def controller_system(estore: Estore, inp: DungeonInput) -> list[SideEffect]:
    """
    Applies incoming ControllerEvents to Controller comps based on player id
    """
    for controller in estore.by_type(Controller):
        controller.clear()

    for player, controller in estore.by_types2(Player, Controller):
        this_player_id = player.player_id
        for event in inp.events:
            match event:
                case ControllerEvent(player_id, action_name) if player_id == this_player_id:
                    setattr(controller, action_name, True)
    return []

from dataclasses import fields
from pydantic import Field
from pydantic.dataclasses import dataclass
from dungeon.dungeon_comps import Player
from dungeon.dungeon_system import DungeonSystem, ControllerEvent

from lethal import Component


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


class ControllerSystem(DungeonSystem):
    """Applies incoming ControllerEvents to Controller comps based on player id"""

    def update(self) -> None:
        for e in self.estore.select(Controller):
            e[Controller].clear()
            print(f"Controller: {e[Controller]}")
        for ent in self.estore.select(Player, Controller):
            con = ent[Controller]
            # con.clear()
            this_player_id = ent[Player].player_id
            for event in self.system_input.events:
                match event:
                    case ControllerEvent(player_id, action_name) if player_id == this_player_id:
                        setattr(con, action_name, True)

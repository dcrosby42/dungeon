"""Dungeon Module using ECS"""
# from typing import Any, Optional


from typing import Callable
from lethal import Input, Loc, Module, Output
from lethal.ecs import SideEffect
from lethal.ecs2 import Estore

from .controller_system import Controller, controller_system
from .dungeon_comps import *
from .dungeon_comps import ROOM_HEIGHT, ROOM_WIDTH
from .dungeon_renderer import DungeonRenderer
from .dungeon_state import DungeonState
from .dungeon_system import ControllerEvent, DungeonInput, MsgSideEffect
from .player_system import player_system


KEY_MAP = {
    "KEY_RIGHT": "right",
    "KEY_LEFT": "left",
    "KEY_UP": "up",
    "KEY_DOWN": "down",
    " ": "action",
    "t": "take",
    "T": "drop",
}

DungeonSys = Callable[[Estore, DungeonInput], list[SideEffect]]

DUNGEON_SYSTEMS: list[DungeonSys] = [
    controller_system,
    player_system,
]


class DungeonModule(Module[DungeonState]):
    """The Dungeon"""

    def create(self) -> DungeonState:
        estore = self._init_estore()

        messages = [
            "Move with arrow keys.  t=take, T=drop",
            "Welcome to the Dungeon!",
        ]

        return DungeonState(estore=estore, my_player_id="player1", messages=messages)

    def update(self, state: DungeonState, user_input: Input) -> DungeonState:
        player_id = state.my_player_id

        #
        # Map player input actions
        #
        dungeon_input = DungeonInput(events=[])
        dungeon_input.events = []
        for key in user_input.keys:
            action_name = KEY_MAP.get(key)
            if action_name:
                dungeon_input.events.append(ControllerEvent(player_id, action_name))

        #
        # System chain
        #
        side_effects: list[SideEffect] = []
        for system in DUNGEON_SYSTEMS:
            sfx = system(state.estore, dungeon_input)
            side_effects.extend(sfx)

        #
        # Side effects
        #
        for se in side_effects:
            match se:
                case MsgSideEffect(text=msg):
                    state.messages.append(msg)

        return state

    def draw(self, state: DungeonState, output: Output):
        DungeonRenderer(state, output).draw()

    def _init_estore(self):
        estore = Estore()

        estore.create_entity(
            Player(player_id="player1"),
            Health(max=10, current=10),
            Controller(name="controller1"),
            Text(text="O"),
            Loc(x=70, y=10),
            Drawable(layer=10),
            Room(room_id="room1"),
        )

        self._add_room1(estore)
        self._add_room2(estore)

        return estore

    def _add_room1(self, estore):
        estore.create_entity(
            Item(cat="gold", name="Gold Piece", value="10"),
            Text(text="$"),
            Room(room_id="room1"),
            Loc(x=12, y=4),
            Drawable(),
        )

        estore.create_entity(
            Item(cat="gold", name="Dubloon", value="10"),
            Room(room_id="room1"),
            Loc(x=30, y=8),
            Text(text="$"),
            Drawable(),
        )

        estore.create_entity(
            Item(cat="sword", name="Sword", value="30"),
            Room(room_id="room1"),
            Loc(x=32, y=3),
            Text(text="/"),
            Drawable(),
        )

        estore.create_entity(
            Place(name="Fountain", blocked=True),
            Room(room_id="room1"),
            Loc(x=10, y=0),
            Text(text="*"),
            Drawable(),
        )

        estore.create_entity(
            Door(door_id="door1", to_door_id="door2"),
            Place(name="Door"),
            Room(room_id="room1"),
            Loc(x=ROOM_WIDTH - 5, y=ROOM_HEIGHT - 1),
            Text(text="#"),
            Drawable(),
        )

        estore.create_entity(
            Mob(cat="enemy", name="Slime"),
            Health(max=3, current=3),
            Text(text="@"),
            Room(room_id="room1"),
            Loc(x=ROOM_WIDTH - 6, y=ROOM_HEIGHT - 3),
            Drawable(),
        )

        estore.create_entity(
            Mob(cat="enemy", name="Slime"),
            Health(max=3, current=3),
            Text(text="@"),
            Room(room_id="room1"),
            Loc(x=10, y=4),
            Drawable(),
        )

    def _add_room2(self, estore):
        estore.create_entity(
            Item(cat="gold", name="Gold Piece", value="10"),
            Loc(x=20, y=10),
            Text(text="$"),
            Room(room_id="room2"),
            Drawable(),
        )

        estore.create_entity(
            Place(name="Door"),
            Door(door_id="door2", to_door_id="door1"),
            Room(room_id="room2"),
            Loc(x=4, y=0),
            Text(text="#"),
            Drawable(),
        )

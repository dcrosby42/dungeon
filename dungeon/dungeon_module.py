"""Dungeon Module using ECS"""
# from typing import Any, Optional


from lethal import EntityStore, Input, Loc, Module, Output

from .controller_system import Controller, ControllerSystem
from .dungeon_comps import *
from .dungeon_comps import ROOM_HEIGHT, ROOM_WIDTH
from .dungeon_renderer import DungeonRenderer
from .dungeon_state import DungeonState
from .dungeon_system import MsgSideEffect
from .player_system import PlayerSystem


class DungeonModule(Module[DungeonState]):
    """The Dungeon"""

    def create(self) -> DungeonState:
        estore = self._init_entity_store()

        messages = [
            "Move with arrow keys.  t=take, T=drop",
            "Welcome to the Dungeon!",
        ]

        return DungeonState(estore=estore, my_player_id="player1", messages=messages)

    def update(
        self, state: DungeonState, user_input: Input, delta: float
    ) -> DungeonState:
        #
        # System chain
        #
        side_effects = []
        systems = [
            ControllerSystem,
            PlayerSystem,
        ]
        for new_system in systems:
            s = new_system(estore=state.estore, user_input=user_input)
            s.update()
            side_effects.extend(s.side_effects)

        #
        # Side effects
        #
        for se in side_effects:
            if isinstance(se, MsgSideEffect):
                state.messages.append(se.text)

        return state

    def draw(self, state: DungeonState, output: Output):
        DungeonRenderer(state, output).draw()

    def _init_entity_store(self):
        estore = EntityStore()

        player = estore.create_entity()
        player.add(Player(player_id="player1"))
        player.add(Health(max=10, current=10))
        player.add(Controller(name="controller1"))
        player.add(Text(text="O"))
        player.add(Loc(x=70, y=10))
        player.add(Drawable(layer=10))
        player.add(Room(room_id="room1"))

        self._add_room1(estore)
        self._add_room2(estore)
        return estore

    def _add_room1(self, estore):
        gold1 = estore.create_entity()
        gold1.add(Item(cat="gold", name="Gold Piece", value="10"))
        gold1.add(Loc(x=12, y=4))
        gold1.add(Text(text="$"))

        gold2 = estore.create_entity()
        gold2.add(Item(cat="gold", name="Dubloon", value="10"))
        gold2.add(Loc(x=30, y=8))
        gold2.add(Text(text="$"))

        sword = estore.create_entity()
        sword.add(Item(cat="sword", name="Sword", value="30"))
        sword.add(Loc(x=32, y=3))
        sword.add(Text(text="/"))

        fountain = estore.create_entity()
        fountain.add(Place(name="Fountain", blocked=True))
        fountain.add(Loc(x=10, y=0))
        fountain.add(Text(text="*"))

        door = estore.create_entity()
        door.add(Door(door_id="door1", to_door_id="door2"))
        door.add(Place(name="Door"))
        door.add(Loc(x=ROOM_WIDTH - 5, y=ROOM_HEIGHT - 1))
        door.add(Text(text="#"))

        slime1 = estore.create_entity()
        slime1.add(Mob(cat="enemy", name="Slime"))
        slime1.add(Health(max=3, current=3))
        slime1.add(Text(text="@"))
        slime1.add(Loc(x=ROOM_WIDTH - 6, y=ROOM_HEIGHT - 3))
        # TODO: Drops

        slime2 = estore.create_entity()
        slime2.add(Mob(cat="enemy", name="Slime"))
        slime2.add(Health(max=3, current=3))
        slime2.add(Text(text="@"))
        slime2.add(Loc(x=10, y=4))
        # TODO: Drops

        for e in estore.select():
            e.add(Room(room_id="room1"))
            e.add(Drawable())

    def _add_room2(self, estore):
        gold1 = estore.create_entity()
        gold1.add(Item(cat="gold", name="Gold Piece", value="10"))
        gold1.add(Loc(x=20, y=10))
        gold1.add(Text(text="$"))
        gold1.add(Room(room_id="room2"))
        gold1.add(Drawable())

        door = estore.create_entity()
        door.add(Place(name="Door"))
        door.add(Door(door_id="door2", to_door_id="door1"))
        door.add(Room(room_id="room2"))
        door.add(Loc(x=4, y=0))
        door.add(Text(text="#"))
        door.add(Drawable())

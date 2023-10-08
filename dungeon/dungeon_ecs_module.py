"""Dungeon Module using ECS"""
# from typing import Any, Optional
from dataclasses import dataclass

from pydantic import BaseModel, Field

from lethal import (
    Component,
    EntityStore,
    Entity,
    Input,
    Loc,
    Module,
    Output,
    Pos,
    System,
    SideEffect,
)

from .controller import Controller, ControllerSystem


# import pdb

# @dataclass
# class Item:
#     """A thing you can take"""

#     pos: Pos
#     kind: str
#     name: str
#     view: str
#     value: int


# @dataclass
# class Obstacle:
#     """A thing you run into"""

#     pos: Pos
#     kind: str
#     name: str
#     view: str
#     is_blocker: bool
#     extras: dict[str, Any]


# @dataclass
# class Health:
#     """Health component"""

#     max_hp: int
#     current_hp: int

#     def is_alive(self) -> bool:
#         """Return True if health remaining"""
#         return self.current_hp > 0

#     def is_dead(self) -> bool:
#         """Return True if health depleted"""
#         return self.current_hp <= 0

#     def damage(self, points: int):
#         """Reduce HP"""
#         self.current_hp -= points

#     def heal(self, points: int):
#         """Increase HP up to max"""
#         self.current_hp += points
#         if self.current_hp > self.max_hp:
#             self.current_hp = self.max_hp


# @dataclass
# class Mob:
#     """A monster"""

#     pos: Pos
#     kind: str
#     name: str
#     view: str
#     health: Health
#     drops: list[Item]


# @dataclass
# class Player:
#     """The player"""

#     pos: Pos
#     items: list[Item]
#     health: Health


@dataclass
class DungeonState:
    """State of the D"""

    estore: EntityStore
    current_room_id: str
    messages: list[str]


ROOM_WIDTH = 80
ROOM_HEIGHT = 15


class Text(Component):
    """Drawable string"""

    text: str


class Drawable(Component):
    layer: int | None = Field(default=0)


class Item(Component):
    """A thing you can get"""

    cat: str
    name: str
    value: int


class Player(Component):
    """Indicates a player"""


MobCategory = str


class Mob(Component):
    """Indicates a non-player creature"""

    name: str
    cat: MobCategory


class Place(Component):
    """A place on the map"""

    name: str
    blocked: bool | None = Field(default=False)


class Health(Component):
    """Creature or player health"""

    max: int
    current: int


class Room(Component):
    """Relates an entity to a room"""

    room_id: str


class Door(Component):
    """Doors link to doors by id"""

    door_id: str
    to_door_id: str


class MsgSideEffect(SideEffect):
    """Send a log msg to the ui"""

    text: str


class RoomSideEffect(SideEffect):
    """Switching rooms"""

    to_room_id: str


class DungeonSystem(System):
    """Extended ECS system adds helpers for our particular game setup"""

    def _message(self, text) -> MsgSideEffect:
        return self.add_side_effect(MsgSideEffect(text=text))


class PlayerSystem(DungeonSystem):
    """Update Player(s)"""

    def update(self) -> None:
        for player_e in self.estore.select(Player, Controller, Room, Loc):
            room = player_e.get(Room)
            loc = player_e.get(Loc)
            con = player_e.get(Controller)

            loc_backup = loc.model_copy()
            self._move(loc, con)

            for other_e in self._entities_at_loc(room, loc):
                if other_e.has_any(Place):
                    place: Place = other_e.get(Place)
                    if place.blocked:
                        # undo move, emit message
                        loc.x = loc_backup.x
                        loc.y = loc_backup.y
                        self._message(f"Bonk! {place.name} blocks the way.")
                    elif con.action:
                        door: Door = other_e.get(Door)
                        if door:
                            dest_door = next(
                                (
                                    e
                                    for e in self.estore.select(Door)
                                    if e.get(Door).door_id == door.to_door_id
                                ),
                                None,
                            )
                            if dest_door:
                                dest_room = dest_door.get(Room).room_id
                                self._message(f"Opened door {door.door_id}")
                                player_e.get(Loc).x = dest_door.get(Loc).x
                                player_e.get(Loc).y = dest_door.get(Loc).y
                                player_e.get(Room).room_id = dest_room
                                self.add_side_effect(
                                    RoomSideEffect(to_room_id=dest_room)
                                )

                elif other_e.has_any(Item):
                    # TODO: Pickup items
                    # item_e = other_e.get(Item)
                    # item_e.remove(Drawable)
                    # item_e.add(Link(eid=player_e))
                    ...
                elif other_e.has_any(Mob):
                    # Mob encounter!

                    # prevent motion
                    loc.x = loc_backup.x
                    loc.y = loc_backup.y

                    self._attack_mob(player_e, other_e)

    def _attack_mob(self, player_e: Entity, mob_e: Entity):
        hit = True
        damage = 1
        if hit:
            mob_health = mob_e.get(Health)
            mob_health.current = max(mob_health.current - damage, 0)
            if mob_health.current <= 0:
                self.estore.destroy_entity(mob_e)
                self._message(f"{mob_e.get(Mob).name} defeated!")
            else:
                self._message(f"{mob_e.get(Mob).name} hit for {damage}")
        else:
            self._message(f"{mob_e.get(Mob).name} missed")

        # obst = self.obstacle_at(state, state.player.pos)
        # if obst:
        #     if obst.is_blocker:
        #         state.player.pos.copy_from(last_pos)
        #         state.messages.append(obst.name + " is blocking the way")
        #     elif do_action:
        #         if obst.kind == "door":
        #             # locked door?
        #             door = obst
        #             req_key = door.extras.get("locked")
        #             if req_key:
        #                 keys = [
        #                     item for item in state.player.items if item.kind == req_key
        #                 ]
        #                 if len(keys) > 0:
        #                     # We have a key! Use it to unlock the door
        #                     door_key = keys[0]
        #                     del door.extras["locked"]
        #                     door.view = "_"
        #                     state.player.items.remove(door_key)
        #                     state.messages.append(
        #                         f"Unlocked {door.name} with {door_key.name}"
        #                     )
        #             else:
        #                 # do door
        #                 state.messages.append(f"Opened door {door.name}")

        # # Mob encounter!
        # mob = self.mob_at(state, state.player.pos)
        # if mob and mob.health.is_alive():
        #     state.player.pos.copy_from(last_pos)
        #     state = self.player_attack_mob(state, mob)

    def _move(self, loc: Loc, con: Controller) -> None:
        if con.right:
            loc.x = min(loc.x + 1, ROOM_WIDTH - 1)
        if con.left:
            loc.x = max(loc.x - 1, 0)
        if con.up:
            loc.y = max(loc.y - 1, 0)
        if con.down:
            loc.y = min(loc.y + 1, ROOM_HEIGHT - 1)
        if con.take:
            pass
        if con.drop:
            pass

    def _entities_at_loc(self, room: Room, loc: Loc):
        def hitting(ent: Entity, room: Room, loc: Loc):
            if ent.eid != loc.eid:
                if ent.get(Room).room_id == room.room_id:
                    eloc = ent.get(Loc)
                    return eloc.x == loc.x and eloc.y == loc.y
            return False

        return [e for e in self.estore.select(Room, Loc) if hitting(e, room, loc)]


class DungeonModule(Module[DungeonState]):
    """The Dungeon"""

    def create(self) -> DungeonState:
        estore = self._init_entity_store()

        messages = [
            "Move with arrow keys.  t=take, T=drop",
            "Welcome to the Dungeon!",
        ]

        return DungeonState(estore=estore, current_room_id="room1", messages=messages)

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
            if isinstance(se, RoomSideEffect):
                state.current_room_id = se.to_room_id

        return state

    def draw(self, state: DungeonState, output: Output):
        self.draw_ui(state, output)

        with output.offset(Pos(1, 1)):  # offset to be within the UI borders
            for ent in sorted(
                state.estore.select(Drawable, Loc, Room),
                key=lambda e: e.get(Drawable).layer,
            ):
                # for ent in state.estore.select(Drawable, Loc, Room):
                if ent.get(Room).room_id == state.current_room_id:
                    output.print_at(ent.get(Loc).to_pos(), ent.get(Text).text)

    def draw_ui(self, state: DungeonState, output: Output):
        """render bound box and labels"""
        width = ROOM_WIDTH + 2
        height = ROOM_HEIGHT

        # messages
        output.print_at(
            Pos(0, height + 3),
            output.term.darkgray
            + "\n".join(list(reversed(state.messages))[0:5])
            + output.term.normal,
        )

        # for e in state.estore.select(Controller):
        #     con = e.get(Controller)
        #     output.print_at(
        #         Pos(0, height + 3), output.term.blue + repr(con) + output.term.normal
        #     )

        # bounds
        hbar = "+" + ("-" * (width - 2)) + "+"
        bounds = hbar + "\n"
        for y in range(0, height):
            bounds += "|" + (" " * (width - 2)) + "|\n"
        bounds += hbar
        output.print_at(Pos(0, 0), bounds)

        # status
        # with output.offset(Pos(0, height + 1)):
        #     item_str = ""
        #     item = self.last_item_at(state, state.player.pos)
        #     if item:
        #         item_str = f" {item.name} "
        #     obst_str = ""
        #     obst = self.obstacle_at(state, state.player.pos)
        #     if obst:
        #         obst_str = f" >> {obst.name} "
        #     output.print_at(
        #         Pos(2, 0),
        #         f"({state.player.pos.x},{state.player.pos.y}){item_str}{obst_str}",
        #     )

        # inventory
        # with output.offset(Pos(0, height + 2)):
        #     output.print_at(
        #         Pos(0, 0),
        #         f"{output.term.normal}Gear: {output.term.gold_on_black}{', '.join([i.name for i in state.player.items])}{output.term.normal}",
        #     )

    def _init_entity_store(self):
        estore = EntityStore()

        player = estore.create_entity()
        player.add(Player())
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

        # door = estore.create_entity()
        # door.add(Place(name="Door"))
        # door.add(Loc(x=ROOM_WIDTH - 5, y=ROOM_HEIGHT - 1))
        # door.add(Text(text="#"))
        # door.add(Room(name="room2"))

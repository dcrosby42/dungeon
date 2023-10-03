"""Dungeon Module using ECS"""
# from typing import Any, Optional
from dataclasses import dataclass

from pydantic import BaseModel, Field

from lethal import Component, EntityStore, Input, Loc, Module, Output, Pos

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
    messages: list[str]


ROOM_WIDTH = 80
ROOM_HEIGHT = 15


class Text(Component):
    """Drawable string"""

    text: str


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


class Controller(Component):
    """Controller state"""

    name: str
    up: bool | None = Field(default=False)
    down: bool | None = Field(default=False)
    left: bool | None = Field(default=False)
    right: bool | None = Field(default=False)
    take: bool | None = Field(default=False)
    drop: bool | None = Field(default=False)


class Place(Component):
    """A place on the map"""

    name: str
    blocked: bool | None = Field(default=False)


class Health(Component):
    """Creature or player health"""

    max: int
    current: int


class System(BaseModel):
    """ECS System base class"""

    estore: EntityStore
    user_input: Input

    # def __init__(self, estore: EntityStore, user_input: Input):
    #     self.estore = estore
    #     self.user_input = user_input

    def update(self) -> None:
        """No-op"""
        return None


class ControllerSystem(System):
    """Updates Controller components based on user input"""

    def update(self) -> None:
        for ent in self.estore.select(Controller):
            con = ent.get(Controller)
            if con.name == "controller1":
                self._apply_input(con)

    def _apply_input(self, con: Controller):
        # map keys to controller attr names
        key_map = {
            "KEY_RIGHT": "right",
            "KEY_LEFT": "left",
            "KEY_UP": "up",
            "KEY_DOWN": "down",
            " ": "action",
            "t": "take",
            "T": "drop",
        }
        # Clear controller state:
        for _, attr in key_map.items():
            setattr(con, attr, False)

        # Update controller state::
        for key in self.user_input.keys:
            attr = key_map.get(key)
            if attr:
                setattr(con, attr, True)


class PlayerSystem(System):
    """Update Player(s)"""

    def update(self) -> None:
        for e in self.estore.select(Player, Controller, Loc):
            con = e.get(Controller)
            # p = e.get(Player)
            loc = e.get(Loc)
            if con.right:
                loc.x += 1
            if con.left:
                loc.x -= 1
            if con.up:
                loc.y -= 1
            if con.down:
                loc.y += 1
            if con.take:
                pass
            if con.drop:
                pass

        #     elif key == "t":
        #         # player takes item
        #         item = self.last_item_at(state, state.player.pos)
        #         if item:
        #             state.items.remove(item)
        #             state.player.items.append(item)
        #             state.messages.append("You got " + item.name)
        #     elif key == "T":
        #         # player drops item
        #         if len(state.player.items) > 0:
        #             item = state.player.items.pop()
        #             item.pos.copy_from(state.player.pos)
        #             state.items.append(item)
        #             state.messages.append("You dropped " + item.name)=

        # for key in user_input.keys:
        #     # Movement:
        #     last_pos = Pos(0, 0).copy_from(state.player.pos)
        #     if key == "KEY_RIGHT":
        #         state.player.pos.x += 1
        #     elif key == "KEY_LEFT":
        #         state.player.pos.x -= 1
        #     elif key == "KEY_UP":
        #         state.player.pos.y -= 1
        #     elif key == "KEY_DOWN":
        #         state.player.pos.y += 1
        #     elif key == " ":
        #         do_action = True
        #     elif key == "t":
        #         # player takes item
        #         item = self.last_item_at(state, state.player.pos)
        #         if item:
        #             state.items.remove(item)
        #             state.player.items.append(item)
        #             state.messages.append("You got " + item.name)
        #     elif key == "T":
        #         # player drops item
        #         if len(state.player.items) > 0:
        #             item = state.player.items.pop()
        #             item.pos.copy_from(state.player.pos)
        #             state.items.append(item)
        #             state.messages.append("You dropped " + item.name)=


class DungeonModule(Module[DungeonState]):
    """The Dungeon"""

    def create(self) -> DungeonState:
        estore = EntityStore()

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
        door.add(Place(name="Door"))
        door.add(Loc(x=ROOM_WIDTH - 5, y=ROOM_HEIGHT - 1))
        door.add(Text(text="#"))

        player = estore.create_entity()
        player.add(Player())
        player.add(Health(max=10, current=10))
        player.add(Controller(name="player1"))
        player.add(Text(text="O"))
        player.add(Loc(x=0, y=0))

        slime1 = estore.create_entity()
        slime1.add(Mob(cat="enemy", name="Slime"))
        slime1.add(Health(max=3, current=3))
        slime1.add(Text(text="@"))
        slime1.add(Loc(x=ROOM_WIDTH - 6, y=ROOM_HEIGHT - 3))
        # TODO: Drops

        slime2 = estore.create_entity()
        slime2.add(Mob(cat="enemy", name="Slime"))
        slime2.add(Health(max=3, current=1))
        slime2.add(Text(text="@"))
        slime2.add(Loc(x=10, y=4))
        # TODO: Drops

        messages = [
            "Move with arrow keys.  t=take, T=drop",
            "Welcome to the Dungeon!",
        ]
        return DungeonState(estore, messages)

    def update(
        self, state: DungeonState, user_input: Input, delta: float
    ) -> DungeonState:
        ControllerSystem(state.estore).update(user_input)
        PlayerSystem(state.estore).update(user_input)

        # do_action = False

        # for key in user_input.keys:
        #     # Movement:
        #     last_pos = Pos(0, 0).copy_from(state.player.pos)
        #     if key == "KEY_RIGHT":
        #         state.player.pos.x += 1
        #     elif key == "KEY_LEFT":
        #         state.player.pos.x -= 1
        #     elif key == "KEY_UP":
        #         state.player.pos.y -= 1
        #     elif key == "KEY_DOWN":
        #         state.player.pos.y += 1
        #     elif key == " ":
        #         do_action = True
        #     elif key == "t":
        #         # player takes item
        #         item = self.last_item_at(state, state.player.pos)
        #         if item:
        #             state.items.remove(item)
        #             state.player.items.append(item)
        #             state.messages.append("You got " + item.name)
        #     elif key == "T":
        #         # player drops item
        #         if len(state.player.items) > 0:
        #             item = state.player.items.pop()
        #             item.pos.copy_from(state.player.pos)
        #             state.items.append(item)
        #             state.messages.append("You dropped " + item.name)

        # # obstruction?
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

        # # Apply constraints
        # if state.player.pos.x < 0:
        #     state.player.pos.x = 0
        # if state.player.pos.x >= MAX_WIDTH:
        #     state.player.pos.x = MAX_WIDTH - 1
        # if state.player.pos.y < 0:
        #     state.player.pos.y = 0
        # if state.player.pos.y >= MAX_HEIGHT:
        #     state.player.pos.y = MAX_HEIGHT - 1

        return state

    # def last_item_at(self, state: DungeonState, pos: Pos) -> Optional[Item]:
    #     """Return the 'most recent' item at pos, or None"""
    #     for item in reversed(state.items):
    #         if item.pos == pos:
    #             return item
    #     return None

    # def obstacle_at(self, state: DungeonState, pos: Pos) -> Optional[Obstacle]:
    #     """Return the obstacle at the pos"""
    #     for obst in state.obstacles:
    #         if obst.pos == pos:
    #             return obst
    #     return None

    # def mob_at(self, state: DungeonState, pos: Pos) -> Optional[Mob]:
    #     """Return the mob at the pos"""
    #     for mob in state.mobs:
    #         if mob.pos == pos:
    #             return mob
    #     return None

    # def player_attack_mob(self, state: DungeonState, mob: Mob) -> DungeonState:
    #     """Try to attack the mob"""
    #     swords = [item for item in state.player.items if item.kind == "sword"]
    #     if len(swords) > 0:
    #         sword = swords[0]
    #         dmg = 1
    #         mob.health.damage(dmg)
    #         msg = f"Hit {mob.name} for {dmg} ({sword.name})"
    #         if mob.health.is_dead():
    #             state.mobs.remove(mob)
    #             for item in mob.drops:
    #                 item.pos.copy_from(mob.pos)
    #                 mob.drops.remove(item)
    #                 state.items.append(item)
    #             msg += f" -- {mob.name} is defeated!"
    #         state.messages.append(msg)
    #     else:
    #         state.messages.append(
    #             "OUCH! A " + mob.name + "! Try getting the sword first!"
    #         )
    #     return state

    def draw(self, state: DungeonState, output: Output):
        self.draw_ui(state, output)

        with output.offset(Pos(1, 1)):
            for ent in state.estore.select(Text, Loc):
                output.print_at(ent.get(Loc).to_pos(), ent.get(Text).text)
            # state.messages.append(f"Text: {ent.get(Text).text} {ent.get(Loc).to_pos()}")
            # pos = ent.get(Loc).to_pos()
            # text = ent.get(Text).text
            # output.print_at(pos, text)

        # with output.offset(Pos(1, 1)):
        #     self.draw_obstacles(state, output)
        #     self.draw_items(state, output)
        #     self.draw_mobs(state, output)
        #     self.draw_player(state, output)

    # def draw_items(self, state: DungeonState, output: Output):
    #     for item in state.items:
    #         output.print_at(item.pos, item.view)

    # def draw_obstacles(self, state: DungeonState, output: Output):
    #     for obst in state.obstacles:
    #         output.print_at(obst.pos, obst.view)

    # def draw_mobs(self, state: DungeonState, output: Output):
    #     for mob in state.mobs:
    #         output.print_at(mob.pos, mob.view)

    # def draw_player(self, state: DungeonState, output: Output):
    #     output.print_at(state.player.pos, "O")

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

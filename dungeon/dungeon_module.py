"""Dungeon Module"""
from dataclasses import dataclass
from typing import Optional, Any

from lethal import Input, Module, Output, Pos


@dataclass
class Item:
    """A thing you can take"""

    pos: Pos
    kind: str
    name: str
    view: str
    value: int


@dataclass
class Obstacle:
    """A thing you run into"""

    pos: Pos
    kind: str
    name: str
    view: str
    is_blocker: bool
    extras: dict[str, Any]


@dataclass
class Health:
    """Health component"""

    max_hp: int
    current_hp: int

    def is_alive(self) -> bool:
        """Return True if health remaining"""
        return self.current_hp > 0

    def is_dead(self) -> bool:
        """Return True if health depleted"""
        return self.current_hp <= 0

    def damage(self, points: int):
        """Reduce HP"""
        self.current_hp -= points

    def heal(self, points: int):
        """Increase HP up to max"""
        self.current_hp += points
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp


@dataclass
class Mob:
    """A monster"""

    pos: Pos
    kind: str
    name: str
    view: str
    health: Health
    drops: list[Item]


@dataclass
class Player:
    """The player"""

    pos: Pos
    items: list[Item]
    health: Health


@dataclass
class DungeonState:
    """State of the D"""

    player: Player
    items: list[Item]
    obstacles: list[Obstacle]
    mobs: list[Mob]
    messages: list[str]


MAX_WIDTH = 80
MAX_HEIGHT = 15


class DungeonModule(Module[DungeonState]):
    """The Dungeon"""

    def create(self) -> DungeonState:
        items = [
            Item(Pos(12, 4), "gold", "Gold Piece", "$", 10),
            Item(Pos(30, 8), "gold", "Dubloon", "$", 10),
            Item(Pos(32, 3), "sword", "Bronze Sword", "/", 30),
        ]
        obst = [
            Obstacle(
                Pos(MAX_WIDTH - 5, MAX_HEIGHT - 1),
                "door",
                "Door",
                "#",
                False,
                {"locked": "stone_key"},
            ),
            Obstacle(Pos(10, 0), "fountain", "Fountain", "*", True, {}),
        ]
        mobs = [
            Mob(
                pos=Pos(MAX_WIDTH - 6, MAX_HEIGHT - 3),
                kind="slime",
                name="Slime",
                view="x",
                health=Health(3, 3),
                drops=[
                    Item(Pos(0, 0), "gold", "Gold nug", "$", 1),
                ],
            ),
            Mob(
                pos=Pos(10, 4),
                kind="slime",
                name="Slime",
                view="x",
                health=Health(3, 1),
                drops=[
                    Item(Pos(0, 0), "stone_key", "Stone Key", "%", 50),
                ],
            ),
        ]
        messages = [
            "Move with arrow keys.  t=take, T=drop",
            "Welcome to the Dungeon!",
        ]
        return DungeonState(
            Player(Pos(0, 0), [], Health(10, 10)), items, obst, mobs, messages
        )

    def update(
        self, state: DungeonState, user_input: Input, delta: float
    ) -> DungeonState:
        do_action = False
        for key in user_input.keys:
            # Movement:
            last_pos = Pos(0, 0).copy_from(state.player.pos)
            if key == "KEY_RIGHT":
                state.player.pos.x += 1
            elif key == "KEY_LEFT":
                state.player.pos.x -= 1
            elif key == "KEY_UP":
                state.player.pos.y -= 1
            elif key == "KEY_DOWN":
                state.player.pos.y += 1
            elif key == " ":
                do_action = True
            elif key == "t":
                # player takes item
                item = self.last_item_at(state, state.player.pos)
                if item:
                    state.items.remove(item)
                    state.player.items.append(item)
                    state.messages.append("You got " + item.name)
            elif key == "T":
                # player drops item
                if len(state.player.items) > 0:
                    item = state.player.items.pop()
                    item.pos.copy_from(state.player.pos)
                    state.items.append(item)
                    state.messages.append("You dropped " + item.name)

        # obstruction?
        obst = self.obstacle_at(state, state.player.pos)
        if obst:
            if obst.is_blocker:
                state.player.pos.copy_from(last_pos)
                state.messages.append(obst.name + " is blocking the way")
            elif do_action:
                if obst.kind == "door":
                    # locked door?
                    door = obst
                    req_key = door.extras.get("locked")
                    if req_key:
                        keys = [
                            item for item in state.player.items if item.kind == req_key
                        ]
                        if len(keys) > 0:
                            # We have a key! Use it to unlock the door
                            door_key = keys[0]
                            del door.extras["locked"]
                            door.view = "_"
                            state.player.items.remove(door_key)
                            state.messages.append(
                                f"Unlocked {door.name} with {door_key.name}"
                            )
                    else:
                        # do door
                        state.messages.append(f"Opened door {door.name}")

        # Mob encounter!
        mob = self.mob_at(state, state.player.pos)
        if mob and mob.health.is_alive():
            state.player.pos.copy_from(last_pos)
            state = self.player_attack_mob(state, mob)

        # Apply constraints
        if state.player.pos.x < 0:
            state.player.pos.x = 0
        if state.player.pos.x >= MAX_WIDTH:
            state.player.pos.x = MAX_WIDTH - 1
        if state.player.pos.y < 0:
            state.player.pos.y = 0
        if state.player.pos.y >= MAX_HEIGHT:
            state.player.pos.y = MAX_HEIGHT - 1

        return state

    def last_item_at(self, state: DungeonState, pos: Pos) -> Optional[Item]:
        """Return the 'most recent' item at pos, or None"""
        for item in reversed(state.items):
            if item.pos == pos:
                return item
        return None

    def obstacle_at(self, state: DungeonState, pos: Pos) -> Optional[Obstacle]:
        """Return the obstacle at the pos"""
        for obst in state.obstacles:
            if obst.pos == pos:
                return obst
        return None

    def mob_at(self, state: DungeonState, pos: Pos) -> Optional[Mob]:
        """Return the mob at the pos"""
        for mob in state.mobs:
            if mob.pos == pos:
                return mob
        return None

    def player_attack_mob(self, state: DungeonState, mob: Mob) -> DungeonState:
        """Try to attack the mob"""
        swords = [item for item in state.player.items if item.kind == "sword"]
        if len(swords) > 0:
            sword = swords[0]
            dmg = 1
            mob.health.damage(dmg)
            msg = f"Hit {mob.name} for {dmg} ({sword.name})"
            if mob.health.is_dead():
                state.mobs.remove(mob)
                for item in mob.drops:
                    item.pos.copy_from(mob.pos)
                    mob.drops.remove(item)
                    state.items.append(item)
                msg += f" -- {mob.name} is defeated!"
            state.messages.append(msg)
        else:
            state.messages.append(
                "OUCH! A " + mob.name + "! Try getting the sword first!"
            )
        return state

    def draw(self, state: DungeonState, output: Output):
        self.draw_ui(state, output)
        with output.offset(Pos(1, 1)):
            self.draw_obstacles(state, output)
            self.draw_items(state, output)
            self.draw_mobs(state, output)
            self.draw_player(state, output)

    def draw_items(self, state: DungeonState, output: Output):
        for item in state.items:
            output.print_at(item.pos, item.view)

    def draw_obstacles(self, state: DungeonState, output: Output):
        for obst in state.obstacles:
            output.print_at(obst.pos, obst.view)

    def draw_mobs(self, state: DungeonState, output: Output):
        for mob in state.mobs:
            output.print_at(mob.pos, mob.view)

    def draw_player(self, state: DungeonState, output: Output):
        output.print_at(state.player.pos, "O")

    def draw_ui(self, state: DungeonState, output: Output):
        """render bound box and labels"""
        width = MAX_WIDTH + 2
        height = MAX_HEIGHT

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
        with output.offset(Pos(0, height + 1)):
            item_str = ""
            item = self.last_item_at(state, state.player.pos)
            if item:
                item_str = f" {item.name} "
            obst_str = ""
            obst = self.obstacle_at(state, state.player.pos)
            if obst:
                obst_str = f" >> {obst.name} "
            output.print_at(
                Pos(2, 0),
                f"({state.player.pos.x},{state.player.pos.y}){item_str}{obst_str}",
            )

        # inventory
        with output.offset(Pos(0, height + 2)):
            output.print_at(
                Pos(0, 0),
                f"{output.term.normal}Gear: {output.term.gold_on_black}{', '.join([i.name for i in state.player.items])}{output.term.normal}",
            )

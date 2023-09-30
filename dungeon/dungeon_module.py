"""Dungeon Module"""
from dataclasses import dataclass
from typing import Optional

from lethal.lethal import Input, Module, Output, Pos


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


@dataclass
class Player:
    """The player"""

    pos: Pos
    items: list[Item]


@dataclass
class DungeonState:
    """State of the D"""

    player: Player
    items: list[Item]
    obstacles: list[Obstacle]
    messages: list[str]


MAX_WIDTH = 40
MAX_HEIGHT = 10


class DungeonModule(Module[DungeonState]):
    """The Dungeon"""

    def create(self) -> DungeonState:
        items = [
            Item(Pos(12, 4), "gold", "Gold Piece", "$", 10),
            Item(Pos(30, 8), "gold", "Dubloon", "$", 10),
            Item(Pos(32, 3), "sword", "Bronze Sword", "/", 30),
        ]
        obst = [
            Obstacle(Pos(MAX_WIDTH - 5, MAX_HEIGHT - 1), "door", "Door", "#", False),
            Obstacle(Pos(10, 0), "fountain", "Fountain", "*", True),
        ]
        messages = ["Welcome to the Dungeon!"]
        return DungeonState(Player(Pos(0, 0), []), items, obst, messages)

    def update(
        self, state: DungeonState, user_input: Input, delta: float
    ) -> DungeonState:
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
        if obst and obst.is_blocker:
            state.player.pos.copy_from(last_pos)
            state.messages.append(obst.name + " is blocking the way")

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

    def draw(self, state: DungeonState, output: Output):
        self.draw_ui(state, output)
        with output.offset(Pos(1, 1)):
            self.draw_obstacles(state, output)
            self.draw_items(state, output)
            self.draw_player(state, output)

    def draw_items(self, state: DungeonState, output: Output):
        for item in state.items:
            output.print_at(item.pos, item.view)

    def draw_obstacles(self, state: DungeonState, output: Output):
        for obst in state.obstacles:
            output.print_at(obst.pos, obst.view)

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

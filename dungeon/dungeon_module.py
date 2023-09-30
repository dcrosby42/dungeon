"""Dungeon Module"""
from dataclasses import dataclass
from typing import Optional

from lethal.lethal import Input, Module, Output, Pos


@dataclass
class Item:
    """A thing"""

    pos: Pos
    kind: str
    name: str
    view: str
    value: int


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
        return DungeonState(Player(Pos(0, 0), []), items)

    def update(
        self, state: DungeonState, user_input: Input, delta: float
    ) -> DungeonState:
        for key in user_input.keys:
            # Movement:
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
                item = self.item_at(state, state.player.pos)
                if item:
                    state.items.remove(item)
                    state.player.items.append(item)
            elif key == "T":
                # player drops item
                if len(state.player.items) > 0:
                    item = state.player.items.pop()
                    item.pos.copy_from(state.player.pos)
                    state.items.append(item)

        if state.player.pos.x < 0:
            state.player.pos.x = 0
        if state.player.pos.x >= MAX_WIDTH:
            state.player.pos.x = MAX_WIDTH - 1
        if state.player.pos.y < 0:
            state.player.pos.y = 0
        if state.player.pos.y >= MAX_HEIGHT:
            state.player.pos.y = MAX_HEIGHT - 1

        return state

    def item_at(self, state: DungeonState, pos: Pos) -> Optional[Item]:
        """If an Item is at pos, return it"""
        # reversed; this finds items in most recently "dropped" order, when they occupy the same pos
        for item in reversed(state.items):
            if item.pos == pos:
                return item
        return None

    def draw(self, state: DungeonState, output: Output):
        self.draw_ui(state, output)
        with output.offset(Pos(1, 1)):
            self.draw_items(state, output)
            self.draw_player(state, output)

    def draw_items(self, state: DungeonState, output: Output):
        for item in state.items:
            output.print_at(item.pos, item.view)

    def draw_player(self, state: DungeonState, output: Output):
        output.print_at(state.player.pos, "O")

    def draw_ui(self, state: DungeonState, output: Output):
        """render bound box and labels"""

        # bounds
        width = MAX_WIDTH + 2
        height = MAX_HEIGHT
        bounds = "#" * width + "\n"
        for y in range(0, height):
            bounds += "#" + (" " * (width - 2)) + "#\n"
        bounds += "#" * width
        output.print_at(Pos(0, 0), bounds)

        # status
        with output.offset(Pos(0, height + 1)):
            output.print_at(Pos(2, 0), f"({state.player.pos.x},{state.player.pos.y})")
            item = self.item_at(state, state.player.pos)
            if item:
                output.print_at(Pos(20, 0), f" {item.name} ")

        # inventory
        with output.offset(Pos(0, height + 2)):
            output.print_at(
                Pos(0, 0), f"Inv: {','.join([i.name for i in state.player.items])}"
            )

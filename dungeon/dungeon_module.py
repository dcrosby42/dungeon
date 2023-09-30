"""Dungeon Module"""
from dataclasses import dataclass
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
class DungeonState:
    """State of the D"""

    player_pos: Pos
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
        return DungeonState(Pos(0, 0), items)

    def update(
        self, state: DungeonState, user_input: Input, delta: float
    ) -> DungeonState:
        for key in user_input.keys:
            if key == "KEY_RIGHT":
                state.player_pos.x += 1
            elif key == "KEY_LEFT":
                state.player_pos.x -= 1
            elif key == "KEY_UP":
                state.player_pos.y -= 1
            elif key == "KEY_DOWN":
                state.player_pos.y += 1
        if state.player_pos.x < 0:
            state.player_pos.x = 0
        if state.player_pos.x >= MAX_WIDTH:
            state.player_pos.x = MAX_WIDTH - 1
        if state.player_pos.y < 0:
            state.player_pos.y = 0
        if state.player_pos.y >= MAX_HEIGHT:
            state.player_pos.y = MAX_HEIGHT - 1

        return state

    def draw(self, state: DungeonState, output: Output):
        self.draw_ui(state, output)
        with output.offset(Pos(1, 1)):
            self.draw_items(state, output)
            self.draw_player(state, output)

    def draw_items(self, state: DungeonState, output: Output):
        for item in state.items:
            output.print_at(item.pos, item.view)

    def draw_player(self, state: DungeonState, output: Output):
        output.print_at(state.player_pos, "O")

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

        # player location
        # output.print_at(Pos(2, height + 1), repr(state.player_pos))
        output.print_at(
            Pos(2, height + 1), f"({state.player_pos.x},{state.player_pos.y})"
        )
        for item in state.items:
            if state.player_pos == item.pos:
                output.print_at(Pos(20, height + 1), f" {item.name} ")

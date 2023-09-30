"""Dungeon Module"""
from dataclasses import dataclass
from lethal.lethal import Input, Module, Output, Pos


@dataclass
class DungeonState:
    """State of the D"""

    player_pos: Pos


MAX_WIDTH = 40
MAX_HEIGHT = 10


class DungeonModule(Module[DungeonState]):
    """The Dungeon"""

    def create(self) -> DungeonState:
        return DungeonState(Pos(0, 0))

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
        self.draw_ui(output)
        output.print_at(Pos(1, 1).add(state.player_pos), "O")

    def draw_ui(self, output):
        """render bound box and labels"""
        width = MAX_WIDTH + 2
        height = MAX_HEIGHT
        bounds = "#" * width + "\n"
        for y in range(0, height):
            bounds += "#" + (" " * (width - 2)) + "#\n"
        bounds += "#" * width
        output.print_at(Pos(0, 0), bounds)

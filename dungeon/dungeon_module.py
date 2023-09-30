"""Dungeon Module"""
from dataclasses import dataclass
from lethal.lethal import Input, Module, Output


@dataclass
class Pos:
    """x,y coord pair"""

    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name


@dataclass
class DungeonState:
    """State of the D"""

    pos: Pos


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
                state.pos.x += 1
            elif key == "KEY_LEFT":
                state.pos.x -= 1
            elif key == "KEY_UP":
                state.pos.y -= 1
            elif key == "KEY_DOWN":
                state.pos.y += 1
        if state.pos.x < 0:
            state.pos.x = 0
        if state.pos.x >= MAX_WIDTH:
            state.pos.x = MAX_WIDTH - 1
        if state.pos.y < 0:
            state.pos.y = 0
        if state.pos.y >= MAX_HEIGHT:
            state.pos.y = MAX_HEIGHT - 1

        return state

    def draw(self, state: DungeonState, output: Output):
        print(output.term.move_xy(state.pos.x, state.pos.y) + "X")

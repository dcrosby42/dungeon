# from dungeon_comps import *
from .dungeon_state import DungeonState
from lethal import Output, Loc, Pos
from .dungeon_comps import *


class DungeonRenderer:
    """Single-use object: convenience code around geting state rendered"""

    def __init__(self, state: DungeonState, output: Output):
        self.state = state
        self.output = output
        self.estore = state.estore

        self.player_id = state.my_player_id
        self.player_ent = next((e for e in self.state.estore.select(Player) if e[Player].player_id == self.player_id))

    def draw(self):
        self.draw_ui()

        room_id = self.player_ent[Room].room_id

        with self.output.offset(Pos(1, 1)):  # offset to be within the UI borders
            for ent in sorted(
                self.state.estore.select(Drawable, Loc, Room),
                key=lambda e: e[Drawable].layer,
            ):
                # for ent in state.estore.select(Drawable, Loc, Room):
                if ent[Room].room_id == room_id:
                    self.output.print_at(ent[Loc].to_pos(), ent[Text].text)

    def draw_ui(self):
        """render bound box and labels"""
        width = ROOM_WIDTH + 2
        height = ROOM_HEIGHT

        # messages
        self.output.print_at(
            Pos(0, height + 3),
            self.output.term.darkgray + "\n".join(list(reversed(self.state.messages))[0:5]) + self.output.term.normal,
        )

        # Debug controller state:
        # for e in state.estore.select(Controller):
        #     con = e[Controller]
        #     output.print_at(
        #         Pos(0, height + 3), output.term.blue + repr(con) + output.term.normal
        #     )

        # bounds
        hbar = "+" + ("-" * (width - 2)) + "+"
        bounds = hbar + "\n"
        for y in range(0, height):
            bounds += "|" + (" " * (width - 2)) + "|\n"
        bounds += hbar
        self.output.print_at(Pos(0, 0), bounds)

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

from typing import cast

from pydantic import Field

from lethal import Component, System


class Controller(Component):
    """Controller state"""

    name: str
    up: bool | None = Field(default=False)
    down: bool | None = Field(default=False)
    left: bool | None = Field(default=False)
    right: bool | None = Field(default=False)
    take: bool | None = Field(default=False)
    drop: bool | None = Field(default=False)
    action: bool | None = Field(default=False)


class ControllerSystem(System):
    """Updates Controller components based on user input"""

    def update(self) -> None:
        for ent in self.estore.select(Controller):
            con = ent[Controller]
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
            attr2 = key_map.get(key)
            print(f"Checking {key}")
            if attr2:
                print("setting")
                setattr(con, attr2, True)

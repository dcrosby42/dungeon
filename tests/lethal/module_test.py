# pylint: disable-all
from lethal import module
from dataclasses import dataclass


@dataclass
class MyTestState:
    captured_key: str


class MyMod(module.Module[MyTestState]):
    def create(self) -> MyTestState:
        return MyTestState("")

    def update(
        self, state: MyTestState, user_input: module.Input, delta: float
    ) -> MyTestState:
        state.captured_key = user_input.keys[-1]
        return state

    def draw(self, state: MyTestState, output: module.Output):
        return None


def test_MyMod_create():
    st = MyMod().create()
    assert st.captured_key == ""


def test_MyMod_update():
    mod = MyMod()
    st = mod.create()

    inp = module.Input(["KEY_RIGHT"])
    st = mod.update(st, inp, 0)
    assert st.captured_key == "KEY_RIGHT"

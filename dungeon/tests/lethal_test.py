# pylint: disable-all
from lethal import lethal
from dataclasses import dataclass


@dataclass
class MyTestState:
    captured_key: str


class MyMod(lethal.Module[MyTestState]):
    def create(self) -> MyTestState:
        return MyTestState("")

    def update(self, state: MyTestState, user_input: lethal.Input) -> MyTestState:
        state.captured_key = user_input.keys[-1]
        return state

    def draw(self, state: MyTestState, output: lethal.Output):
        return None


def test_MyMod_create():
    st = MyMod().create()
    assert st.captured_key == ""


def test_MyMod_update():
    mod = MyMod()
    st = mod.create()

    inp = lethal.Input(["KEY_RIGHT"])
    st = mod.update(st, inp)
    assert st.captured_key == "KEY_RIGHT"

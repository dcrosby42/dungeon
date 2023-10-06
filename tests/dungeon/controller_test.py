from lethal import Input, EntityStore
from dungeon.controller import Controller, ControllerSystem
import pdb


def test_Controller():
    estore = EntityStore()
    e = estore.create_entity()
    e.add(Controller(name="controller1"))

    inp = Input(keys=["KEY_RIGHT"])
    system = ControllerSystem(estore=estore, user_input=inp)
    system.update()
    assert e.get(Controller).left is False
    assert e.get(Controller).right is True

    inp = Input(keys=["KEY_LEFT"])
    system = ControllerSystem(estore=estore, user_input=inp)
    system.update()
    assert e.get(Controller).left is True
    assert e.get(Controller).right is False

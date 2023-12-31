# pylint: disable-all

from lethal import Input, EntityStore
from dungeon.controller_system import Controller, ControllerSystem


def test_Controller():
    estore = EntityStore()
    e = estore.create_entity()
    e.add(Controller(name="controller1"))

    inp = Input(keys=["KEY_RIGHT"])
    system = ControllerSystem(estore=estore, user_input=inp)
    system.update()
    assert e[Controller].left is False
    assert e[Controller].right is True

    inp = Input(keys=["KEY_LEFT"])
    system = ControllerSystem(estore=estore, user_input=inp)
    system.update()
    assert e[Controller].left is True
    assert e[Controller].right is False

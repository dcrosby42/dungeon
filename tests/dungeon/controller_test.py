# pylint: disable-all

from dungeon.controller_system import Controller, controller_system
from dungeon.dungeon_comps import Player
from dungeon.dungeon_system import ControllerEvent, DungeonInput

# from lethal import Input
from lethal.ecs2 import Estore


def test_Controller():
    con = Controller()
    con.left = True
    con.action = True
    con.clear()
    assert con.up is False
    assert con.down is False
    assert con.left is False
    assert con.right is False
    assert con.take is False
    assert con.drop is False
    assert con.action is False


def test_ControllerSystem():
    estore = Estore()

    p1e = estore.create_entity(
        Player(player_id="player1"),
        Controller(),
    )
    con1 = estore[p1e, Controller]

    p2e = estore.create_entity(
        Player(player_id="player2"),
        Controller(),
    )
    con2 = estore[p2e, Controller]

    input = DungeonInput(
        events=[
            ControllerEvent("player1", "right"),
            ControllerEvent("player2", "left"),
            ControllerEvent("player1", "drop"),
        ]
    )

    controller_system(estore, input)

    # The Controller for player 1 should be updated according to p1 events:
    assert con1.up is False
    assert con1.down is False
    assert con1.left is False
    assert con1.right is True
    assert con1.take is False
    assert con1.drop is True
    assert con1.action is False

    # The Controller for player 2 should be updated according to p2 events:
    assert con2.up is False
    assert con2.down is False
    assert con2.left is True
    assert con2.right is False
    assert con2.take is False
    assert con2.drop is False
    assert con2.action is False

    # An update with no events should leave controllers cleared:
    input = DungeonInput(events=[])
    controller_system(estore, input)

    assert con1.up is False
    assert con1.down is False
    assert con1.left is False
    assert con1.right is False
    assert con1.take is False
    assert con1.drop is False
    assert con1.action is False

    assert con2.up is False
    assert con2.down is False
    assert con2.left is False
    assert con2.right is False
    assert con2.take is False
    assert con2.drop is False
    assert con2.action is False

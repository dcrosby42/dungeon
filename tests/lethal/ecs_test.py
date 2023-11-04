# pylint: disable-all
from lethal.ecs import Component
from typing import Any


#
# Helpers
#


class Loc2(Component):
    x: int
    y: int


class Loc3(Loc2):
    ...


class Obstr(Component):
    blocker: bool


class TItem(Component):
    name: str


class Annot(Component):
    notes: dict[str, Any]


def make_an_entity(eid="e42"):
    ent = Entity(
        eid=eid,
        components=[
            Loc2(x=1, y=2),
            Obstr(blocker=True),
            Loc2(x=3, y=4),
        ],
    )
    return ent


#
# Component
#


def test_Component():
    loc = Loc2(eid="the_entity", x=100, y=200)
    assert loc.eid == "the_entity"
    assert loc.kind == "Loc2"
    assert loc.x == 100
    assert loc.y == 200


def test_Component_clone():
    nestedObj = {
        "topic": "game dev",
        "entries": ["lib congress", "local lib"],
    }
    ann_orig = Annot(eid="e9", notes=nestedObj)
    ann_copy = ann_orig.clone()

    # See they're equal
    assert ann_copy == ann_orig

    # See changing the copy doesn't change the original
    ann_copy.notes["entries"] = []
    assert ann_orig.notes == nestedObj
    assert ann_copy != ann_orig

    ann_copy2 = ann_orig.clone("new_eid")
    assert ann_copy2.eid == "new_eid"
    assert ann_orig.eid == "e9"


def test_Component_to_dict__from_dict():
    loc = Loc2(eid="the_entity", x=100, y=200)
    # conver to a plain dictionary:
    d = loc.to_dict()
    assert d == {"kind": "Loc2", "eid": "the_entity", "x": 100, "y": 200}
    # reconstitute to a proper Loc2:
    new_loc = Loc2.from_dict(d)
    assert new_loc == Loc2(eid="the_entity", x=100, y=200)


def test_Component__find_class():
    assert Component.find_class("Component") == Component
    assert Component.find_class("Loc2") == Loc2
    assert Component.find_class("Loc3") == Loc3
    assert Component.find_class("TItem") == TItem
    assert Component.find_class("loc") is None

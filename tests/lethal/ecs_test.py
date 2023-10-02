# pylint: disable-all
from lethal.ecs import Entity, Component, NoComponentError
from typing import Any
import pytest

import pdb


class Loc2(Component):
    x: int
    y: int


class Obstr(Component):
    blocker: bool


class Item(Component):
    name: bool


class Annot(Component):
    notes: dict[str, Any]


def makeAnEntity(eid="e42"):
    ent = Entity(
        eid=eid,
        components=[
            Loc2(x=1, y=2),
            Obstr(blocker=True),
            Loc2(x=3, y=4),
        ],
    )
    return ent


def test_Component():
    loc = Loc2(eid="the_entity", x=100, y=200)
    assert loc.eid == "the_entity"
    assert loc.kind == "Loc2"
    assert loc.x == 100
    assert loc.y == 200


def test_Component_clone():
    nestedObj: dict[str, Any] = {
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


def test_Entity_defaults_to_empty_component_list():
    ent = Entity(eid="e1")
    assert ent.eid == "e1"
    assert ent.components == []


def test_Entity_with_comps():
    ent = makeAnEntity("e37")
    assert ent.eid == "e37"
    assert ent.components == [
        Loc2(eid="e37", x=1, y=2),
        Obstr(eid="e37", blocker=True),
        Loc2(eid="e37", x=3, y=4),
    ]


def test_Entity_constructor_deep_copies_comps():
    ann_orig = Annot(notes={"hello": "there", "map": {"a": 1}})
    ent = Entity(eid="e6", components=[ann_orig])

    # See the original Annot is unmodifid
    assert ann_orig == Annot(eid=None, notes={"hello": "there", "map": {"a": 1}})
    # Manually change the original Annot
    ann_orig.notes["hello"] = "bye"
    ann_orig.notes["map"]["b"] = 2

    # See the entity's copied Annot notes remain unchanged:
    ann_copy = ent.get(Annot)
    assert ann_copy.notes == {"hello": "there", "map": {"a": 1}}
    assert ann_copy.eid == "e6"


def test_Entity_select():
    ent = makeAnEntity()
    assert ent.select(Loc2) == [Loc2(eid="e42", x=1, y=2), Loc2(eid="e42", x=3, y=4)]
    assert ent.select(Obstr) == [Obstr(eid="e42", blocker=True)]
    assert ent.select(Item) == []


def test_Entity_get():
    ent = makeAnEntity()
    assert ent.get(Loc2) == Loc2(eid="e42", x=1, y=2)
    assert ent.get(Obstr) == Obstr(eid="e42", blocker=True)


def test_Entity_get_raises_on_miss():
    ent = Entity(eid="e1", components=[Loc2(x=1, y=2)])
    with pytest.raises(NoComponentError) as e_info:
        ent.get(Item)


def test_Entity_add():
    ent = Entity(eid="e1")
    ent.add(Loc2(x=10, y=20))
    loc = ent.get(Loc2)
    assert loc == Loc2(eid="e1", x=10, y=20)


def test_Entity_add_deep_copy():
    ann_orig = Annot(notes={"hello": "there", "map": {"a": 1}})
    ent = Entity(eid="e6")

    # add
    ent.add(ann_orig)

    # See the original Annot is unmodifid
    assert ann_orig == Annot(eid=None, notes={"hello": "there", "map": {"a": 1}})
    # Manually change the original Annot
    ann_orig.notes["hello"] = "bye"
    ann_orig.notes["map"]["b"] = 2

    # See the entity's copied Annot notes remain unchanged:
    ann_copy = ent.get(Annot)
    assert ann_copy.notes == {"hello": "there", "map": {"a": 1}}
    assert ann_copy.eid == "e6"


def test_Entity_remove():
    ent = makeAnEntity()
    loc1 = ent.get(Loc2)
    assert loc1 == Loc2(eid=ent.eid, x=1, y=2)  # (sanity check)

    rloc1 = ent.remove(loc1)
    assert rloc1 == Loc2(eid=None, x=1, y=2)
    assert ent.remove(loc1) == None  # already gone

    loc2 = ent.get(Loc2)
    assert loc2 == Loc2(eid=ent.eid, x=3, y=4)  # (sanity check)

    rloc2 = ent.remove(loc2)
    assert rloc2 == Loc2(eid=None, x=3, y=4)
    assert ent.remove(loc2) == None  # already gone

    # See no more Locs
    with pytest.raises(NoComponentError) as e_info:
        ent.get(Loc2)


def test_Entity_contains():
    ent = makeAnEntity()
    assert ent.contains(Loc2(eid=ent.eid, x=1, y=2)) == True
    assert ent.contains(Loc2(eid=None, x=1, y=2)) == False


def test_Entity_has_any():
    ent = makeAnEntity()
    assert ent.has_any(Loc2) == True
    assert ent.has_any(Obstr) == True
    assert ent.has_any(Item) == False

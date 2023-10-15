# pylint: disable-all
from lethal.ecs import EntityStore, Entity, Component, NoComponentError, NoEntityError
from typing import Any
import pytest

import pdb

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


class Item(Component):
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
    assert Component.find_class("Item") == Item

    assert Component.find_class("loc") is None


#
# Entity
#


def test_Entity_defaults_to_empty_component_list():
    ent = Entity(eid="e1")
    assert ent.eid == "e1"
    assert ent.components == []


def test_Entity_with_comps():
    ent = make_an_entity("e37")
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
    ann_copy = ent[Annot]
    assert ann_copy.notes == {"hello": "there", "map": {"a": 1}}
    assert ann_copy.eid == "e6"


def test_Entity_select():
    ent = make_an_entity()
    assert ent.select(Loc2) == [Loc2(eid="e42", x=1, y=2), Loc2(eid="e42", x=3, y=4)]
    assert ent.select(Obstr) == [Obstr(eid="e42", blocker=True)]
    assert ent.select(Item) == []


def test_Entity_get():
    ent = make_an_entity()
    assert ent[Loc2] == Loc2(eid="e42", x=1, y=2)
    assert ent[Obstr] == Obstr(eid="e42", blocker=True)


def test_Entity_get_raises_on_miss():
    ent = Entity(eid="e1", components=[Loc2(x=1, y=2)])
    with pytest.raises(NoComponentError) as e_info:
        ent[Item]


def test_Entity_add():
    ent = Entity(eid="e1")
    ent.add(Loc2(x=10, y=20))
    loc = ent[Loc2]
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
    ann_copy = ent[Annot]
    assert ann_copy.notes == {"hello": "there", "map": {"a": 1}}
    assert ann_copy.eid == "e6"


def test_Entity_remove():
    ent = make_an_entity()
    loc1 = ent[Loc2]
    assert loc1 == Loc2(eid=ent.eid, x=1, y=2)  # (sanity check)

    rloc1 = ent.remove(loc1)
    assert rloc1 == Loc2(eid=None, x=1, y=2)
    assert ent.remove(loc1) == None  # already gone

    loc2 = ent[Loc2]
    assert loc2 == Loc2(eid=ent.eid, x=3, y=4)  # (sanity check)

    rloc2 = ent.remove(loc2)
    assert rloc2 == Loc2(eid=None, x=3, y=4)
    assert ent.remove(loc2) == None  # already gone

    # See no more Locs
    with pytest.raises(NoComponentError) as e_info:
        ent[Loc2]


def test_Entity_contains():
    ent = make_an_entity()
    assert ent.contains(Loc2(eid=ent.eid, x=1, y=2)) == True
    assert ent.contains(Loc2(eid=None, x=1, y=2)) == False


def test_Entity_has_any():
    ent = make_an_entity()
    assert ent.has_any(Loc2) == True
    assert ent.has_any(Obstr) == True
    assert ent.has_any(Item) == False


def test_Entity_to_dict__from_dict():
    ent = make_an_entity()
    d = ent.to_dict()
    assert d["eid"] == ent.eid
    assert len(d["components"]) == 3
    assert d["components"][0] == {
        "eid": ent.eid,
        "kind": "Loc2",
        "x": 1,
        "y": 2,
    }
    assert d["components"][1] == {
        "eid": ent.eid,
        "kind": "Obstr",
        "blocker": True,
    }
    assert d["components"][2] == {
        "eid": ent.eid,
        "kind": "Loc2",
        "x": 3,
        "y": 4,
    }

    # Rehydrate the data stucture to a proper Entity:
    new_ent = Entity.from_dict(d)
    assert new_ent.eid == ent.eid
    assert len(new_ent.components) == 3
    assert new_ent.components[0] == Loc2(eid=ent.eid, x=1, y=2)
    assert new_ent.components[1] == Obstr(eid=ent.eid, blocker=True)
    assert new_ent.components[2] == Loc2(eid=ent.eid, x=3, y=4)
    # pdb.set_trace()


def test_EntityStore():
    estore = EntityStore()
    assert estore._next_eid() == "e1"
    assert estore._next_eid() == "e2"
    for i in range(1, 10):
        estore._next_eid()
    assert estore._next_eid() == "e12"


def test_EntityStore__next_eid():
    estore = EntityStore()
    assert estore._next_eid() == "e1"
    assert estore._next_eid() == "e2"
    for i in range(1, 10):
        estore._next_eid()
    assert estore._next_eid() == "e12"


def test_EntityStore_create_entity():
    estore = EntityStore()
    e1 = estore.create_entity()
    e2 = estore.create_entity()
    assert e1 == Entity(eid="e1")
    assert e2 == Entity(eid="e2")


def make_an_entity_store():
    estore = EntityStore()
    e1 = estore.create_entity()
    e1.add(Loc2(x=1, y=1))

    e2 = estore.create_entity()
    e2.add(Loc2(x=2, y=2))
    e2.add(Item(name="Money"))

    e3 = estore.create_entity()
    e3.add(Loc2(x=3, y=3))
    e3.add(Obstr(blocker=True))
    e3.add(Item(name="Fountain"))

    return estore


def test_EntityStore_get():
    estore = make_an_entity_store()
    ent = estore["e2"]
    assert ent.eid == "e2"
    assert ent[Item] == Item(eid="e2", name="Money")


def test_EntityStore_destroy_entity():
    estore = make_an_entity_store()
    assert len(estore.entities) == 3
    # See e2:
    ent = estore["e2"]
    estore.destroy_entity(ent)
    # Now... it should be gone:
    with pytest.raises(NoEntityError) as e_info:
        estore["e2"]
    assert len(estore.entities) == 2


def test_EntityStore_get_NoEntityError():
    estore = make_an_entity_store()
    with pytest.raises(NoEntityError) as e_info:
        estore["nope"]


def test_EntityStore_select_when_empty():
    estore = make_an_entity_store()
    ents = estore.select(Annot)
    assert ents == []


def test_EntityStore_select_based_on_single_kind():
    estore = make_an_entity_store()
    ents = estore.select(Item)
    assert len(ents) == 2
    assert ents[0][Item].name == "Money"
    assert ents[1][Item].name == "Fountain"


def test_EntityStore_select_based_on_multiple_kinds():
    estore = make_an_entity_store()
    ents = estore.select(Obstr, Item)
    assert len(ents) == 1
    assert ents[0][Item].name == "Fountain"
    assert ents[0][Obstr].blocker == True


def test_EntityStore_select__all():
    """The select() method should return all the entities, if given empty args"""
    estore = make_an_entity_store()
    ents = estore.select()
    assert len(ents) == 3
    assert ents[0][Loc2].x == 1
    assert ents[1][Item].name == "Money"
    assert ents[2][Obstr].blocker == True


# def test_EntityStore__serialize():
#     estore = make_an_entity_store()
#     x = estore.model_dump()

# pylint:disable-all
from lethal.ecs import Component
from lethal.ecs2 import Estore


class TLoc(Component):
    x: int
    y: int


class TName(Component):
    name: str


class TColl(Component):
    ...


class TPsi(Component):
    lv: int


class TOrphan(Component):
    mom: str


def test__Estore__basics():
    estore = Estore()

    e1 = estore.create_entity()
    assert e1 == "e1"
    estore.set_comp(e1, TLoc(x=2, y=5))
    estore.set_comp(e1, TName(name="Stone"))

    e2 = estore.create_entity()
    assert e2 == "e2"
    estore.set_comp(e2, TLoc(x=3, y=7))
    estore.set_comp(e2, TName(name="Bird"))

    e1_loc = estore.get_comp(e1, TLoc)
    assert e1_loc.eid == e1
    assert e1_loc.x == 2
    assert e1_loc.y == 5
    e1_name = estore.get_comp(e1, TName)
    assert e1_name.name == "Stone"

    e2_loc = estore.get_comp(e2, TLoc)
    assert e2_loc.eid == e2
    assert e2_loc.x == 3
    assert e2_loc.y == 7
    e2_name = estore.get_comp(e2, TName)
    assert e2_name.name == "Bird"

    # deleting comps
    estore.delete_comp(e2, TLoc)
    assert estore.get_comp(e2, TLoc) is None
    assert estore.get_comp(e2, TName) is not None
    estore.delete_comp(e2, TName)
    assert estore.get_comp(e2, TName) is None

    # destroying entities
    estore.destroy_entity(e1)
    assert estore.get_comp(e1, TLoc) is None
    assert estore.get_comp(e1, TName) is None


def test__Estore__alt_syntax():
    estore = Estore()

    e1 = estore.create_entity()
    assert e1 == "e1"
    # estore.set_comp(e1, TLoc(x=2, y=5))
    # estore.set_comp(e1, TName(name="Stone"))
    estore[e1, TLoc] = TLoc(x=2, y=5)
    estore[e1, TName] = TName(name="Stone")

    e1_loc = estore[e1, TLoc]
    assert e1_loc.eid == e1
    assert e1_loc.x == 2
    assert e1_loc.y == 5
    e1_name = estore[e1, TName]
    assert e1_name.name == "Stone"

    # compact-but-strange alternate set_comp syntax:
    estore[e1] = TLoc(x=9, y=8)
    estore[e1] = TName(name="wow")
    assert estore[e1, TLoc] == TLoc(eid=e1, x=9, y=8)
    assert estore[e1, TName] == TName(eid=e1, name="wow")

    # deleting comps via del []
    del estore[e1, TLoc]
    assert estore.get_comp(e1, TLoc) is None
    assert estore.get_comp(e1, TName) is not None
    del estore[e1, TName]
    estore.delete_comp(e1, TName)

    # destroying entities via del []
    e2 = estore.create_entity(
        TName(name="goodbye"),
        TLoc(x=0, y=0),
    )
    assert estore[e2, TName] is not None
    assert estore[e2, TName] is not None
    del estore[e2]
    assert estore.get_comp(e2, TName) is None
    assert estore.get_comp(e2, TName) is None


def test__Estore__by_type():
    estore = Estore()
    n = 5
    for i in range(0, n):
        estore.create_entity(TName(name=f"Point {i+1}"), TLoc(x=i, y=2 * i))

    name_comps = estore.by_type(TName)
    loc_comps = estore.by_type(TLoc)
    for i in range(0, n):
        assert TName(eid=f"e{i+1}", name=f"Point {i+1}") in name_comps
        assert TLoc(eid=f"e{i+1}", x=i, y=2 * i) in loc_comps


def test__Estore__by_types():
    estore = Estore()

    estore.create_entity(TName(name=f"El"), TLoc(x=1, y=1), TColl(), TPsi(lv=10), TOrphan(mom="Terry"))
    estore.create_entity(TName(name=f"Will"))
    estore.create_entity(TName(name=f"Mike"), TLoc(x=3, y=3), TColl())
    estore.create_entity(TName(name=f"Dustin"), TLoc(x=4, y=4))
    estore.create_entity(TName(name=f"Lucas"), TLoc(x=5, y=3))

    # Get component pairings from entities that have both location and name:
    name_tups = estore.by_types2(TLoc, TName)
    names = []
    for loc, name in name_tups:
        names.append(name.name)

    # See four of the kids:
    assert len(names) == 4
    for name in ["El", "Mike", "Dustin", "Lucas"]:
        assert name in names

    # quick-check the remaining alternate signatures of by_typesN to catch silly slips:
    coll_tups = estore.by_types3(TLoc, TName, TColl)
    names = []
    for loc, name, tcoll in coll_tups:
        names.append(name.name)
    assert len(names) == 2
    for name in ["El", "Mike"]:
        assert name in names

    tups4 = estore.by_types4(TLoc, TName, TColl, TPsi)
    assert len(tups4) == 1
    loc, name, coll, psi = tups4[0]
    assert loc.x == 1
    assert name.name == "El"
    assert coll.__class__ == TColl
    assert psi.lv == 10

    tups5 = estore.by_types5(TName, TLoc, TColl, TPsi, TOrphan)
    assert len(tups5) == 1
    name, loc, coll, psi, orph = tups5[0]
    assert name.name == "El"
    assert loc.x == 1
    assert coll.__class__ == TColl
    assert orph.mom == "Terry"
    assert psi.lv == 10


def test__Estore__search():
    estore = Estore()

    estore.create_entity(TName(name=f"El"), TLoc(x=1, y=1), TColl(), TPsi(lv=10), TOrphan(mom="Terry"))
    estore.create_entity(TName(name=f"Will"))
    estore.create_entity(TName(name=f"Mike"), TLoc(x=3, y=3), TColl())
    estore.create_entity(TName(name=f"Dustin"), TLoc(x=4, y=4))
    estore.create_entity(TName(name=f"Lucas"), TLoc(x=5, y=3))

    # Get component pairings from entities that have both location and name:
    results = estore.search(TLoc, TName)
    names = []
    for loc, name in results:
        names.append(name.name)

    # See four of the kids:
    assert len(names) == 4
    for name in ["El", "Mike", "Dustin", "Lucas"]:
        assert name in names

    # quick-check the remaining alternate signatures of by_typesN to catch silly slips:
    coll_res = estore.search(TLoc, TName, TColl)
    names = []
    for _, name, _ in coll_res:
        names.append(name.name)
    assert len(names) == 2
    for name in ["El", "Mike"]:
        assert name in names

    res4 = estore.search(TLoc, TName, TColl, TPsi)
    assert len(res4) == 1
    loc, name, coll, psi = res4[0]
    assert loc.x == 1
    assert name.name == "El"
    assert coll.__class__ == TColl
    assert psi.lv == 10

    res5 = estore.search(TName, TLoc, TColl, TPsi, TOrphan)
    assert len(res5) == 1
    name, loc, coll, psi, orph = res5[0]
    assert name.name == "El"
    assert loc.x == 1
    assert coll.__class__ == TColl
    assert orph.mom == "Terry"
    assert psi.lv == 10

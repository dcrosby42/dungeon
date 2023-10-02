# pylint: disable-all
from lethal import Loc
from lethal import Pos
from typing import Any
import pytest

import pdb


def test_Loc():
    loc = Loc(eid="e1", x=10, y=20)
    assert loc.eid == "e1"
    assert loc.x == 10
    assert loc.y == 20

    # convert to Pos:
    assert loc.to_pos() == Pos(10, 20)

    # to-and-from dict:
    d1 = loc.model_dump()
    loc2 = Loc.model_validate(d1)
    assert loc2 == loc

    # to-and-from json:
    d2 = loc.model_dump_json()
    loc3 = Loc.model_validate_json(d2)
    assert loc3 == loc

    # see add() modifies the loc in-place:
    loc.add(loc2).add(loc3)
    assert loc.x == 30
    assert loc.y == 60

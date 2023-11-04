"""Lethal ECS"""
from typing import Type, TypeVar, cast

from pydantic import BaseModel

EntityId = str


class EcsError(RuntimeError):
    """ECS error base"""


class NoComponentError(EcsError):
    """Raised when you try to access a component type and Entity has none of."""

    def __init__(self, eid: EntityId, ctype: Type["Component"]):
        super(EcsError, self).__init__(f"Entity {eid} has no {ctype.__name__}")


C = TypeVar("C", bound="Component")


class Component(BaseModel):
    """A Component has an entity id (eid) and a kind (auto-set to the name of the class)"""

    eid: EntityId
    kind: str

    def __init__(self, **data):
        if data.get("kind") is None:
            data["kind"] = type(self).__name__
        if data.get("eid") is None:
            data["eid"] = ""
        super().__init__(**data)

    def clone(self, eid=None) -> "Component":
        """Create a deep copy of this component.
        If optional eid is given, the cloned component will have its eid updated."""
        copy = self.model_copy(deep=True)
        if eid:
            copy.eid = eid
        return copy

    def clone2(self, t: Type[C], eid: EntityId = "") -> C:
        """Create a deep copy of this component.
        If optional eid is given, the cloned component will have its eid updated."""
        copy = self.model_copy(deep=True)
        if eid != "":
            copy.eid = eid
        return cast(C, copy)

    def to_dict(self):
        """Return a dict representation of this Component"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, d):
        """Given a dict of component data, return a Component of the proper subclass"""
        subclass = cls.find_class(d["kind"])

        return subclass.model_validate(d)

    @classmethod
    def find_class(cls, name):
        """Given a Component kind name, find the matching Component subclass"""

        if cls.__name__ == name:
            return cls
        for subc in cls.__subclasses__():
            x = subc.find_class(name)
            if x:
                return x
        return None


class SideEffect(BaseModel):
    """A thing systems return to change the world outside"""

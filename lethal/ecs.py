"""Lethal ECS"""
from typing import Type

from pydantic import BaseModel, Field
import pdb

EntityId = str


class EcsError(RuntimeError):
    """ECS error base"""


class NoComponentError(EcsError):
    """Raised when you try to access a component type and Entity has none of."""

    def __init__(self, ent: "Entity", comp_kind: Type["Component"]):
        super().__init__(f"Entity {ent.eid} has no {comp_kind.__name__} component(s)")


class Component(BaseModel):
    """A Component has an entity id (eid) and a kind (auto-set to the name of the class)"""

    eid: EntityId | None = Field(default=None)
    kind: str | None = Field(default=None)

    def __init__(self, **data):
        if data.get("kind") is None:
            data["kind"] = type(self).__name__
        super().__init__(**data)

    def clone(self, eid=None) -> "Component":
        """Create a deep copy of this component.
        If optional eid is given, the cloned component will have its eid updated."""
        copy = self.model_copy(deep=True)
        if eid:
            copy.eid = eid
        return copy


class Entity(BaseModel):
    """An Entity is just an ID and a bunch of Components,
    with some added conveniences."""

    eid: EntityId
    components: list[Component] = Field(default=[])

    def __init__(self, **data):
        # Any components passed to the constructor are:
        #   - deep-copied
        #   - given the eid of the Entity
        data["components"] = [
            comp.clone(data["eid"]) for comp in data.get("components", [])
        ]
        super().__init__(**data)

    def add(self, comp: Component):
        """Add the Component to this entity. eid will be assigned. deep-copy"""
        # pylint: disable=no-member
        self.components.append(comp.clone(self.eid))

    def remove(self, comp: Component) -> Component | None:
        """
        Delete the Component from this Entity.
        If found, deletes comp from components, sets eid=None, returns comp
        If not, returns None.
        """
        ret = None
        while self.contains(comp):
            # (looping to doubly ensure comp didn't somehow make in the list twice)
            # pylint: disable=no-member
            self.components.remove(comp)
            ret = comp
            ret.eid = None
        return ret

    def contains(self, comp: Component) -> bool:
        """Returns true if this Entity contains the precise component"""
        # pylint: disable=no-member
        return self.components.count(comp) > 0

    def has_any(self, kind: Type[Component]) -> bool:
        """Returns True if Entity contains any Components of the given type"""
        # TODO: DO THIS SMARTER
        try:
            self.get(kind)
            return True
        except NoComponentError:
            return False

    def select(self, kind: Type[Component]) -> list[Component]:
        """Get a list of components matching the given kind"""
        return [comp for comp in self.components if isinstance(comp, kind)]

    def get(self, kind: Type[Component]) -> Component:
        """Return the component of given type.
        If Entity has multiple like-kind Components, the first is returned.
        If Entity has no matching Components, NoComponentError is raised.
        """
        hits = self.select(kind)
        if len(hits) > 0:
            return hits[0]
        raise NoComponentError(self, kind)


# Entity.remove_all ?

# Entity.remove_all(kind) ?

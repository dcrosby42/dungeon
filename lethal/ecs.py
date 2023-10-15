"""Lethal ECS"""
from typing import Type, TypedDict, TypeVar, cast

from pydantic import BaseModel, Field

from .input import Input

EntityId = str


class EcsError(RuntimeError):
    """ECS error base"""


class NoComponentError(EcsError):
    """Raised when you try to access a component type and Entity has none of."""

    def __init__(self, ent: "Entity", comp_kind: Type["Component"]):
        super(EcsError, self).__init__(f"Entity {ent.eid} has no {comp_kind.__name__} component(s)")


class NoEntityError(EcsError):
    """Raised when you try to get an Entity by eid that doesn't exist in the EntityStore"""

    def __init__(self, eid: "EntityId"):
        super(NoEntityError, self).__init__(f"EntityStore has no Entity with eid {eid}")


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


class EntityDict(TypedDict):
    """For Entity.{to,from}_dict"""

    eid: str
    components: list[dict]


C = TypeVar("C", bound=Component)


class Entity(BaseModel):
    """An Entity is just an ID and a bunch of Components,
    with some added conveniences."""

    eid: EntityId
    components: list[Component]

    def __init__(self, **data):
        # Any components passed to the constructor are:
        #   - deep-copied
        #   - given the eid of the Entity
        data["components"] = [comp.clone(data["eid"]) for comp in data.get("components", [])]
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
            _ = self[kind]
            return True
        except NoComponentError:
            return False

    def has_all(self, kinds: list[Type[Component]]) -> bool:
        """Returns True if this Entity has a Component of each kind"""
        for kind in kinds:
            hits = self.select(kind)
            if len(hits) == 0:
                return False
        return True

    def select(self, kind: Type[Component]) -> list[Component]:
        """Get a list of components matching the given kind"""
        # pylint: disable=not-an-iterable
        return [comp for comp in self.components if isinstance(comp, kind)]

    def __getitem__(self, kind: Type[C]) -> C:
        """Return the Component of given type.
        If Entity has multiple like-kind Components, the first is returned.
        If Entity has no matching Components, NoComponentError is raised.
        """
        hits = self.select(kind)
        if len(hits) > 0:
            return cast(C, hits[0])
        raise NoComponentError(self, kind)

    def to_dict(self) -> EntityDict:
        """Eases serialization"""
        return {
            "eid": self.eid,
            "components": [c.to_dict() for c in self.components],
        }

    @classmethod
    def from_dict(cls, ed: EntityDict) -> "Entity":
        """Given a dictionary w entity data, return an Entity"""
        return cls(
            eid=ed["eid"],
            components=[Component.from_dict(cd) for cd in ed["components"]],
        )


# Entity.remove_all ?

# Entity.remove_all(kind) ?


class EntityStore:
    """EntityStore creates, holds and finds Entities"""

    entities: dict[EntityId, Entity]
    eid_counter: int

    def __init__(self):
        self.entities = {}
        self.eid_counter = 0

    def create_entity(self) -> Entity:
        """Create a new empty Entity with the next eid"""
        ent = Entity(eid=self._next_eid())
        # pylint: disable=unsupported-assignment-operation
        self.entities[ent.eid] = ent
        return ent

    def destroy_entity(self, entity: Entity) -> None:
        """Remove the given entity"""
        del self.entities[entity.eid]

    def _next_eid(self) -> EntityId:
        """Generate the next eid"""
        self.eid_counter += 1
        return f"e{self.eid_counter}"

    def __getitem__(self, eid: EntityId) -> Entity:
        """Returns an Entity given an eid.
        Raises NoEntityError if not found."""
        ent = self.entities.get(eid)  # pylint: disable=no-member
        if not ent:
            raise NoEntityError(eid)
        return ent

    def select(self, *kinds: Type[Component]) -> list[Entity]:
        """Return a list of all Entities containing Components of all the given kinds"""
        return [ent for _, ent in self.entities.items() if ent.has_all(list(kinds))]


class SideEffect(BaseModel):
    """A thing systems return to change the world outside"""


class System:
    """ECS System base class"""

    estore: EntityStore
    user_input: Input
    side_effects: list[SideEffect]

    def __init__(self, estore: EntityStore, user_input: Input):
        self.estore = estore
        self.user_input = user_input
        self.side_effects = []

    def update(self) -> None:
        """Default behavior: No-op"""

    def add_side_effect(self, side_effect: SideEffect) -> SideEffect:
        """Record a side effect"""
        self.side_effects.append(side_effect)
        return side_effect

from typing import Tuple, Type, TypeVar, cast
from lethal.ecs import Component, EntityId, NoComponentError

CompEntMap = dict[Type[Component], dict[EntityId, Component]]

C = TypeVar("C", bound=Component)  # pylint:disable=invalid-name
C1 = TypeVar("C1", bound=Component)  # pylint:disable=invalid-name
C2 = TypeVar("C2", bound=Component)  # pylint:disable=invalid-name
C3 = TypeVar("C3", bound=Component)  # pylint:disable=invalid-name
C4 = TypeVar("C4", bound=Component)  # pylint:disable=invalid-name


class Estore:
    """Entity Store"""

    cmap: CompEntMap
    eid_counter: int

    def __init__(self, cmap: CompEntMap | None = None, eid_counter: int = 0):
        self.cmap = cmap or {}
        self.eid_counter = eid_counter

    def create_entity(self, *comps: Component) -> EntityId:
        """Return a new entity id"""
        self.eid_counter += 1
        eid = f"e{self.eid_counter}"
        for comp in comps:
            self[eid] = comp
        return eid

    def destroy_entity(self, eid: EntityId) -> None:
        """Remove the indicated entity"""
        for _ctype, emap in self.cmap.items():
            if eid in emap:
                del emap[eid]

    def set_comp(self, eid: EntityId, comp: Component) -> None:
        """
        Add the given component to the given entity.
        Creates a deep copy of the clone and sets the eid.
        """
        ctype = comp.__class__
        if ctype not in self.cmap:
            self.cmap[ctype] = {}
        self.cmap[ctype][eid] = comp.clone(eid)

    def get_comp(self, eid: EntityId, ctype: Type[C]) -> C | None:
        """Return the Component of the requested type for the indicated Entity"""
        if ctype in self.cmap and eid in self.cmap[ctype]:
            return cast(C, self.cmap[ctype][eid])
        return None

    def delete_comp(self, eid: EntityId, ctype: Type[C]) -> None:
        """Return the Component of the requested type for the indicated Entity"""
        if ctype in self.cmap and eid in self.cmap[ctype]:
            del self.cmap[ctype][eid]

    def __setitem__(self, key: EntityId | Tuple[EntityId, Type[C]], comp: Component) -> None:
        """Convenience syntax for 'set_comp'"""
        if isinstance(key, EntityId):
            return self.set_comp(key, comp)
        else:
            return self.set_comp(key[0], comp)

    def __getitem__(self, key: Tuple[EntityId, Type[C]]) -> C:
        """Convenience syntax for 'get_comp'"""
        comp = self.get_comp(key[0], key[1])
        if not comp:
            raise NoComponentError(eid=key[0], ctype=key[1])
        return comp

    def __delitem__(self, key: EntityId | Tuple[EntityId, Type[C]]) -> None:
        """Convenience syntax for either 'destroy_entity' or 'delete_comp'"""
        if isinstance(key, EntityId):
            self.destroy_entity(key)
        else:
            self.delete_comp(key[0], key[1])

    def by_type(self, ctype: Type[C]) -> list[C]:
        """Get components of the given type"""
        return [cast(C, comp) for comp in self.cmap[ctype].values()]

    def by_types2(
        self,
        ctype0: Type[C],
        ctype1: Type[C1],
    ) -> list[Tuple[C, C1]]:
        """Get combinations of Components based on 2 types and joined on entity id"""
        found: list[Tuple[C, C1]] = []
        if ctype0 in self.cmap:
            for eid, comp0 in self.cmap[ctype0].items():
                if ctype1 in self.cmap and eid in self.cmap[ctype1]:
                    comp1 = self.cmap[ctype1][eid]
                    found.append((cast(C, comp0), cast(C1, comp1)))
        return found

    def by_types3(
        self,
        ctype0: Type[C],
        ctype1: Type[C1],
        ctype2: Type[C2],
    ) -> list[Tuple[C, C1, C2]]:
        """Get combinations of Components based on 3 types and joined on entity id"""
        found: list[Tuple[C, C1, C2]] = []
        if ctype0 in self.cmap:
            for eid, comp0 in self.cmap[ctype0].items():
                if ctype1 in self.cmap and eid in self.cmap[ctype1]:
                    comp1 = self.cmap[ctype1][eid]
                    if ctype2 in self.cmap and eid in self.cmap[ctype2]:
                        comp2 = self.cmap[ctype2][eid]
                        found.append((cast(C, comp0), cast(C1, comp1), cast(C2, comp2)))
        return found

    def by_types4(
        self,
        ctype0: Type[C],
        ctype1: Type[C1],
        ctype2: Type[C2] | None = None,
        ctype3: Type[C3] | None = None,
    ) -> list[Tuple[C, C1, C2, C3]]:
        """Get combinations of Components based on 4 types and joined on entity id"""
        found: list[Tuple[C, C1, C2, C3]] = []
        if ctype0 in self.cmap:
            for eid, comp0 in self.cmap[ctype0].items():
                if ctype1 in self.cmap and eid in self.cmap[ctype1]:
                    comp1 = self.cmap[ctype1][eid]
                    if ctype2 in self.cmap and eid in self.cmap[ctype2]:
                        comp2 = self.cmap[ctype2][eid]
                        if ctype3 in self.cmap and eid in self.cmap[ctype3]:
                            comp3 = self.cmap[ctype3][eid]
                            found.append((cast(C, comp0), cast(C1, comp1), cast(C2, comp2), cast(C3, comp3)))
        return found

    def by_types5(
        self,
        ctype0: Type[C],
        ctype1: Type[C1],
        ctype2: Type[C2],
        ctype3: Type[C3],
        ctype4: Type[C4],
    ) -> list[Tuple[C, C1, C2, C3, C4]]:
        """Get combinations of Components based on 5 types and joined on entity id"""
        found: list[Tuple[C, C1, C2, C3, C4]] = []
        if ctype0 in self.cmap:
            for eid, comp0 in self.cmap[ctype0].items():
                if ctype1 in self.cmap and eid in self.cmap[ctype1]:
                    comp1 = self.cmap[ctype1][eid]
                    if ctype2 in self.cmap and eid in self.cmap[ctype2]:
                        comp2 = self.cmap[ctype2][eid]
                        if ctype3 in self.cmap and eid in self.cmap[ctype3]:
                            comp3 = self.cmap[ctype3][eid]
                            if ctype4 in self.cmap and eid in self.cmap[ctype4]:
                                comp4 = self.cmap[ctype4][eid]
                                found.append(
                                    (cast(C, comp0), cast(C1, comp1), cast(C2, comp2), cast(C3, comp3), cast(C4, comp4))
                                )
        return found

    def search(self, *ctypes: Type[Component]) -> list[list[Component]]:
        """
        Search entities, returning combos based on required component types.
        Much the same as by_typesN(), with two important differences:
        - ctypes can be 0 or more Component type names. (len(0) implies empty results).  No upper limit.
        - Results are lists of length = len(ctypes)... not tuples.
        - Results are list[Component] instead of being strongly typed; no lovey-dovey type inference for you! Your code will need to make assumptions about down-casts; mypy will not love you.
        """
        count = len(ctypes)
        results: list[list[Component]] = []
        if count < 1:
            return results
        t0 = ctypes[0]
        if t0 not in self.cmap:
            return results
        for eid, _ in self.cmap[t0].items():
            comp0 = self.cmap[t0][eid]
            row = [comp0]
            for ct in ctypes[1:]:
                if ct in self.cmap and eid in self.cmap[ct]:
                    row.append(self.cmap[ct][eid])
                else:
                    # we missed one; stop looking for any more comps for the current entity
                    break
            if len(row) == count:
                # only append full results
                results.append(row)
        return results

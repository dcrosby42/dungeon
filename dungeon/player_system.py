from typing import cast

from lethal import Entity, Loc

from .controller_system import Controller
from .dungeon_comps import *
from .dungeon_system import DungeonSystem


class PlayerSystem(DungeonSystem):
    """Update Player(s)"""

    def update(self) -> None:
        for player_e in self.estore.select(Player, Controller, Room, Loc):
            room = cast(Room, player_e.get(Room))
            loc = cast(Loc, player_e.get(Loc))
            con = cast(Controller, player_e.get(Controller))

            loc_backup = loc.model_copy()
            self._move(loc, con)

            for other_e in self._entities_at_loc(room, loc):
                if other_e.has_any(Place):
                    place: Place = other_e.get(Place)
                    if place.blocked:
                        # undo move, emit message
                        loc.x = loc_backup.x
                        loc.y = loc_backup.y
                        self._message(f"Bonk! {place.name} blocks the way.")
                    elif con.action:
                        door: Door = other_e.get(Door)
                        if door:
                            dest_door = next(
                                (e for e in self.estore.select(Door) if e.get(Door).door_id == door.to_door_id),
                                None,
                            )
                            if dest_door:
                                dest_room = dest_door.get(Room).room_id
                                self._message(f"Opened door {door.door_id}")
                                player_e.get(Loc).x = dest_door.get(Loc).x
                                player_e.get(Loc).y = dest_door.get(Loc).y
                                player_e.get(Room).room_id = dest_room
                                # self.add_side_effect(
                                #     RoomSideEffect(to_room_id=dest_room)
                                # )

                elif other_e.has_any(Item):
                    # TODO: Pickup items
                    # item_e = other_e.get(Item)
                    # item_e.remove(Drawable)
                    # item_e.add(Link(eid=player_e))
                    ...
                elif other_e.has_any(Mob):
                    # Mob encounter!

                    # prevent motion
                    loc.x = loc_backup.x
                    loc.y = loc_backup.y

                    self._attack_mob(player_e, other_e)

    def _attack_mob(self, player_e: Entity, mob_e: Entity):
        hit = True
        damage = 1
        if hit:
            mob_health = mob_e.get(Health)
            mob_health.current = max(mob_health.current - damage, 0)
            if mob_health.current <= 0:
                self.estore.destroy_entity(mob_e)
                self._message(f"{mob_e.get(Mob).name} defeated!")
            else:
                self._message(f"{mob_e.get(Mob).name} hit for {damage}")
        else:
            self._message(f"{mob_e.get(Mob).name} missed")

    def _move(self, loc: Loc, con: Controller) -> None:
        if con.right:
            loc.x = min(loc.x + 1, ROOM_WIDTH - 1)
        if con.left:
            loc.x = max(loc.x - 1, 0)
        if con.up:
            loc.y = max(loc.y - 1, 0)
        if con.down:
            loc.y = min(loc.y + 1, ROOM_HEIGHT - 1)
        if con.take:
            pass
        if con.drop:
            pass

    def _entities_at_loc(self, room: Room, loc: Loc):
        def hitting(ent: Entity, room: Room, loc: Loc):
            if ent.eid != loc.eid:
                if ent.get(Room).room_id == room.room_id:
                    eloc = ent.get(Loc)
                    return eloc.x == loc.x and eloc.y == loc.y
            return False

        return [e for e in self.estore.select(Room, Loc) if hitting(e, room, loc)]

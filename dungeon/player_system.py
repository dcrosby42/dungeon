from typing import Generator

from lethal import Loc, SideEffect
from lethal import EntityId, SideEffect
from lethal.ecs2 import Estore

from .controller_system import Controller
from .dungeon_comps import *
from .dungeon_system import DungeonInput, MsgSideEffect


def player_system(estore: Estore, _inp: DungeonInput) -> list[SideEffect]:
    """Update Player(s)"""
    messages: list[str] = []
    for _player, con, pl_room, pl_loc in estore.by_types4(Player, Controller, Room, Loc):
        loc_backup = pl_loc.model_copy()
        update_loc(pl_loc, con)

        for other_eid in other_eids_at_location(estore, pl_room, pl_loc):
            place = estore.get_comp(other_eid, Place)
            if place:
                if place.blocked:
                    # undo move, emit message
                    pl_loc.x = loc_backup.x
                    pl_loc.y = loc_backup.y
                    messages.append(f"Bonk! {place.name} blocks the way.")
                elif con.action:
                    this_door = estore.get_comp(other_eid, Door)
                    if this_door:
                        hits = [rd for rd in estore.by_types3(Room, Door, Loc) if rd[1].door_id == this_door.to_door_id]
                        if hits:
                            dest_room, _dest_door, dest_loc = hits[0]
                            messages.append(f"Passed through door into {dest_room.room_id}")
                            # Travel to the destination room
                            pl_room.room_id = dest_room.room_id
                            pl_loc.x = dest_loc.x
                            pl_loc.y = dest_loc.y

            item = estore.get_comp(other_eid, Item)
            if item:
                # TODO: Pickup items
                # messages.append(f"Item {item.name}")
                # item_e = other_e[Item]
                # item_e.remove(Drawable)
                # item_e.add(Link(eid=player_e))
                ...
            mob = estore.get_comp(other_eid, Mob)
            if mob:
                # Mob encounter!

                # undo motion
                pl_loc.x = loc_backup.x
                pl_loc.y = loc_backup.y

                attack_msgs = attack_mob(estore, mob)
                messages.extend(attack_msgs)

    return list(map(lambda s: MsgSideEffect(text=s), messages))


def attack_mob(estore: Estore, mob: Mob) -> list[str]:
    """dfd"""
    messages = []
    hit = True
    damage = 1
    if hit:
        mob_health = estore[mob.eid, Health]
        mob_health.current = max(mob_health.current - damage, 0)
        if mob_health.current <= 0:
            estore.destroy_entity(mob.eid)
            messages.append(f"{mob.name} defeated!")
        else:
            messages.append(f"{mob.name} hit for {damage}")
    else:
        messages.append(f"{mob.name} missed")
    return messages


def update_loc(loc: Loc, con: Controller) -> None:
    """dssds"""
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


def other_eids_at_location(estore: Estore, room: Room, loc: Loc) -> Generator[EntityId, None, None]:
    """dfdd"""
    room = room.clone2(Room)
    loc = loc.clone2(Loc)
    for room_b, loc_b in estore.by_types2(Room, Loc):
        if (loc_b.eid != loc.eid) and (room_b.room_id == room.room_id) and (loc_b.x == loc.x and loc_b.y == loc.y):
            yield loc_b.eid

"""ECS Components for the Dungeon"""
from pydantic import Field
from lethal import Component

ROOM_WIDTH = 80
ROOM_HEIGHT = 15


class Text(Component):
    """Drawable string"""

    text: str


class Drawable(Component):
    """For entities that can be drawn"""

    layer: int | None = Field(default=0)


class Item(Component):
    """A thing you can get"""

    cat: str
    name: str
    value: int


class Player(Component):
    """Indicates a player"""

    player_id: str


MobCategory = str


class Mob(Component):
    """Indicates a non-player creature"""

    name: str
    cat: MobCategory


class Place(Component):
    """A place on the map"""

    name: str
    blocked: bool | None = Field(default=False)


class Health(Component):
    """Creature or player health"""

    max: int
    current: int


class Room(Component):
    """Relates an entity to a room"""

    room_id: str


class Door(Component):
    """Doors link to doors by id"""

    door_id: str
    to_door_id: str

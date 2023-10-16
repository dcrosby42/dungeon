from typing import List, Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey, String, create_engine, Engine, select


class Base(DeclarativeBase):
    """Base class for all these db models"""


MetaData = Base.metadata


class Dungeon(Base):
    """Dungeons contain rooms"""

    __tablename__ = "dungeon"
    id: Mapped[int] = mapped_column(primary_key=True)
    shortname: Mapped[str] = mapped_column(String(30))
    name: Mapped[Optional[str]]
    rooms: Mapped[List["Room"]] = relationship(back_populates="dungeon")

    def __repr__(self) -> str:
        return f"Dungeon(id={self.id!r}, name={self.name!r}, shortname={self.shortname!r})"


class Room(Base):
    """Rooms comprise dungeons"""

    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    dungeon_id = mapped_column(ForeignKey("dungeon.id"))
    dungeon: Mapped[Dungeon] = relationship(back_populates="rooms")

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, name={self.name!r}, dungeon_id={self.dungeon_id})"


# all_users = []
# with Session(engine) as session:
#     for row in session.execute(select(User)):
#         all_users.append(row)

# with Session(engine) as session:
#     for user in all_users:
#         print(f"Deleting: {user}")
#         session.delete(user)

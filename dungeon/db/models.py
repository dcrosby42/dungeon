from typing import List, Optional, Any

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey, String, create_engine, Engine, select


class Base(DeclarativeBase):
    """Base class for all these db models"""

    def attrs(self) -> dict[str, Any]:
        """Return attributes as a dict"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __repr__(self) -> str:
        """Return formatted repr like MyModel(field1=val1 field2=val2 ...)"""
        attr_str = " ".join([f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_")])
        return f"{self.__class__.__name__}({attr_str})"


MetaData = Base.metadata


class Dungeon(Base):
    """Dungeons contain rooms"""

    __tablename__ = "dungeon"
    id: Mapped[int] = mapped_column(primary_key=True)
    shortname: Mapped[str] = mapped_column(String(30))
    name: Mapped[Optional[str]]
    rooms: Mapped[List["Room"]] = relationship(back_populates="dungeon", cascade="all, delete-orphan")


class Room(Base):
    """Rooms comprise dungeons"""

    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    dungeon_id = mapped_column(ForeignKey("dungeon.id"))
    dungeon: Mapped[Dungeon] = relationship(back_populates="rooms")

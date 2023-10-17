import os

import ptpython.repl
import tomli
from sqlalchemy import URL, Engine, create_engine, select
from sqlalchemy.orm import Session

from dungeon.db.models import Dungeon, MetaData, Room


def load_db_conf(filename: str, section: str = "database"):
    """Load database conf from toml file"""
    with open(filename, "rb") as f:
        d = tomli.load(f)
        return d[section]


def connect_engine(
    database: str,
    username: str,
    password: str,
    host: str = "localhost",
    port: int | None = None,  # 5432
    echo: bool = False,
    driver: str = "postgresql+psycopg2",
) -> Engine:
    """Connect to the database and return a new Engine"""
    conn_url = URL.create(
        driver,
        username=username,
        password=password,
        host=host,
        port=port,
        database=database,
    )
    return create_engine(conn_url, echo=echo)


def create_db_schema(engine):
    """Ensures the schema exists in the db"""
    MetaData.create_all(engine)


def destroy_db_schema(engine):
    """die"""
    MetaData.drop_all(engine)


def rebuild_db_schema(engine):
    """undie"""
    destroy_db_schema(engine)
    create_db_schema(engine)


class Builder:
    """Dungeon builder util"""

    session: Session

    def __init__(self, session: Session):
        self.session = session

    def build_dungeon(self, shortname):
        """generate a dungeon"""
        if self.session.query(Dungeon.id).where(Dungeon.shortname == shortname).count() > 0:
            print(f"Builder: Dungeon '{shortname}' already exists; skipping.")
            return
        # self.session.
        d = Dungeon(shortname=shortname, name="First Dungeon")
        d.rooms = [
            Room(name="room1"),
            Room(name="room2"),
        ]
        self.session.add(d)
        self.session.flush()

    def delete_dungeon(self, shortname):
        """delete a dungeon"""
        for d in self.session.query(Dungeon).where(Dungeon.shortname == shortname).all():
            print(f"Builder: deleting dungeon: f{d}")
            self.session.delete(d)

    def console(self):
        """Start a REPL with an active db session"""
        print("""Welcome to DB console""")
        session = self.session  # pylint: disable=possibly-unused-variable
        S = session
        home = os.getenv("HOME")
        ptpython.repl.embed(locals=locals(), globals=globals(), history_filename=f"{home}/.ptpython_history")

    def dump_stuff(self):
        """print the stuff"""
        print("Dungeons")
        for d in self.session.scalars(select(Dungeon)):
            print(d)
        print("Rooms")
        for r in self.session.scalars(select(Room)):
            print(r)

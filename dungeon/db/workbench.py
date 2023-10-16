import tomli
from sqlalchemy import URL, Engine, create_engine, select
from sqlalchemy.orm import Session

from dungeon.db.models import MetaData, Dungeon, Room


def load_db_conf(filename: str, section: str = "database"):
    """Load database conf from toml file"""
    with open("db.dev.toml", "rb") as f:
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

    def build_dungeon1(self):
        """d1"""
        d = Dungeon(shortname="dun1", name="First Dungeon")
        d.rooms = [
            Room(name="room1"),
            Room(name="room2"),
        ]
        self.session.add(d)
        self.session.flush()

    def prompt(self):
        """debugging"""
        session = self.session
        import pdb

        pdb.set_trace()

    def dump_stuff(self):
        print("Dungeons")
        for d in self.session.scalars(select(Dungeon)):
            print(d)
        print("Rooms")
        for r in self.session.scalars(select(Room)):
            print(r)


# def list_users(engine):
#     with Session(engine) as session:
#         for user in session.scalars(select(User)):
#             print(user)


# def list_users2(engine):
#     with Session(engine) as session:
#         for name, fullname in session.execute(select(User.name, User.fullname)):
#             print(f"User {name} is named {fullname}")


# def add_users(engine):
#     session = Session(engine)
#     session.add(User(name="lemmy", fullname="Lemmy Kilmister"))
#     session.add(User(name="ozzy", fullname="Ozzy Osbourne"))
#     session.flush()
#     session.commit()

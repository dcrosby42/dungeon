# import dungeon.db.workbench  # pylint: disable=unused-import
from invoke import task
from sqlalchemy.orm import Session

from dungeon.db import workbench as ddb

Stuff = {"engine": None}


def connect():
    """Connect to the database"""
    if Stuff["engine"] is None:
        Stuff["engine"] = ddb.connect_engine(**ddb.load_db_conf("db.dev.toml"))
    return Stuff["engine"]


@task
def create_schema(c):
    """Create DB schema"""
    engine = connect()
    ddb.create_db_schema(engine)


@task
def recreate_schema(c):
    """RE-create DB schema (first destroying it)"""
    engine = connect()
    ddb.rebuild_db_schema(engine)


@task
def console(c):
    """Print dungones and rooms and stuff"""
    engine = connect()
    with Session(engine) as session:
        builder = ddb.Builder(session)
        # builder.prompt()
        builder.console()


@task
def build_dungeon(c):
    """Generate a dungeon in the db"""
    with Session(connect()) as session:
        builder = ddb.Builder(session)
        builder.build_dungeon("dun1")
        # builder.prompt()
        session.commit()
        builder.dump_stuff()
        session.close()


@task
def delete_dungeon(c):
    """Removes a dungeon from the db"""
    with Session(connect()) as session:
        builder = ddb.Builder(session)
        builder.delete_dungeon("dun1")
        session.commit()
        builder.dump_stuff()
        session.close()


@task
def show_dungeon(c):
    """Print dungones and rooms and stuff"""
    engine = connect()
    with Session(engine) as session:
        builder = ddb.Builder(session)
        builder.dump_stuff()
        session.close()

        # builder.build_dungeon1()
        # builder.prompt()
        # session.commit()

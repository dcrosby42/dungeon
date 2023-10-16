# import dungeon.db.workbench  # pylint: disable=unused-import
from sqlalchemy.orm import Session

from dungeon.db import workbench as ddb

engine = ddb.connect_engine(**ddb.load_db_conf("db.dev.toml"))

ddb.create_db_schema(engine)

with Session(engine) as session:
    builder = ddb.Builder(session)
    builder.build_dungeon1()
    # builder.prompt()
    session.commit()

    builder.dump_stuff()

    session.close()

# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html

from sqlalchemy import create_engine

# from sqlalchemy import text
from sqlalchemy import MetaData, ForeignKey, Table, Column, Integer, String

CONN_STR = "postgresql+psycopg2://toaduser:toadpass@localhost:5451/toadstool"
engine = create_engine(CONN_STR, echo=True)

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

metadata_obj.create_all(engine)

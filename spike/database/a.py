from sqlalchemy import create_engine
from sqlalchemy import text

CONN_STR = "postgresql+psycopg2://toaduser:toadpass@localhost:5451/toadstool"

engine = create_engine(CONN_STR, echo=True)

# https://docs.sqlalchemy.org/en/20/tutorial/dbapi_transactions.html

# with engine.connect() as conn:
#     result = conn.execute(text("select 'hello world'"))
#     print(result.all())

# with engine.connect() as conn:
# conn.execute(text("CREATE TABLE some_table (x int, y int)"))
# conn.execute(
#     text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x": 1, "y": 1}, {"x": 2, "y": 4}, {"x": 5, "y": 5}]
# )
# conn.commit()

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, y FROM some_table"))
#     for row in result:
#         print(f"x: {row.x}  y: {row.y}")


# ORM stuff
# from sqlalchemy.orm import Session

# with Session(engine) as session:
#     result = session.execute(
#         text("UPDATE some_table SET y=:y WHERE x=:x"),
#         [{"x": 5, "y": 11}, {"x": 2, "y": 3}],
#     )
#     session.commit()

with engine.begin() as conn:
    # conn.execute(text("DELETE FROM some_table"))
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

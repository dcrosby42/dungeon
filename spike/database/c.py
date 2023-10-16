# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html
from typing import List, Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import ForeignKey, String, create_engine, Engine, select


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


def connect() -> Engine:
    CONN_STR = "postgresql+psycopg2://toaduser:toadpass@localhost:5451/toadstool"
    return create_engine(CONN_STR, echo=True)


def create_tables(engine):
    Base.metadata.create_all(engine)


def list_users(engine):
    with Session(engine) as session:
        for user in session.scalars(select(User)):
            print(user)


def list_users2(engine):
    with Session(engine) as session:
        for name, fullname in session.execute(select(User.name, User.fullname)):
            print(f"User {name} is named {fullname}")


def add_users(engine):
    session = Session(engine)
    session.add(User(name="lemmy", fullname="Lemmy Kilmister"))
    session.add(User(name="ozzy", fullname="Ozzy Osbourne"))
    session.flush()
    session.commit()


engine = connect()
# create_tables(engine)
# add_users(engine)
# list_users2(engine)
list_users(engine)
list_users2(engine)

# all_users = []
# with Session(engine) as session:
#     for row in session.execute(select(User)):
#         all_users.append(row)

# with Session(engine) as session:
#     for user in all_users:
#         print(f"Deleting: {user}")
#         session.delete(user)

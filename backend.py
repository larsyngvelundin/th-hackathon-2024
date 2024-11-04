import json
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

default_data = json.load(open("default_cards.json", "r"))


class Card(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hint: str = Field(index=True)
    command: str | None = Field(index=True, unique=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
# SessionDep.add(default_data[0])
# SessionDep.commit()
# SessionDep.refresh(default_data[0])

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        # Check if data already exists to avoid duplicates
        result = session.exec(select(Card)).first()
        if not result:  # If there's no data in the table, insert default data
            for card_data in default_data:
                card = Card(**card_data)
                session.add(card)
            session.commit()


@app.post("/cards/")
def create_card(card: Card, session: SessionDep) -> Card:
    session.add(card)
    session.commit()
    session.refresh(card)
    return card


@app.get("/cards/")
def read_cards(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Card]:
    cardes = session.exec(select(Card).offset(offset).limit(limit)).all()
    return cardes


@app.get("/cards/{card_id}")
def read_card(card_id: int, session: SessionDep) -> Card:
    card = session.get(Card, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="card not found")
    return card


@app.delete("/cards/{card_id}")
def delete_card(card_id: int, session: SessionDep):
    card = session.get(Card, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="card not found")
    session.delete(card)
    session.commit()
    return {"ok": True}

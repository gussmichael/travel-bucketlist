import os
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

DB_DIR = Path(os.environ.get("DB_DIR", str(Path(__file__).resolve().parent.parent / "data")))
DB_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite:///{DB_DIR / 'travel.db'}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

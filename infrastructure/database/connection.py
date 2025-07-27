from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from infrastructure.database.models import Base

DATABASE_URL = "sqlite:///./schedule.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
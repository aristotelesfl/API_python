from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

BASE_URL = "sqlite:///dataset_livros.db"
engine = create_engine(BASE_URL)
SessionLocal = sessionmaker(engine)

def get_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
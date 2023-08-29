from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel

app = FastAPI()

BASE_URL = "sqlite:///dataset_livros.db"

engine = create_engine(BASE_URL)

SessionLocal = sessionmaker(engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, nullable=False)

Base.metadata.create_all(engine)

def get_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserBase(BaseModel):
    username: str

@app.post("/user")
def create_user(user: UserBase, db: Session = Depends(get_bd)):
    db_user = User(username = user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users")
def read_users(db: Session = Depends(get_bd)):
    users = db.query(User).all()
    return {"Users": users}

@app.get(("/user/{id_user}"))
def read_user(id_user: int, db: Session = Depends(get_bd)):
    user = db.query(User).filter(User.id == id_user).all()
    return {"User": user}
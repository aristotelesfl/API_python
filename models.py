from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer

Base = declarative_base()

class Livros(Base):
    __tablename__ = "Livros"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String, nullable=False)
    descricao: str = Column(String, nullable=False)
    numero_paginas: int = Column(Integer, nullable=False)
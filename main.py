from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
from core import LivroCore
from models import Livros
from schemas import LivrosCreate, LivrosResponse, LivrosUpdate

app = FastAPI()

# Cria as tabelas no banco de dados
Livros.metadata.create_all(bind=engine)

@app.post("/livros/", response_model=LivrosResponse)
def create_livro(livro: LivrosCreate, db: Session = Depends(get_db)):
    return LivroCore.create_book(db, Livros(**livro.dict()))

@app.get("/livros/", response_model=list[LivrosResponse])
def read_livros(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return LivroCore.get_books(db, skip, limit)

@app.get("/livros/{livro_id}", response_model=LivrosResponse)
def read_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = LivroCore.get_book(db, livro_id)
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

@app.put("/livros/{livro_id}", response_model=LivrosResponse)
def update_livro(livro_id: int, livro: LivrosUpdate, db: Session = Depends(get_db)):
    existing_livro = LivroCore.get_book(db, livro_id)
    if existing_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    new_data = livro.dict()
    return LivroCore.update_book(db, livro_id, new_data)

@app.delete("/livros/{livro_id}", response_model=LivrosResponse)
def delete_livro(livro_id: int, db: Session = Depends(get_db)):
    existing_livro = LivroCore.get_book(db, livro_id)
    if existing_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return LivroCore.delete_book(db, livro_id)

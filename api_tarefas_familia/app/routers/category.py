from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/", response_model=List[CategoryResponse])
def listar_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todas as categorias"""
    categorias = db.query(Category).offset(skip).limit(limit).all()
    return categorias


@router.get("/{categoria_id}", response_model=CategoryResponse)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """Obtém uma categoria pelo ID"""
    categoria = db.query(Category).filter(Category.category_id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(categoria: CategoryCreate, db: Session = Depends(get_db)):
    """Cria uma nova categoria"""
    db_categoria = Category(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


@router.put("/{categoria_id}", response_model=CategoryResponse)
def atualizar_categoria(categoria_id: int, categoria: CategoryUpdate, db: Session = Depends(get_db)):
    """Atualiza uma categoria existente"""
    db_categoria = db.query(Category).filter(Category.category_id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    update_data = categoria.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_categoria, key, value)

    db.commit()
    db.refresh(db_categoria)
    return db_categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """Deleta uma categoria"""
    db_categoria = db.query(Category).filter(Category.category_id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db.delete(db_categoria)
    db.commit()
    return None

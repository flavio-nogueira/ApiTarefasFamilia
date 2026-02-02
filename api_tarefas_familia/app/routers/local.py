from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.local import Local
from app.schemas.local import LocalCreate, LocalUpdate, LocalResponse

router = APIRouter(prefix="/locais", tags=["Locais"])


@router.get("/", response_model=List[LocalResponse])
def listar_locais(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os locais"""
    locais = db.query(Local).offset(skip).limit(limit).all()
    return locais


@router.get("/{local_id}", response_model=LocalResponse)
def obter_local(local_id: int, db: Session = Depends(get_db)):
    """Obtém um local pelo ID"""
    local = db.query(Local).filter(Local.idLocal == local_id).first()
    if not local:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return local


@router.post("/", response_model=LocalResponse, status_code=status.HTTP_201_CREATED)
def criar_local(local: LocalCreate, db: Session = Depends(get_db)):
    """Cria um novo local"""
    db_local = Local(**local.model_dump())
    db.add(db_local)
    db.commit()
    db.refresh(db_local)
    return db_local


@router.put("/{local_id}", response_model=LocalResponse)
def atualizar_local(local_id: int, local: LocalUpdate, db: Session = Depends(get_db)):
    """Atualiza um local existente"""
    db_local = db.query(Local).filter(Local.idLocal == local_id).first()
    if not db_local:
        raise HTTPException(status_code=404, detail="Local não encontrado")

    update_data = local.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_local, key, value)

    db.commit()
    db.refresh(db_local)
    return db_local


@router.delete("/{local_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_local(local_id: int, db: Session = Depends(get_db)):
    """Deleta um local"""
    db_local = db.query(Local).filter(Local.idLocal == local_id).first()
    if not db_local:
        raise HTTPException(status_code=404, detail="Local não encontrado")

    db.delete(db_local)
    db.commit()
    return None

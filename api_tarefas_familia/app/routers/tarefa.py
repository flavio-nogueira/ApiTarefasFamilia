from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.tarefa import Tarefa
from app.schemas.tarefa import TarefaCreate, TarefaUpdate, TarefaResponse

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


@router.get("/", response_model=List[TarefaResponse])
def listar_tarefas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todas as tarefas"""
    tarefas = db.query(Tarefa).offset(skip).limit(limit).all()
    return tarefas


@router.get("/{tarefa_id}", response_model=TarefaResponse)
def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    """Obtém uma tarefa pelo ID"""
    tarefa = db.query(Tarefa).filter(Tarefa.idTarefa == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa


@router.get("/local/{local_id}", response_model=List[TarefaResponse])
def listar_tarefas_por_local(local_id: int, db: Session = Depends(get_db)):
    """Lista todas as tarefas de um local específico"""
    tarefas = db.query(Tarefa).filter(Tarefa.Local_idLocal == local_id).all()
    return tarefas


@router.post("/", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    """Cria uma nova tarefa"""
    db_tarefa = Tarefa(**tarefa.model_dump())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


@router.put("/{tarefa_id}", response_model=TarefaResponse)
def atualizar_tarefa(tarefa_id: int, tarefa: TarefaUpdate, db: Session = Depends(get_db)):
    """Atualiza uma tarefa existente"""
    db_tarefa = db.query(Tarefa).filter(Tarefa.idTarefa == tarefa_id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    update_data = tarefa.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tarefa, key, value)

    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    """Deleta uma tarefa"""
    db_tarefa = db.query(Tarefa).filter(Tarefa.idTarefa == tarefa_id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(db_tarefa)
    db.commit()
    return None

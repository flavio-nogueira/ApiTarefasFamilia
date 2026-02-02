from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.tarefa_usuario import TarefaUsuario
from app.schemas.tarefa_usuario import TarefaUsuarioCreate, TarefaUsuarioUpdate, TarefaUsuarioResponse

router = APIRouter(prefix="/tarefas-usuarios", tags=["Tarefas-Usuários"])


@router.get("/", response_model=List[TarefaUsuarioResponse])
def listar_atribuicoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todas as atribuições de tarefas a usuários"""
    atribuicoes = db.query(TarefaUsuario).offset(skip).limit(limit).all()
    return atribuicoes


@router.get("/{atribuicao_id}", response_model=TarefaUsuarioResponse)
def obter_atribuicao(atribuicao_id: int, db: Session = Depends(get_db)):
    """Obtém uma atribuição pelo ID"""
    atribuicao = db.query(TarefaUsuario).filter(TarefaUsuario.id == atribuicao_id).first()
    if not atribuicao:
        raise HTTPException(status_code=404, detail="Atribuição não encontrada")
    return atribuicao


@router.get("/usuario/{usuario_id}", response_model=List[TarefaUsuarioResponse])
def listar_tarefas_do_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Lista todas as tarefas atribuídas a um usuário"""
    atribuicoes = db.query(TarefaUsuario).filter(
        TarefaUsuario.usuario_idUsuario == usuario_id
    ).all()
    return atribuicoes


@router.get("/tarefa/{tarefa_id}", response_model=List[TarefaUsuarioResponse])
def listar_usuarios_da_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    """Lista todos os usuários atribuídos a uma tarefa"""
    atribuicoes = db.query(TarefaUsuario).filter(
        TarefaUsuario.Tarefa_idTarefa == tarefa_id
    ).all()
    return atribuicoes


@router.get("/pendentes/usuario/{usuario_id}", response_model=List[TarefaUsuarioResponse])
def listar_tarefas_pendentes_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Lista todas as tarefas pendentes de um usuário"""
    atribuicoes = db.query(TarefaUsuario).filter(
        TarefaUsuario.usuario_idUsuario == usuario_id,
        TarefaUsuario.Feito == 0
    ).all()
    return atribuicoes


@router.post("/", response_model=TarefaUsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_atribuicao(atribuicao: TarefaUsuarioCreate, db: Session = Depends(get_db)):
    """Cria uma nova atribuição de tarefa a usuário"""
    db_atribuicao = TarefaUsuario(**atribuicao.model_dump())
    db.add(db_atribuicao)
    db.commit()
    db.refresh(db_atribuicao)
    return db_atribuicao


@router.put("/{atribuicao_id}", response_model=TarefaUsuarioResponse)
def atualizar_atribuicao(atribuicao_id: int, atribuicao: TarefaUsuarioUpdate, db: Session = Depends(get_db)):
    """Atualiza uma atribuição existente"""
    db_atribuicao = db.query(TarefaUsuario).filter(TarefaUsuario.id == atribuicao_id).first()
    if not db_atribuicao:
        raise HTTPException(status_code=404, detail="Atribuição não encontrada")

    update_data = atribuicao.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_atribuicao, key, value)

    db.commit()
    db.refresh(db_atribuicao)
    return db_atribuicao


@router.patch("/{atribuicao_id}/concluir", response_model=TarefaUsuarioResponse)
def concluir_tarefa(atribuicao_id: int, db: Session = Depends(get_db)):
    """Marca uma tarefa como concluída"""
    db_atribuicao = db.query(TarefaUsuario).filter(TarefaUsuario.id == atribuicao_id).first()
    if not db_atribuicao:
        raise HTTPException(status_code=404, detail="Atribuição não encontrada")

    db_atribuicao.Feito = 1
    db_atribuicao.DataHoraConclusao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.commit()
    db.refresh(db_atribuicao)
    return db_atribuicao


@router.delete("/{atribuicao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_atribuicao(atribuicao_id: int, db: Session = Depends(get_db)):
    """Deleta uma atribuição"""
    db_atribuicao = db.query(TarefaUsuario).filter(TarefaUsuario.id == atribuicao_id).first()
    if not db_atribuicao:
        raise HTTPException(status_code=404, detail="Atribuição não encontrada")

    db.delete(db_atribuicao)
    db.commit()
    return None

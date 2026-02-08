from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.tarefa_email import TarefaEmail
from app.models.tarefa import Tarefa
from app.schemas.tarefa_email import TarefaEmailCreate, TarefaEmailUpdate, TarefaEmailResponse, TarefaEmailDetalhadaResponse

router = APIRouter(prefix="/tarefas-email", tags=["Tarefas-Email"])


@router.get("/", response_model=List[TarefaEmailResponse])
def listar_tarefas_email(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todas as tarefas vinculadas a emails"""
    tarefas = db.query(TarefaEmail).offset(skip).limit(limit).all()
    return tarefas


@router.get("/{id}", response_model=TarefaEmailResponse)
def obter_tarefa_email(id: int, db: Session = Depends(get_db)):
    """Obtem uma tarefa-email pelo ID"""
    tarefa = db.query(TarefaEmail).filter(TarefaEmail.id == id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Registro nao encontrado")
    return tarefa


@router.get("/email/{email}", response_model=List[TarefaEmailDetalhadaResponse])
def listar_tarefas_por_email(email: str, db: Session = Depends(get_db)):
    """Lista todas as tarefas de um email especifico com nome e descricao da tarefa"""
    resultados = db.query(
        TarefaEmail.id,
        TarefaEmail.Tarefa_idTarefa,
        Tarefa.Tarefa.label('Tarefa_nome'),
        Tarefa.Descricao.label('Tarefa_descricao'),
        TarefaEmail.email,
        TarefaEmail.Data,
        TarefaEmail.Periodo,
        TarefaEmail.Feito,
        TarefaEmail.DataHoraConclusao
    ).join(Tarefa, TarefaEmail.Tarefa_idTarefa == Tarefa.idTarefa).filter(
        TarefaEmail.email == email
    ).all()

    return [
        TarefaEmailDetalhadaResponse(
            id=r.id,
            Tarefa_idTarefa=r.Tarefa_idTarefa,
            Tarefa_nome=r.Tarefa_nome,
            Tarefa_descricao=r.Tarefa_descricao,
            email=r.email,
            Data=r.Data,
            Periodo=r.Periodo,
            Feito=r.Feito,
            DataHoraConclusao=r.DataHoraConclusao
        ) for r in resultados
    ]


@router.get("/email/{email}/pendentes", response_model=List[TarefaEmailResponse])
def listar_tarefas_pendentes_email(email: str, db: Session = Depends(get_db)):
    """Lista todas as tarefas pendentes de um email"""
    tarefas = db.query(TarefaEmail).filter(
        TarefaEmail.email == email,
        TarefaEmail.Feito == 0
    ).all()
    return tarefas


@router.get("/email/{email}/detalhado", response_model=List[TarefaEmailDetalhadaResponse])
def listar_tarefas_detalhadas_por_email(email: str, db: Session = Depends(get_db)):
    """Lista todas as tarefas de um email com informacoes detalhadas da tarefa"""
    resultados = db.query(
        TarefaEmail.id,
        TarefaEmail.Tarefa_idTarefa,
        Tarefa.Tarefa.label('Tarefa_nome'),
        Tarefa.Descricao.label('Tarefa_descricao'),
        TarefaEmail.email,
        TarefaEmail.Data,
        TarefaEmail.Periodo,
        TarefaEmail.Feito,
        TarefaEmail.DataHoraConclusao
    ).join(Tarefa, TarefaEmail.Tarefa_idTarefa == Tarefa.idTarefa).filter(
        TarefaEmail.email == email
    ).all()

    return [
        TarefaEmailDetalhadaResponse(
            id=r.id,
            Tarefa_idTarefa=r.Tarefa_idTarefa,
            Tarefa_nome=r.Tarefa_nome,
            Tarefa_descricao=r.Tarefa_descricao,
            email=r.email,
            Data=r.Data,
            Periodo=r.Periodo,
            Feito=r.Feito,
            DataHoraConclusao=r.DataHoraConclusao
        ) for r in resultados
    ]


@router.post("/", response_model=TarefaEmailResponse, status_code=status.HTTP_201_CREATED)
def criar_tarefa_email(tarefa: TarefaEmailCreate, db: Session = Depends(get_db)):
    """Vincula uma tarefa a um email"""
    db_tarefa = TarefaEmail(**tarefa.model_dump())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


@router.put("/{id}", response_model=TarefaEmailResponse)
def atualizar_tarefa_email(id: int, tarefa: TarefaEmailUpdate, db: Session = Depends(get_db)):
    """Atualiza uma tarefa-email"""
    db_tarefa = db.query(TarefaEmail).filter(TarefaEmail.id == id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Registro nao encontrado")

    update_data = tarefa.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tarefa, key, value)

    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


@router.patch("/{id}/concluir", response_model=TarefaEmailResponse)
def concluir_tarefa_email(id: int, db: Session = Depends(get_db)):
    """Marca uma tarefa como concluida"""
    db_tarefa = db.query(TarefaEmail).filter(TarefaEmail.id == id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Registro nao encontrado")

    db_tarefa.Feito = 1
    db_tarefa.DataHoraConclusao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa_email(id: int, db: Session = Depends(get_db)):
    """Deleta uma tarefa-email"""
    db_tarefa = db.query(TarefaEmail).filter(TarefaEmail.id == id).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Registro nao encontrado")

    db.delete(db_tarefa)
    db.commit()
    return None

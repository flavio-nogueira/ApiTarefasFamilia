from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime

from app.database import get_db
from app.models.tarefa_email import TarefaEmail
from app.models.tarefa_usuario import TarefaUsuario
from app.models.tarefa import Tarefa
from app.models.usuario import Usuario
from app.models.tarefa_conclusao_diaria import TarefaConclusaoDiaria
from app.schemas.tarefa_conclusao_diaria import (
    TarefaDoDiaResponse,
    TarefaDoDiaUsuarioResponse,
    ConclusaoDiariaResponse,
    HistoricoConclusaoResponse,
)

router = APIRouter(prefix="/tarefas-dia", tags=["Tarefas-Dia"])


# ========================
# ENDPOINTS POR EMAIL
# ========================

@router.get("/email/{email}", response_model=List[TarefaDoDiaResponse])
def listar_tarefas_do_dia_email(email: str, db: Session = Depends(get_db)):
    """Lista todas as tarefas do dia para um email, com status de conclusao"""
    hoje = date.today()

    tarefas_email = db.query(
        TarefaEmail.id.label('tarefa_email_id'),
        TarefaEmail.Tarefa_idTarefa,
        Tarefa.Tarefa.label('Tarefa_nome'),
        Tarefa.Descricao.label('Tarefa_descricao'),
        TarefaEmail.email,
        TarefaEmail.Periodo,
    ).join(Tarefa, TarefaEmail.Tarefa_idTarefa == Tarefa.idTarefa).filter(
        TarefaEmail.email == email
    ).all()

    resultado = []
    for t in tarefas_email:
        conclusao = db.query(TarefaConclusaoDiaria).filter(
            TarefaConclusaoDiaria.tarefa_email_id == t.tarefa_email_id,
            TarefaConclusaoDiaria.data == hoje
        ).first()

        resultado.append(TarefaDoDiaResponse(
            tarefa_email_id=t.tarefa_email_id,
            Tarefa_idTarefa=t.Tarefa_idTarefa,
            Tarefa_nome=t.Tarefa_nome,
            Tarefa_descricao=t.Tarefa_descricao,
            email=t.email,
            Periodo=t.Periodo,
            data_hoje=hoje,
            concluida=conclusao is not None,
            data_hora_conclusao=conclusao.data_hora_conclusao if conclusao else None
        ))

    return resultado


@router.post("/email/{tarefa_email_id}/concluir", response_model=ConclusaoDiariaResponse, status_code=status.HTTP_201_CREATED)
def concluir_tarefa_dia_email(tarefa_email_id: int, db: Session = Depends(get_db)):
    """Marca uma tarefa (por email) como concluida no dia de hoje"""
    tarefa_email = db.query(TarefaEmail).filter(TarefaEmail.id == tarefa_email_id).first()
    if not tarefa_email:
        raise HTTPException(status_code=404, detail="Tarefa email nao encontrada")

    hoje = date.today()

    existente = db.query(TarefaConclusaoDiaria).filter(
        TarefaConclusaoDiaria.tarefa_email_id == tarefa_email_id,
        TarefaConclusaoDiaria.data == hoje
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Tarefa ja foi concluida hoje")

    conclusao = TarefaConclusaoDiaria(
        tarefa_email_id=tarefa_email_id,
        data=hoje,
        data_hora_conclusao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status=1
    )
    db.add(conclusao)
    db.commit()
    db.refresh(conclusao)
    return conclusao


@router.delete("/email/{tarefa_email_id}/desfazer", status_code=status.HTTP_204_NO_CONTENT)
def desfazer_conclusao_dia_email(tarefa_email_id: int, db: Session = Depends(get_db)):
    """Remove a conclusao do dia para tarefa por email"""
    hoje = date.today()

    conclusao = db.query(TarefaConclusaoDiaria).filter(
        TarefaConclusaoDiaria.tarefa_email_id == tarefa_email_id,
        TarefaConclusaoDiaria.data == hoje
    ).first()

    if not conclusao:
        raise HTTPException(status_code=404, detail="Nenhuma conclusao encontrada para hoje")

    db.delete(conclusao)
    db.commit()
    return None


@router.get("/email/{email}/historico", response_model=List[HistoricoConclusaoResponse])
def historico_conclusoes_email(
    email: str,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Historico de conclusoes de tarefas por email"""
    query = db.query(
        TarefaConclusaoDiaria.id,
        TarefaConclusaoDiaria.tarefa_email_id,
        Tarefa.Tarefa.label('Tarefa_nome'),
        Tarefa.Descricao.label('Tarefa_descricao'),
        TarefaEmail.email,
        TarefaConclusaoDiaria.data,
        TarefaConclusaoDiaria.data_hora_conclusao,
        TarefaConclusaoDiaria.status,
    ).join(TarefaEmail, TarefaConclusaoDiaria.tarefa_email_id == TarefaEmail.id
    ).join(Tarefa, TarefaEmail.Tarefa_idTarefa == Tarefa.idTarefa
    ).filter(TarefaEmail.email == email)

    if data_inicio:
        query = query.filter(TarefaConclusaoDiaria.data >= data_inicio)
    if data_fim:
        query = query.filter(TarefaConclusaoDiaria.data <= data_fim)

    query = query.order_by(TarefaConclusaoDiaria.data.desc())

    resultados = query.all()

    return [
        HistoricoConclusaoResponse(
            id=r.id,
            tarefa_email_id=r.tarefa_email_id,
            Tarefa_nome=r.Tarefa_nome,
            Tarefa_descricao=r.Tarefa_descricao,
            email=r.email,
            data=r.data,
            data_hora_conclusao=r.data_hora_conclusao,
            status=r.status
        ) for r in resultados
    ]


# ========================
# ENDPOINTS POR USUARIO
# ========================

@router.get("/usuario/{usuario_id}", response_model=List[TarefaDoDiaUsuarioResponse])
def listar_tarefas_do_dia_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Lista todas as tarefas do dia para um usuario, com status de conclusao"""
    hoje = date.today()

    tarefas_usuario = db.query(
        TarefaUsuario.id.label('tarefa_usuario_id'),
        TarefaUsuario.Tarefa_idTarefa,
        Tarefa.Tarefa.label('Tarefa_nome'),
        Tarefa.Descricao.label('Tarefa_descricao'),
        TarefaUsuario.usuario_idUsuario,
        Usuario.Nome.label('Nome_usuario'),
        TarefaUsuario.Periodo,
    ).join(Tarefa, TarefaUsuario.Tarefa_idTarefa == Tarefa.idTarefa
    ).join(Usuario, TarefaUsuario.usuario_idUsuario == Usuario.idUsuario
    ).filter(
        TarefaUsuario.usuario_idUsuario == usuario_id
    ).all()

    resultado = []
    for t in tarefas_usuario:
        conclusao = db.query(TarefaConclusaoDiaria).filter(
            TarefaConclusaoDiaria.tarefa_usuario_id == t.tarefa_usuario_id,
            TarefaConclusaoDiaria.data == hoje
        ).first()

        resultado.append(TarefaDoDiaUsuarioResponse(
            tarefa_usuario_id=t.tarefa_usuario_id,
            Tarefa_idTarefa=t.Tarefa_idTarefa,
            Tarefa_nome=t.Tarefa_nome,
            Tarefa_descricao=t.Tarefa_descricao,
            usuario_idUsuario=t.usuario_idUsuario,
            Nome_usuario=t.Nome_usuario,
            Periodo=t.Periodo,
            data_hoje=hoje,
            concluida=conclusao is not None,
            data_hora_conclusao=conclusao.data_hora_conclusao if conclusao else None
        ))

    return resultado


@router.post("/usuario/{tarefa_usuario_id}/concluir", response_model=ConclusaoDiariaResponse, status_code=status.HTTP_201_CREATED)
def concluir_tarefa_dia_usuario(tarefa_usuario_id: int, db: Session = Depends(get_db)):
    """Marca uma tarefa (por usuario) como concluida no dia de hoje"""
    tarefa_usr = db.query(TarefaUsuario).filter(TarefaUsuario.id == tarefa_usuario_id).first()
    if not tarefa_usr:
        raise HTTPException(status_code=404, detail="Tarefa usuario nao encontrada")

    hoje = date.today()

    existente = db.query(TarefaConclusaoDiaria).filter(
        TarefaConclusaoDiaria.tarefa_usuario_id == tarefa_usuario_id,
        TarefaConclusaoDiaria.data == hoje
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Tarefa ja foi concluida hoje")

    conclusao = TarefaConclusaoDiaria(
        tarefa_usuario_id=tarefa_usuario_id,
        data=hoje,
        data_hora_conclusao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status=1
    )
    db.add(conclusao)
    db.commit()
    db.refresh(conclusao)
    return conclusao


@router.delete("/usuario/{tarefa_usuario_id}/desfazer", status_code=status.HTTP_204_NO_CONTENT)
def desfazer_conclusao_dia_usuario(tarefa_usuario_id: int, db: Session = Depends(get_db)):
    """Remove a conclusao do dia para tarefa por usuario"""
    hoje = date.today()

    conclusao = db.query(TarefaConclusaoDiaria).filter(
        TarefaConclusaoDiaria.tarefa_usuario_id == tarefa_usuario_id,
        TarefaConclusaoDiaria.data == hoje
    ).first()

    if not conclusao:
        raise HTTPException(status_code=404, detail="Nenhuma conclusao encontrada para hoje")

    db.delete(conclusao)
    db.commit()
    return None


@router.get("/usuario/{usuario_id}/historico", response_model=List[HistoricoConclusaoResponse])
def historico_conclusoes_usuario(
    usuario_id: int,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Historico de conclusoes de tarefas por usuario"""
    query = db.query(
        TarefaConclusaoDiaria.id,
        TarefaConclusaoDiaria.tarefa_usuario_id,
        Tarefa.Tarefa.label('Tarefa_nome'),
        Tarefa.Descricao.label('Tarefa_descricao'),
        Usuario.Nome.label('Nome_usuario'),
        TarefaConclusaoDiaria.data,
        TarefaConclusaoDiaria.data_hora_conclusao,
        TarefaConclusaoDiaria.status,
    ).join(TarefaUsuario, TarefaConclusaoDiaria.tarefa_usuario_id == TarefaUsuario.id
    ).join(Tarefa, TarefaUsuario.Tarefa_idTarefa == Tarefa.idTarefa
    ).join(Usuario, TarefaUsuario.usuario_idUsuario == Usuario.idUsuario
    ).filter(TarefaUsuario.usuario_idUsuario == usuario_id)

    if data_inicio:
        query = query.filter(TarefaConclusaoDiaria.data >= data_inicio)
    if data_fim:
        query = query.filter(TarefaConclusaoDiaria.data <= data_fim)

    query = query.order_by(TarefaConclusaoDiaria.data.desc())

    resultados = query.all()

    return [
        HistoricoConclusaoResponse(
            id=r.id,
            tarefa_usuario_id=r.tarefa_usuario_id,
            Tarefa_nome=r.Tarefa_nome,
            Tarefa_descricao=r.Tarefa_descricao,
            Nome_usuario=r.Nome_usuario,
            data=r.data,
            data_hora_conclusao=r.data_hora_conclusao,
            status=r.status
        ) for r in resultados
    ]

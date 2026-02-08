from pydantic import BaseModel
from typing import Optional
from datetime import date


class TarefaDoDiaResponse(BaseModel):
    tarefa_email_id: int
    Tarefa_idTarefa: int
    Tarefa_nome: str
    Tarefa_descricao: Optional[str] = None
    email: str
    Periodo: Optional[str] = None
    data_hoje: date
    concluida: bool
    data_hora_conclusao: Optional[str] = None

    class Config:
        from_attributes = True


class TarefaDoDiaUsuarioResponse(BaseModel):
    tarefa_usuario_id: int
    Tarefa_idTarefa: int
    Tarefa_nome: str
    Tarefa_descricao: Optional[str] = None
    usuario_idUsuario: int
    Nome_usuario: str
    Periodo: Optional[str] = None
    data_hoje: date
    concluida: bool
    data_hora_conclusao: Optional[str] = None

    class Config:
        from_attributes = True


class ConclusaoDiariaResponse(BaseModel):
    id: int
    tarefa_email_id: Optional[int] = None
    tarefa_usuario_id: Optional[int] = None
    data: date
    data_hora_conclusao: str
    status: int

    class Config:
        from_attributes = True


class HistoricoConclusaoResponse(BaseModel):
    id: int
    tarefa_email_id: Optional[int] = None
    tarefa_usuario_id: Optional[int] = None
    Tarefa_nome: str
    Tarefa_descricao: Optional[str] = None
    email: Optional[str] = None
    Nome_usuario: Optional[str] = None
    data: date
    data_hora_conclusao: str
    status: int

    class Config:
        from_attributes = True

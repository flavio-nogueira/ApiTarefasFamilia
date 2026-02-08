from pydantic import BaseModel
from typing import Optional
from datetime import date


class TarefaEmailBase(BaseModel):
    Tarefa_idTarefa: int
    email: str
    Data: Optional[date] = None
    Periodo: Optional[str] = None
    Feito: Optional[int] = 0
    DataHoraConclusao: Optional[str] = None


class TarefaEmailCreate(TarefaEmailBase):
    pass


class TarefaEmailUpdate(BaseModel):
    Tarefa_idTarefa: Optional[int] = None
    email: Optional[str] = None
    Data: Optional[date] = None
    Periodo: Optional[str] = None
    Feito: Optional[int] = None
    DataHoraConclusao: Optional[str] = None


class TarefaEmailResponse(TarefaEmailBase):
    id: int

    class Config:
        from_attributes = True


class TarefaEmailDetalhadaResponse(BaseModel):
    id: int
    Tarefa_idTarefa: int
    Tarefa_nome: str
    Tarefa_descricao: Optional[str] = None
    email: str
    Data: Optional[date] = None
    Periodo: Optional[str] = None
    Feito: int
    DataHoraConclusao: Optional[str] = None

    class Config:
        from_attributes = True

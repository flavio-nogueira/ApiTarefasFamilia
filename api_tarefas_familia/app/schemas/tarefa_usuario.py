from pydantic import BaseModel
from typing import Optional
from datetime import date


class TarefaUsuarioBase(BaseModel):
    usuario_idUsuario: int
    Tarefa_idTarefa: int
    Data: Optional[date] = None
    Periodo: Optional[str] = None
    Feito: Optional[int] = 0
    DataHoraConclusao: Optional[str] = None


class TarefaUsuarioCreate(TarefaUsuarioBase):
    pass


class TarefaUsuarioUpdate(BaseModel):
    usuario_idUsuario: Optional[int] = None
    Tarefa_idTarefa: Optional[int] = None
    Data: Optional[date] = None
    Periodo: Optional[str] = None
    Feito: Optional[int] = None
    DataHoraConclusao: Optional[str] = None


class TarefaUsuarioResponse(TarefaUsuarioBase):
    id: int

    class Config:
        from_attributes = True

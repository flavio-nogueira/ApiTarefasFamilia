from pydantic import BaseModel
from typing import Optional


class TarefaBase(BaseModel):
    Tarefa: str
    Descricao: Optional[str] = None
    Local_idLocal: Optional[int] = None


class TarefaCreate(TarefaBase):
    pass


class TarefaUpdate(BaseModel):
    Tarefa: Optional[str] = None
    Descricao: Optional[str] = None
    Local_idLocal: Optional[int] = None


class TarefaResponse(TarefaBase):
    idTarefa: int

    class Config:
        from_attributes = True

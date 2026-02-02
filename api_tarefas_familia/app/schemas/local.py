from pydantic import BaseModel
from typing import Optional


class LocalBase(BaseModel):
    Descricao: str


class LocalCreate(LocalBase):
    pass


class LocalUpdate(BaseModel):
    Descricao: Optional[str] = None


class LocalResponse(LocalBase):
    idLocal: int

    class Config:
        from_attributes = True

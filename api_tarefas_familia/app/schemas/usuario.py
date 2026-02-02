from pydantic import BaseModel
from typing import Optional


class UsuarioBase(BaseModel):
    Nome: str
    login: str


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioUpdate(BaseModel):
    Nome: Optional[str] = None
    login: Optional[str] = None
    senha: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    idUsuario: int

    class Config:
        from_attributes = True

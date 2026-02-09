from pydantic import BaseModel
from typing import Optional


class UsuarioBase(BaseModel):
    Nome: str
    login: str
    email: Optional[str] = None
    tipo_conta: Optional[str] = "simples"


class UsuarioCreate(BaseModel):
    """Cadastro simples com login e senha"""
    Nome: str
    login: str
    senha: str
    email: Optional[str] = None
    tipo_conta: Optional[str] = "simples"


class UsuarioGmailCreate(BaseModel):
    """Cadastro via conta Gmail (sem senha)"""
    Nome: str
    email: str
    tipo_conta: Optional[str] = "gmail"


class UsuarioUpdate(BaseModel):
    Nome: Optional[str] = None
    login: Optional[str] = None
    senha: Optional[str] = None
    email: Optional[str] = None
    tipo_conta: Optional[str] = None


class UsuarioResponse(BaseModel):
    idUsuario: int
    Nome: str
    login: str
    email: Optional[str] = None
    tipo_conta: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Login simples com login e senha"""
    login: str
    senha: str


class LoginGmailRequest(BaseModel):
    """Login via conta Gmail (apenas email)"""
    email: str


class LoginResponse(BaseModel):
    sucesso: bool
    mensagem: str
    usuario: Optional[UsuarioResponse] = None

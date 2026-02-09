from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import hashlib

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import (
    UsuarioCreate, UsuarioGmailCreate, UsuarioUpdate, UsuarioResponse,
    LoginRequest, LoginGmailRequest, LoginResponse
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/login", response_model=LoginResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    """
    Login simples com login e senha.
    """
    usuario = db.query(Usuario).filter(Usuario.login == dados.login).first()

    if not usuario:
        return LoginResponse(
            sucesso=False,
            mensagem="Usuario nao encontrado",
            usuario=None
        )

    if usuario.tipo_conta == "gmail":
        return LoginResponse(
            sucesso=False,
            mensagem="Este usuario usa conta Gmail. Use o login por Gmail.",
            usuario=None
        )

    senha_hash = hash_senha(dados.senha)
    if usuario.senha != senha_hash:
        return LoginResponse(
            sucesso=False,
            mensagem="Senha invalida",
            usuario=None
        )

    return LoginResponse(
        sucesso=True,
        mensagem="Login realizado com sucesso",
        usuario=UsuarioResponse.model_validate(usuario)
    )


@router.post("/login/gmail", response_model=LoginResponse)
def login_gmail(dados: LoginGmailRequest, db: Session = Depends(get_db)):
    """
    Login via conta Gmail. Busca pelo email.
    Se o usuario nao existir, cria automaticamente.
    """
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if not usuario:
        # Cria usuario automaticamente com dados do Gmail
        nome = dados.email.split("@")[0].replace(".", " ").title()
        usuario = Usuario(
            Nome=nome,
            login=dados.email,
            email=dados.email,
            tipo_conta="gmail"
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return LoginResponse(
            sucesso=True,
            mensagem="Usuario criado e login realizado com sucesso",
            usuario=UsuarioResponse.model_validate(usuario)
        )

    if usuario.tipo_conta != "gmail":
        return LoginResponse(
            sucesso=False,
            mensagem="Este email esta vinculado a uma conta simples. Use login e senha.",
            usuario=None
        )

    return LoginResponse(
        sucesso=True,
        mensagem="Login realizado com sucesso",
        usuario=UsuarioResponse.model_validate(usuario)
    )


def hash_senha(senha: str) -> str:
    """Gera hash da senha usando SHA-256"""
    return hashlib.sha256(senha.encode()).hexdigest()


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os usuarios"""
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtem um usuario pelo ID"""
    usuario = db.query(Usuario).filter(Usuario.idUsuario == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return usuario


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Cadastro simples com login e senha"""
    existing = db.query(Usuario).filter(Usuario.login == usuario.login).first()
    if existing:
        raise HTTPException(status_code=400, detail="Login ja cadastrado")

    usuario_data = usuario.model_dump()
    usuario_data["senha"] = hash_senha(usuario_data["senha"])
    usuario_data["tipo_conta"] = "simples"

    db_usuario = Usuario(**usuario_data)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.post("/gmail", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario_gmail(usuario: UsuarioGmailCreate, db: Session = Depends(get_db)):
    """Cadastro via conta Gmail (sem senha)"""
    existing = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ja cadastrado")

    db_usuario = Usuario(
        Nome=usuario.Nome,
        login=usuario.email,
        email=usuario.email,
        tipo_conta="gmail"
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    """Atualiza um usuario existente"""
    db_usuario = db.query(Usuario).filter(Usuario.idUsuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    update_data = usuario.model_dump(exclude_unset=True)

    if "senha" in update_data and update_data["senha"]:
        update_data["senha"] = hash_senha(update_data["senha"])

    for key, value in update_data.items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Deleta um usuario"""
    db_usuario = db.query(Usuario).filter(Usuario.idUsuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    db.delete(db_usuario)
    db.commit()
    return None

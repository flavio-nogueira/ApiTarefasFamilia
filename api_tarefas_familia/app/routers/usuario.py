from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import hashlib

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, LoginRequest, LoginResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("/login", response_model=LoginResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    """
    Realiza login do usuario.
    Recebe login e senha, retorna dados do usuario se autenticado.
    """
    # Busca usuario pelo login
    usuario = db.query(Usuario).filter(Usuario.login == dados.login).first()

    if not usuario:
        return LoginResponse(
            sucesso=False,
            mensagem="Usuario nao encontrado",
            usuario=None
        )

    # Verifica senha
    senha_hash = hash_senha(dados.senha)
    if usuario.senha != senha_hash:
        return LoginResponse(
            sucesso=False,
            mensagem="Senha invalida",
            usuario=None
        )

    # Login bem sucedido
    return LoginResponse(
        sucesso=True,
        mensagem="Login realizado com sucesso",
        usuario=UsuarioResponse(
            idUsuario=usuario.idUsuario,
            Nome=usuario.Nome,
            login=usuario.login
        )
    )


def hash_senha(senha: str) -> str:
    """Gera hash da senha usando SHA-256"""
    return hashlib.sha256(senha.encode()).hexdigest()


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os usuários"""
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtém um usuário pelo ID"""
    usuario = db.query(Usuario).filter(Usuario.idUsuario == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário"""
    # Verifica se o login já existe
    existing = db.query(Usuario).filter(Usuario.login == usuario.login).first()
    if existing:
        raise HTTPException(status_code=400, detail="Login já cadastrado")

    usuario_data = usuario.model_dump()
    usuario_data["senha"] = hash_senha(usuario_data["senha"])

    db_usuario = Usuario(**usuario_data)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    """Atualiza um usuário existente"""
    db_usuario = db.query(Usuario).filter(Usuario.idUsuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    update_data = usuario.model_dump(exclude_unset=True)

    # Hash da senha se estiver sendo atualizada
    if "senha" in update_data:
        update_data["senha"] = hash_senha(update_data["senha"])

    for key, value in update_data.items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Deleta um usuário"""
    db_usuario = db.query(Usuario).filter(Usuario.idUsuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(db_usuario)
    db.commit()
    return None

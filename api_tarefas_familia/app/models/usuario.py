from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    idUsuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Nome = Column(String(45), nullable=False)
    login = Column(String(45), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)

    # Relacionamento com TarefaUsuario
    tarefas = relationship("TarefaUsuario", back_populates="usuario")

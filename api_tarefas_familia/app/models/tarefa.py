from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Tarefa(Base):
    __tablename__ = "Tarefa"

    idTarefa = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Tarefa = Column(String(45), nullable=False)
    Descricao = Column(String(100))
    Local_idLocal = Column(Integer, ForeignKey("Local.idLocal"))

    # Relacionamentos
    local = relationship("Local", back_populates="tarefas")
    usuarios = relationship("TarefaUsuario", back_populates="tarefa")

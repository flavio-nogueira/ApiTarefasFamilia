from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base


class TarefaUsuario(Base):
    __tablename__ = "tarefa_usuario"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_idUsuario = Column(Integer, ForeignKey("usuario.idUsuario"), nullable=False)
    Tarefa_idTarefa = Column(Integer, ForeignKey("Tarefa.idTarefa"), nullable=False)
    Data = Column(Date)
    Periodo = Column(String(45))
    Feito = Column(Integer, default=0)
    DataHoraConclusao = Column(String(45))

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="tarefas")
    tarefa = relationship("Tarefa", back_populates="usuarios")

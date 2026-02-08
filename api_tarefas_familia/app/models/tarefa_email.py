from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base


class TarefaEmail(Base):
    __tablename__ = "tarefa_email"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Tarefa_idTarefa = Column(Integer, ForeignKey("Tarefa.idTarefa"), nullable=False)
    email = Column(String(100), nullable=False)
    Data = Column(Date)
    Periodo = Column(String(45))
    Feito = Column(Integer, default=0)
    DataHoraConclusao = Column(String(45))

    # Relacionamento com Tarefa
    tarefa = relationship("Tarefa")

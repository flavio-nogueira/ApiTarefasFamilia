from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Local(Base):
    __tablename__ = "Local"

    idLocal = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Descricao = Column(String(45), nullable=False)

    # Relacionamento com Tarefa
    tarefas = relationship("Tarefa", back_populates="local")

from sqlalchemy import Column, Integer, Date, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class TarefaConclusaoDiaria(Base):
    __tablename__ = "tarefa_conclusao_diaria"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tarefa_email_id = Column(Integer, ForeignKey("tarefa_email.id"), nullable=True)
    tarefa_usuario_id = Column(Integer, ForeignKey("tarefa_usuario.id"), nullable=True)
    data = Column(Date, nullable=False)
    data_hora_conclusao = Column(String(45), nullable=False)
    status = Column(Integer, default=1)

    __table_args__ = (
        UniqueConstraint('tarefa_email_id', 'data', name='uq_tarefa_email_data'),
        UniqueConstraint('tarefa_usuario_id', 'data', name='uq_tarefa_usuario_data'),
    )

    tarefa_email = relationship("TarefaEmail")
    tarefa_usuario = relationship("TarefaUsuario")

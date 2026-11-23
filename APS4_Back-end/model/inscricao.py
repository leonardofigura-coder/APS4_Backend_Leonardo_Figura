from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Inscricao(Base):
    __tablename__ = "inscricoes"
    __table_args__ = (
        UniqueConstraint("evento_id", "participante_id", name="uq_evento_participante"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    evento_id: Mapped[int] = mapped_column(ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False)
    participante_id: Mapped[int] = mapped_column(ForeignKey("participantes.id", ondelete="CASCADE"), nullable=False)
    data_inscricao: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    evento = relationship("Evento", back_populates="inscricoes")
    participante = relationship("Participante", back_populates="inscricoes")

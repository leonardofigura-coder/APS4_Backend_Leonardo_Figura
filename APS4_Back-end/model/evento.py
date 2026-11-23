from sqlalchemy import String, Integer, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str] = mapped_column(String(1000), nullable=False)
    data: Mapped[object] = mapped_column(Date, nullable=False)
    horario: Mapped[object] = mapped_column(Time, nullable=False)
    local: Mapped[str] = mapped_column(String(200), nullable=False)
    capacidade: Mapped[int] = mapped_column(Integer, nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)

    inscricoes = relationship("Inscricao", back_populates="evento",
                              cascade="all, delete-orphan")

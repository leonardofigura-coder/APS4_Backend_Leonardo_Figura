from datetime import date, time
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator

class CategoriaEvento(str, Enum):
    PALESTRA = "Palestra"
    WORKSHOP = "Workshop"
    MINICURSO = "Minicurso"
    SEMINARIO = "Seminário"
    COMPETICAO = "Competição"

class EventoBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150)
    descricao: str = Field(..., min_length=1, max_length=1000)
    data: date
    horario: time
    local: str = Field(..., min_length=1, max_length=200)
    capacidade: int = Field(..., gt=0)
    categoria: CategoriaEvento

    @field_validator("titulo", "descricao", "local")
    @classmethod
    def nao_pode_ser_vazio(cls, valor):
        valor = valor.strip()
        if not valor:
            raise ValueError("O campo não pode ser vazio.")
        return valor

class EventoResposta(EventoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

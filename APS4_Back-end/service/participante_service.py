from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from model.participante import Participante
from schema.participante_schema import ParticipanteBase

def criar_participante(db: Session, dados: ParticipanteBase):
    participante = Participante(**dados.model_dump())
    db.add(participante)
    try:
        db.commit()
        db.refresh(participante)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um participante cadastrado com este e-mail.")
    return participante

def listar_participantes(db: Session):
    return db.scalars(select(Participante).order_by(Participante.id)).all()

def buscar_participante(db: Session, participante_id: int):
    participante = db.get(Participante, participante_id)
    if not participante:
        raise HTTPException(status_code=404, detail="Participante não encontrado.")
    return participante

def atualizar_participante(db: Session, participante_id: int, dados: ParticipanteBase):
    participante = buscar_participante(db, participante_id)
    for campo, valor in dados.model_dump().items():
        setattr(participante, campo, valor)
    try:
        db.commit()
        db.refresh(participante)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um participante cadastrado com este e-mail.")
    return participante

def excluir_participante(db: Session, participante_id: int):
    participante = buscar_participante(db, participante_id)
    db.delete(participante)
    db.commit()

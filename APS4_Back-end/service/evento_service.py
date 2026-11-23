from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from model.evento import Evento
from model.participante import Participante
from model.inscricao import Inscricao
from schema.evento_schema import EventoBase

def criar_evento(db: Session, dados: EventoBase):
    evento = Evento(**dados.model_dump())
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento

def listar_eventos(db: Session):
    return db.scalars(select(Evento).order_by(Evento.id)).all()

def buscar_evento(db: Session, evento_id: int):
    evento = db.get(Evento, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
    return evento

def atualizar_evento(db: Session, evento_id: int, dados: EventoBase):
    evento = buscar_evento(db, evento_id)
    total = db.scalar(select(func.count(Inscricao.id)).where(Inscricao.evento_id == evento_id)) or 0
    if dados.capacidade < total:
        raise HTTPException(status_code=409, detail="A nova capacidade é menor que o número de participantes já inscritos.")
    for campo, valor in dados.model_dump().items():
        setattr(evento, campo, valor)
    db.commit()
    db.refresh(evento)
    return evento

def excluir_evento(db: Session, evento_id: int):
    evento = buscar_evento(db, evento_id)
    db.delete(evento)
    db.commit()

def realizar_inscricao(db: Session, evento_id: int, participante_id: int):
    evento = buscar_evento(db, evento_id)
    participante = db.get(Participante, participante_id)
    if not participante:
        raise HTTPException(status_code=404, detail="Participante não encontrado.")
    existente = db.scalar(select(Inscricao).where(
        Inscricao.evento_id == evento_id,
        Inscricao.participante_id == participante_id
    ))
    if existente:
        raise HTTPException(status_code=409, detail="Participante já está inscrito neste evento.")
    total = db.scalar(select(func.count(Inscricao.id)).where(Inscricao.evento_id == evento_id)) or 0
    if total >= evento.capacidade:
        raise HTTPException(status_code=409, detail="Não existem vagas disponíveis para este evento.")
    inscricao = Inscricao(evento_id=evento_id, participante_id=participante_id)
    db.add(inscricao)
    try:
        db.commit()
        db.refresh(inscricao)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Não foi possível registrar a inscrição por conflito de integridade.")
    return inscricao

def listar_inscritos(db: Session, evento_id: int):
    buscar_evento(db, evento_id)
    return db.scalars(
        select(Participante).join(Inscricao).where(Inscricao.evento_id == evento_id)
        .order_by(Participante.nome)
    ).all()

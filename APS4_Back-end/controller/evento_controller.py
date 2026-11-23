from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from model.usuario import Usuario
from security.security import obter_usuario_atual, exigir_administrador
from schema.evento_schema import EventoBase, EventoResposta
from schema.participante_schema import ParticipanteResposta
from schema.inscricao_schema import InscricaoResposta
from service import evento_service

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.post("", response_model=EventoResposta, status_code=status.HTTP_201_CREATED)
def cadastrar_evento(dados: EventoBase, db: Session = Depends(get_db), admin: Usuario = Depends(exigir_administrador)):
    return evento_service.criar_evento(db, dados)

@router.get("", response_model=list[EventoResposta])
def listar_eventos(db: Session = Depends(get_db)):
    return evento_service.listar_eventos(db)

@router.get("/{evento_id}", response_model=EventoResposta)
def consultar_evento(evento_id: int, db: Session = Depends(get_db)):
    return evento_service.buscar_evento(db, evento_id)

@router.put("/{evento_id}", response_model=EventoResposta)
def atualizar_evento(evento_id: int, dados: EventoBase, db: Session = Depends(get_db), admin: Usuario = Depends(exigir_administrador)):
    return evento_service.atualizar_evento(db, evento_id, dados)

@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_evento(evento_id: int, db: Session = Depends(get_db), admin: Usuario = Depends(exigir_administrador)):
    evento_service.excluir_evento(db, evento_id)

@router.post("/{evento_id}/inscricoes/{participante_id}", response_model=InscricaoResposta, status_code=status.HTTP_201_CREATED)
def inscrever_participante(evento_id: int, participante_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    return evento_service.realizar_inscricao(db, evento_id, participante_id)

@router.get("/{evento_id}/inscricoes", response_model=list[ParticipanteResposta])
def listar_inscritos(evento_id: int, db: Session = Depends(get_db), admin: Usuario = Depends(exigir_administrador)):
    return evento_service.listar_inscritos(db, evento_id)

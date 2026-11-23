from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from model.usuario import Usuario
from security.security import exigir_administrador, obter_usuario_atual
from schema.participante_schema import ParticipanteBase, ParticipanteResposta
from service import participante_service

router = APIRouter(prefix="/participantes", tags=["Participantes"])

@router.post("", response_model=ParticipanteResposta, status_code=status.HTTP_201_CREATED)
def cadastrar_participante(dados: ParticipanteBase, db: Session = Depends(get_db), admin: Usuario = Depends(exigir_administrador)):
    return participante_service.criar_participante(db, dados)

@router.get("", response_model=list[ParticipanteResposta])
def listar_participantes(db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    return participante_service.listar_participantes(db)

@router.get("/{participante_id}", response_model=ParticipanteResposta)
def consultar_participante(participante_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    return participante_service.buscar_participante(db, participante_id)

@router.put("/{participante_id}", response_model=ParticipanteResposta)
def atualizar_participante(participante_id: int, dados: ParticipanteBase, db: Session = Depends(get_db), admin: Usuario = Depends(exigir_administrador)):
    return participante_service.atualizar_participante(db, participante_id, dados)

@router.delete("/{participante_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_participante(participante_id: int, db: Session = Depends(get_db), admin: Usuario = Depends(exigir_administrador)):
    participante_service.excluir_participante(db, participante_id)

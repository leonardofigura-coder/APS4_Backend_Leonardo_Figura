from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schema.usuario_schema import UsuarioCadastro, UsuarioResposta
from service.usuario_service import criar_usuario

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("", response_model=UsuarioResposta, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(dados: UsuarioCadastro, db: Session = Depends(get_db)):
    return criar_usuario(db, dados)

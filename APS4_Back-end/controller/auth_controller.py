from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from model.usuario import Usuario
from schema.usuario_schema import LoginEntrada, TokenResposta, UsuarioResposta
from service.usuario_service import autenticar_usuario
from security.security import criar_token_acesso, obter_usuario_atual

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=TokenResposta)
def login(dados: LoginEntrada, db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, str(dados.email), dados.senha)
    return {"access_token": criar_token_acesso(usuario), "token_type": "bearer"}

@router.get("/me", response_model=UsuarioResposta)
def meus_dados(usuario: Usuario = Depends(obter_usuario_atual)):
    return usuario

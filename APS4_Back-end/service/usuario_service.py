from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from model.usuario import Usuario
from schema.usuario_schema import UsuarioCadastro
from security.security import gerar_hash_senha, verificar_senha


def criar_usuario(db: Session, dados: UsuarioCadastro) -> Usuario:
    usuario = Usuario(
        nome=dados.nome,
        email=str(dados.email).lower(),
        senha_hash=gerar_hash_senha(dados.senha),
        perfil="usuario",
    )
    db.add(usuario)
    try:
        db.commit()
        db.refresh(usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um usuário cadastrado com este e-mail.")
    return usuario


def autenticar_usuario(db: Session, email: str, senha: str) -> Usuario:
    usuario = db.scalar(select(Usuario).where(Usuario.email == email.lower()))
    if usuario is None or not verificar_senha(senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.", headers={"WWW-Authenticate": "Bearer"})
    return usuario


def criar_administrador_inicial(db: Session, nome: str, email: str, senha: str) -> None:
    if not nome or not email or not senha:
        return
    if len(senha) < 8 or not senha.strip():
        raise RuntimeError("ADMIN_PASSWORD deve ter pelo menos 8 caracteres.")
    existente = db.scalar(select(Usuario).where(Usuario.email == email.lower()))
    if existente:
        return
    db.add(Usuario(nome=nome, email=email.lower(), senha_hash=gerar_hash_senha(senha), perfil="administrador"))
    db.commit()

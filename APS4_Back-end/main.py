import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from database import Base, engine, SessionLocal
from model.evento import Evento
from model.participante import Participante
from model.inscricao import Inscricao
from model.usuario import Usuario
from service.usuario_service import criar_administrador_inicial
from controller.evento_controller import router as evento_router
from controller.participante_controller import router as participante_router
from controller.relatorio_controller import router as relatorio_router
from controller.usuario_controller import router as usuario_router
from controller.auth_controller import router as auth_router

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    criar_administrador_inicial(
        db,
        os.getenv("ADMIN_NOME", ""),
        os.getenv("ADMIN_EMAIL", ""),
        os.getenv("ADMIN_PASSWORD", ""),
    )

app = FastAPI(
    title="API de Eventos Acadêmicos",
    description="API de eventos com persistência SQLite, relatórios, autenticação JWT e autorização por perfil.",
    version="4.0.0",
)

@app.exception_handler(RequestValidationError)
async def tratar_erro_validacao(request: Request, exc: RequestValidationError):
    erros = [{"type": e.get("type"), "loc": e.get("loc"), "msg": e.get("msg")} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": jsonable_encoder(erros)})

app.include_router(evento_router)
app.include_router(participante_router)
app.include_router(relatorio_router)
app.include_router(usuario_router)
app.include_router(auth_router)

@app.get("/", tags=["Início"])
def inicio():
    return {"mensagem": "API de Eventos Acadêmicos funcionando com autenticação e segurança.", "documentacao": "/docs"}

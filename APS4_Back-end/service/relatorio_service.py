from sqlalchemy import select, func, outerjoin
from sqlalchemy.orm import Session
from model.evento import Evento
from model.participante import Participante
from model.inscricao import Inscricao

def relatorio_ocupacao(db: Session):
    stmt = (
        select(Evento.id, Evento.titulo, Evento.capacidade,
               func.count(Inscricao.id).label("total_inscritos"))
        .outerjoin(Inscricao, Inscricao.evento_id == Evento.id)
        .group_by(Evento.id, Evento.titulo, Evento.capacidade)
        .order_by(Evento.id)
    )
    resultado = []
    for linha in db.execute(stmt):
        total = linha.total_inscritos
        capacidade = linha.capacidade
        resultado.append({
            "evento_id": linha.id,
            "titulo": linha.titulo,
            "capacidade": capacidade,
            "total_inscritos": total,
            "vagas_disponiveis": max(capacidade - total, 0),
            "percentual_ocupacao": round((total / capacidade) * 100, 2) if capacidade else 0.0
        })
    return resultado

def relatorio_categorias(db: Session):
    inscricoes_por_evento = (
        select(Inscricao.evento_id, func.count(Inscricao.id).label("qtd"))
        .group_by(Inscricao.evento_id)
        .subquery()
    )
    stmt = (
        select(Evento.categoria,
               func.count(Evento.id).label("total_eventos"),
               func.coalesce(func.sum(Evento.capacidade), 0).label("capacidade_total"),
               func.coalesce(func.sum(inscricoes_por_evento.c.qtd), 0).label("total_inscricoes"))
        .outerjoin(inscricoes_por_evento, inscricoes_por_evento.c.evento_id == Evento.id)
        .group_by(Evento.categoria)
        .order_by(Evento.categoria)
    )
    return [{
        "categoria": r.categoria,
        "total_eventos": r.total_eventos,
        "capacidade_total": r.capacidade_total,
        "total_inscricoes": r.total_inscricoes
    } for r in db.execute(stmt)]

def relatorio_cursos(db: Session):
    stmt = (
        select(Participante.curso,
               func.count(func.distinct(Participante.id)).label("total_participantes"),
               func.count(Inscricao.id).label("total_inscricoes"))
        .outerjoin(Inscricao, Inscricao.participante_id == Participante.id)
        .group_by(Participante.curso)
        .order_by(Participante.curso)
    )
    return [{
        "curso": r.curso,
        "total_participantes": r.total_participantes,
        "total_inscricoes": r.total_inscricoes
    } for r in db.execute(stmt)]

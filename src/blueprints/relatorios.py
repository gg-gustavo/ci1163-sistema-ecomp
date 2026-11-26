"""Blueprint do módulo RELATÓRIOS (ECU007, operação 10)."""
import json
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Atividade, ItemFiscal, RegistroHoras, Relatorio, db

bp = Blueprint("relatorios", __name__)

TIPOS_VALIDOS = ("atividades", "prestacao_contas")


def _parse_data(valor):
    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        return None


def _montar_atividades(inicio, fim):
    registros = RegistroHoras.query.all()
    if inicio or fim:
        filtrados = []
        for registro in registros:
            data = registro.registrado_em.date() if registro.registrado_em else None
            if data is None:
                continue
            if inicio and data < inicio:
                continue
            if fim and data > fim:
                continue
            filtrados.append(registro)
        registros = filtrados

    horas_por_membro = {}
    horas_por_atividade = {}
    for registro in registros:
        nome = registro.membro.nome if registro.membro else "—"
        horas_por_membro[nome] = horas_por_membro.get(nome, 0) + (registro.horas or 0)
        horas_por_atividade[registro.atividade_id] = (
            horas_por_atividade.get(registro.atividade_id, 0) + (registro.horas or 0)
        )

    if inicio or fim:
        ids = set(horas_por_atividade)
        atividades = Atividade.query.filter(Atividade.id.in_(ids)).all() if ids else []
    else:
        atividades = Atividade.query.order_by(Atividade.nome).all()

    atividades.sort(key=lambda a: a.nome)
    return {
        "atividades": atividades,
        "horas_por_atividade": horas_por_atividade,
        "horas_por_membro": sorted(horas_por_membro.items()),
        "total_horas": sum(horas_por_membro.values()),
    }


def _montar_prestacao(inicio, fim):
    itens = ItemFiscal.query.order_by(ItemFiscal.data).all()
    if inicio:
        itens = [i for i in itens if i.data and i.data >= inicio]
    if fim:
        itens = [i for i in itens if i.data and i.data <= fim]

    grupos = {}
    for item in itens:
        grupo = grupos.setdefault(
            item.projeto_id,
            {
                "projeto": item.projeto,
                "itens": [],
                "total_notas": 0.0,
                "total_recibos": 0.0,
                "total": 0.0,
            },
        )
        grupo["itens"].append(item)
        valor = item.valor or 0
        grupo["total"] += valor
        if item.tipo == "nota":
            grupo["total_notas"] += valor
        elif item.tipo == "recibo":
            grupo["total_recibos"] += valor

    por_projeto = sorted(grupos.values(), key=lambda g: g["projeto"].id if g["projeto"] else 0)
    return {
        "por_projeto": por_projeto,
        "total_geral": sum(g["total"] for g in por_projeto),
    }


def _gerar_contexto(tipo, inicio, fim):
    contexto = {
        "tipo": tipo,
        "inicio": inicio,
        "fim": fim,
        "atividades_ctx": None,
        "prestacao_ctx": None,
    }
    if tipo == "atividades":
        contexto["atividades_ctx"] = _montar_atividades(inicio, fim)
    else:
        contexto["prestacao_ctx"] = _montar_prestacao(inicio, fim)
    return contexto


@bp.route("/")
def index():
    relatorios = Relatorio.query.order_by(Relatorio.gerado_em.desc()).all()
    return render_template("relatorios/index.html", relatorios=relatorios)


@bp.route("/gerar", methods=["POST"])
def gerar():
    tipo = request.form.get("tipo", "").strip()
    inicio_raw = request.form.get("data_inicio", "").strip()
    fim_raw = request.form.get("data_fim", "").strip()
    inicio = _parse_data(inicio_raw)
    fim = _parse_data(fim_raw)

    if tipo not in TIPOS_VALIDOS:
        flash("Selecione um tipo de relatório válido.", "error")
        return redirect(url_for("relatorios.index"))

    if inicio_raw and inicio is None:
        flash("Data de início inválida.", "error")
        return redirect(url_for("relatorios.index"))

    if fim_raw and fim is None:
        flash("Data de fim inválida.", "error")
        return redirect(url_for("relatorios.index"))

    if inicio and fim and inicio > fim:
        flash("A data de início deve ser anterior à data de fim.", "error")
        return redirect(url_for("relatorios.index"))

    filtros = {"data_inicio": inicio_raw, "data_fim": fim_raw}
    relatorio = Relatorio(tipo=tipo, filtros_json=json.dumps(filtros))
    db.session.add(relatorio)
    db.session.commit()

    contexto = _gerar_contexto(tipo, inicio, fim)
    return render_template("relatorios/resultado.html", relatorio=relatorio, **contexto)


@bp.route("/<int:relatorio_id>")
def visualizar(relatorio_id):
    relatorio = Relatorio.query.get_or_404(relatorio_id)
    try:
        filtros = json.loads(relatorio.filtros_json or "{}")
    except ValueError:
        filtros = {}

    inicio = _parse_data(filtros.get("data_inicio"))
    fim = _parse_data(filtros.get("data_fim"))
    contexto = _gerar_contexto(relatorio.tipo, inicio, fim)
    return render_template("relatorios/resultado.html", relatorio=relatorio, **contexto)

"""Blueprint do módulo ATIVIDADES (ECU004, operações 6 e 7)."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Atividade, Membro, Participante, RegistroHoras, db

bp = Blueprint("atividades", __name__)

CAMPOS_OBRIGATORIOS = ["nome", "duracao", "local", "objetivo", "resumo"]


@bp.route("/")
def index():
    atividades = Atividade.query.order_by(Atividade.nome).all()
    return render_template("atividades/index.html", atividades=atividades)


@bp.route("/nova", methods=["GET", "POST"])
def nova():
    membros = Membro.query.order_by(Membro.nome).all()

    if request.method == "POST":
        dados = {campo: request.form.get(campo, "").strip() for campo in CAMPOS_OBRIGATORIOS}
        participantes_ids = request.form.getlist("participantes")

        faltando = [campo for campo in CAMPOS_OBRIGATORIOS if not dados[campo]]
        if faltando:
            flash("Preencha todos os campos obrigatórios.", "error")
            return render_template(
                "atividades/form.html",
                membros=membros,
                dados=dados,
                participantes_ids=participantes_ids,
            )

        membros_validos = {str(m.id): m for m in membros}
        ids_validos = [pid for pid in participantes_ids if pid in membros_validos]
        if participantes_ids and not ids_validos:
            flash("Selecione apenas membros cadastrados como participantes.", "error")
            return render_template(
                "atividades/form.html",
                membros=membros,
                dados=dados,
                participantes_ids=participantes_ids,
            )

        atividade = Atividade(
            nome=dados["nome"],
            duracao=dados["duracao"],
            local=dados["local"],
            objetivo=dados["objetivo"],
            resumo=dados["resumo"],
        )
        for pid in ids_validos:
            atividade.participantes.append(Participante(membro=membros_validos[pid]))

        db.session.add(atividade)
        db.session.commit()
        flash("Atividade cadastrada com sucesso.", "success")
        return redirect(url_for("atividades.detalhe", atividade_id=atividade.id))

    return render_template("atividades/form.html", membros=membros, dados={}, participantes_ids=[])


@bp.route("/<int:atividade_id>")
def detalhe(atividade_id):
    atividade = Atividade.query.get_or_404(atividade_id)
    membros = Membro.query.order_by(Membro.nome).all()
    return render_template("atividades/detalhe.html", atividade=atividade, membros=membros)


@bp.route("/<int:atividade_id>/horas", methods=["POST"])
def registrar_horas(atividade_id):
    atividade = Atividade.query.get_or_404(atividade_id)

    membro_id = request.form.get("membro_id", "").strip()
    horas_raw = request.form.get("horas", "").strip().replace(",", ".")

    membro = Membro.query.get(membro_id) if membro_id.isdigit() else None
    try:
        horas = float(horas_raw)
    except ValueError:
        horas = None

    if not membro:
        flash("Selecione um membro cadastrado.", "error")
        return redirect(url_for("atividades.detalhe", atividade_id=atividade.id))

    if horas is None or horas <= 0:
        flash("Informe uma quantidade de horas válida (maior que zero).", "error")
        return redirect(url_for("atividades.detalhe", atividade_id=atividade.id))

    db.session.add(
        RegistroHoras(atividade_id=atividade.id, membro_id=membro.id, horas=horas)
    )
    db.session.commit()
    flash("Horas registradas com sucesso.", "success")
    return redirect(url_for("atividades.detalhe", atividade_id=atividade.id))

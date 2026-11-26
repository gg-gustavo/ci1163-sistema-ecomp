"""Blueprint do módulo FISCAL (ECU005, operação 8)."""
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import ItemFiscal, Projeto, db

bp = Blueprint("fiscal", __name__)

TIPOS_VALIDOS = ("nota", "recibo")


def _parse_data(valor):
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


@bp.route("/")
def index():
    itens = ItemFiscal.query.order_by(ItemFiscal.data.desc()).all()
    total = sum(item.valor or 0 for item in itens)
    return render_template("fiscal/index.html", itens=itens, total=total)


@bp.route("/nova", methods=["GET", "POST"])
def nova():
    projetos = Projeto.query.order_by(Projeto.id).all()

    if request.method == "POST":
        dados = {
            "projeto_id": request.form.get("projeto_id", "").strip(),
            "tipo": request.form.get("tipo", "").strip(),
            "data": request.form.get("data", "").strip(),
            "valor": request.form.get("valor", "").strip(),
        }

        projeto = Projeto.query.get(dados["projeto_id"]) if dados["projeto_id"].isdigit() else None
        data = _parse_data(dados["data"])
        try:
            valor = float(dados["valor"].replace(",", "."))
        except ValueError:
            valor = None

        if not projeto or not dados["tipo"] or not dados["data"] or not dados["valor"]:
            flash("Preencha todos os campos obrigatórios.", "error")
            return render_template("fiscal/form.html", projetos=projetos, dados=dados)

        if dados["tipo"] not in TIPOS_VALIDOS:
            flash("Tipo deve ser 'nota' ou 'recibo'.", "error")
            return render_template("fiscal/form.html", projetos=projetos, dados=dados)

        if data is None:
            flash("Data inválida.", "error")
            return render_template("fiscal/form.html", projetos=projetos, dados=dados)

        if valor is None or valor <= 0:
            flash("Informe um valor válido (maior que zero).", "error")
            return render_template("fiscal/form.html", projetos=projetos, dados=dados)

        db.session.add(
            ItemFiscal(projeto_id=projeto.id, tipo=dados["tipo"], data=data, valor=valor)
        )
        db.session.commit()
        flash("Item fiscal cadastrado com sucesso.", "success")
        return redirect(url_for("fiscal.index"))

    return render_template("fiscal/form.html", projetos=projetos, dados={})

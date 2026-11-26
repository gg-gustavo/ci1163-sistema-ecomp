"""Blueprint do módulo MEMBROS (ECU006, operação 9)."""
import re

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Membro, db

bp = Blueprint("membros", __name__)

CAMPOS_OBRIGATORIOS = ["nome", "cpf", "email", "cargo", "diretoria"]


def apenas_digitos(valor):
    return re.sub(r"\D", "", valor or "")


def cpf_valido(cpf):
    """Confere tamanho e dígitos verificadores de um CPF."""
    numeros = apenas_digitos(cpf)
    if len(numeros) != 11 or len(set(numeros)) == 1:
        return False

    for tamanho in (9, 10):
        soma = sum(int(numeros[i]) * (tamanho + 1 - i) for i in range(tamanho))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if digito != int(numeros[tamanho]):
            return False
    return True


@bp.route("/")
def index():
    membros = Membro.query.order_by(Membro.nome).all()
    return render_template("membros/index.html", membros=membros)


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        dados = {campo: request.form.get(campo, "").strip() for campo in CAMPOS_OBRIGATORIOS}

        if not all(dados.values()):
            flash("Preencha todos os campos obrigatórios.", "error")
            return render_template("membros/form.html", dados=dados)

        if not cpf_valido(dados["cpf"]):
            flash("CPF inválido", "error")
            return render_template("membros/form.html", dados=dados)

        cpf_normalizado = apenas_digitos(dados["cpf"])
        if Membro.query.filter_by(cpf=cpf_normalizado).first():
            flash("CPF já cadastrado.", "error")
            return render_template("membros/form.html", dados=dados)

        db.session.add(
            Membro(
                nome=dados["nome"],
                cpf=cpf_normalizado,
                email=dados["email"],
                cargo=dados["cargo"],
                diretoria=dados["diretoria"],
            )
        )
        db.session.commit()
        flash("Membro cadastrado com sucesso.", "success")
        return redirect(url_for("membros.index"))

    return render_template("membros/form.html", dados={})

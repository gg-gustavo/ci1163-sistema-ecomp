"""Blueprint do módulo PROJETOS (ECU001–ECU003)."""
import os
import uuid
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from models import Cliente, Desenvolvedor, Etapa, Membro, Projeto, db

bp = Blueprint("projetos", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


def _parse_date(value):
    """Converte 'YYYY-MM-DD' em date; retorna None se inválido/ausente."""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _salvar_contrato(arquivo):
    """Salva o arquivo de contrato em src/uploads com nome único."""
    if not arquivo or not arquivo.filename:
        return None
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    nome_original = secure_filename(arquivo.filename)
    nome_unico = f"{uuid.uuid4().hex}_{nome_original}"
    arquivo.save(os.path.join(UPLOAD_DIR, nome_unico))
    return nome_unico


@bp.route("/")
def index():
    projetos = Projeto.query.order_by(Projeto.data_inicio.desc()).all()
    return render_template("projetos/index.html", projetos=projetos)


@bp.route("/nova", methods=["GET", "POST"])
def nova():
    clientes = Cliente.query.order_by(Cliente.nome).all()

    if request.method == "POST":
        cliente_id = request.form.get("cliente_id", type=int)
        data_inicio = _parse_date(request.form.get("data_inicio"))
        prazo_entrega = _parse_date(request.form.get("prazo_entrega"))
        descricao = (request.form.get("descricao") or "").strip()

        erros = []
        if not cliente_id or not db.session.get(Cliente, cliente_id):
            erros.append("Selecione um cliente válido.")
        if not data_inicio:
            erros.append("Informe a data de início.")
        if not prazo_entrega:
            erros.append("Informe o prazo de entrega.")
        if not descricao:
            erros.append("Informe a descrição do projeto.")

        if erros:
            for erro in erros:
                flash(erro, "error")
            return render_template(
                "projetos/form.html", clientes=clientes, form=request.form
            ), 400

        contrato = _salvar_contrato(request.files.get("contrato_pdf"))
        projeto = Projeto(
            cliente_id=cliente_id,
            data_inicio=data_inicio,
            prazo_entrega=prazo_entrega,
            descricao=descricao,
            contrato_pdf=contrato,
        )
        db.session.add(projeto)
        db.session.commit()

        if contrato:
            flash("Projeto cadastrado com contrato importado.", "success")
        else:
            flash("Projeto cadastrado sem contrato (confirmação registrada).", "success")
        return redirect(url_for("projetos.detalhe", projeto_id=projeto.id))

    return render_template("projetos/form.html", clientes=clientes, form={})


@bp.route("/<int:projeto_id>")
def detalhe(projeto_id):
    projeto = db.get_or_404(Projeto, projeto_id)
    membros = Membro.query.order_by(Membro.nome).all()
    return render_template(
        "projetos/detalhe.html", projeto=projeto, membros=membros
    )


@bp.route("/<int:projeto_id>/etapas", methods=["POST"])
def cadastrar_etapas(projeto_id):
    projeto = db.get_or_404(Projeto, projeto_id)
    cronograma = (request.form.get("cronograma") or "").strip()
    status = (request.form.get("status") or "planejada").strip()

    if not cronograma:
        flash("Informe o cronograma da etapa.", "error")
        return redirect(url_for("projetos.detalhe", projeto_id=projeto.id))

    db.session.add(Etapa(projeto_id=projeto.id, cronograma=cronograma, status=status))
    db.session.commit()
    flash("Etapa cadastrada.", "success")
    return redirect(url_for("projetos.detalhe", projeto_id=projeto.id))


@bp.route("/<int:projeto_id>/etapas/<int:etapa_id>/atualizar", methods=["POST"])
def atualizar_cronograma_etapa(projeto_id, etapa_id):
    projeto = db.get_or_404(Projeto, projeto_id)
    etapa = db.get_or_404(Etapa, etapa_id)
    if etapa.projeto_id != projeto.id:
        flash("Etapa não pertence ao projeto informado.", "error")
        return redirect(url_for("projetos.detalhe", projeto_id=projeto.id))

    cronograma = (request.form.get("cronograma") or "").strip()
    status = (request.form.get("status") or "").strip()
    if not cronograma:
        flash("Informe o cronograma da etapa.", "error")
        return redirect(url_for("projetos.detalhe", projeto_id=projeto.id))
    if status not in ("planejada", "em andamento", "concluída"):
        flash("Status inválido.", "error")
        return redirect(url_for("projetos.detalhe", projeto_id=projeto.id))

    etapa.cronograma = cronograma
    etapa.status = status
    db.session.commit()
    flash("Cronograma da etapa atualizado.", "success")
    return redirect(url_for("projetos.detalhe", projeto_id=projeto.id))


@bp.route("/<int:projeto_id>/desenvolvedores", methods=["POST"])
def adicionar_desenvolvedor(projeto_id):
    projeto = db.get_or_404(Projeto, projeto_id)
    membro_id = request.form.get("membro_id", type=int)
    papel = (request.form.get("papel") or "").strip()

    membro = db.session.get(Membro, membro_id) if membro_id else None
    if not membro:
        flash("Nenhum desenvolvedor selecionado.", "error")
        return redirect(url_for("projetos.detalhe", projeto_id=projeto.id))
    if not papel:
        flash("Informe o papel do desenvolvedor.", "error")
        return redirect(url_for("projetos.detalhe", projeto_id=projeto.id))

    db.session.add(
        Desenvolvedor(projeto_id=projeto.id, membro_id=membro.id, papel=papel)
    )
    db.session.commit()
    flash("Desenvolvedor adicionado ao projeto.", "success")
    return redirect(url_for("projetos.detalhe", projeto_id=projeto.id))

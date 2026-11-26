"""Modelos de domínio do Sistema Ecomp (Fonte única — não renomear).

Nomes alinhados a docs/PLANO.md e ao diagrama conceitual do enunciado.
"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    cpf_cnpj = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    contato = db.Column(db.String(120))

    projetos = db.relationship("Projeto", back_populates="cliente")


class Projeto(db.Model):
    __tablename__ = "projetos"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    prazo_entrega = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.Text)
    contrato_pdf = db.Column(db.String(255))  # caminho do arquivo importado

    cliente = db.relationship("Cliente", back_populates="projetos")
    etapas = db.relationship("Etapa", back_populates="projeto", cascade="all, delete-orphan")
    desenvolvedores = db.relationship("Desenvolvedor", back_populates="projeto", cascade="all, delete-orphan")
    itens_fiscais = db.relationship("ItemFiscal", back_populates="projeto", cascade="all, delete-orphan")


class Etapa(db.Model):
    __tablename__ = "etapas"
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey("projetos.id"), nullable=False)
    cronograma = db.Column(db.String(255))
    status = db.Column(db.String(30), default="planejada")

    projeto = db.relationship("Projeto", back_populates="etapas")


class Membro(db.Model):
    """Ecomper: nome, cpf, email, cargo (ECU006)."""
    __tablename__ = "membros"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    email = db.Column(db.String(120))
    cargo = db.Column(db.String(60))
    diretoria = db.Column(db.String(60))

    desenvolvimentos = db.relationship("Desenvolvedor", back_populates="membro")
    participacoes = db.relationship("Participante", back_populates="membro")
    registros_horas = db.relationship("RegistroHoras", back_populates="membro")


class Desenvolvedor(db.Model):
    __tablename__ = "desenvolvedores"
    id = db.Column(db.Integer, primary_key=True)
    membro_id = db.Column(db.Integer, db.ForeignKey("membros.id"), nullable=False)
    projeto_id = db.Column(db.Integer, db.ForeignKey("projetos.id"), nullable=False)
    papel = db.Column(db.String(60))

    membro = db.relationship("Membro", back_populates="desenvolvimentos")
    projeto = db.relationship("Projeto", back_populates="desenvolvedores")


class Atividade(db.Model):
    __tablename__ = "atividades"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    duracao = db.Column(db.String(60))
    local = db.Column(db.String(120))
    objetivo = db.Column(db.Text)
    resumo = db.Column(db.Text)

    participantes = db.relationship("Participante", back_populates="atividade", cascade="all, delete-orphan")
    registros_horas = db.relationship("RegistroHoras", back_populates="atividade", cascade="all, delete-orphan")


class Participante(db.Model):
    __tablename__ = "participantes"
    id = db.Column(db.Integer, primary_key=True)
    atividade_id = db.Column(db.Integer, db.ForeignKey("atividades.id"), nullable=False)
    membro_id = db.Column(db.Integer, db.ForeignKey("membros.id"), nullable=False)

    atividade = db.relationship("Atividade", back_populates="participantes")
    membro = db.relationship("Membro", back_populates="participacoes")


class RegistroHoras(db.Model):
    """Ponto de extensão do ECU004: horas registradas em atividade, atribuídas ao membro."""
    __tablename__ = "registros_horas"
    id = db.Column(db.Integer, primary_key=True)
    atividade_id = db.Column(db.Integer, db.ForeignKey("atividades.id"), nullable=False)
    membro_id = db.Column(db.Integer, db.ForeignKey("membros.id"), nullable=False)
    horas = db.Column(db.Float, nullable=False)
    registrado_em = db.Column(db.DateTime, default=datetime.utcnow)

    atividade = db.relationship("Atividade", back_populates="registros_horas")
    membro = db.relationship("Membro", back_populates="registros_horas")


class ItemFiscal(db.Model):
    """Notas fiscais e recibos vinculados a projetos (ECU005)."""
    __tablename__ = "itens_fiscais"
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey("projetos.id"), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # 'nota' | 'recibo'
    data = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False)

    projeto = db.relationship("Projeto", back_populates="itens_fiscais")


class Relatorio(db.Model):
    """Relatórios de atividades e de prestação de contas (ECU007)."""
    __tablename__ = "relatorios"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)  # 'atividades' | 'prestacao_contas'
    filtros_json = db.Column(db.Text)
    gerado_em = db.Column(db.DateTime, default=datetime.utcnow)
    caminho_pdf = db.Column(db.String(255))

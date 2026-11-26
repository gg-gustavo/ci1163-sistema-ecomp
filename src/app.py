"""Fábrica da aplicação Flask do Sistema Ecomp."""
import os

from flask import Flask, render_template

from models import db

BLUEPRINTS = [
    ("blueprints.projetos", "bp", "/projetos"),
    ("blueprints.atividades", "bp", "/atividades"),
    ("blueprints.fiscal", "bp", "/fiscal"),
    ("blueprints.membros", "bp", "/membros"),
    ("blueprints.relatorios", "bp", "/relatorios"),
]


def create_app():
    app = Flask(__name__)
    base = os.path.dirname(os.path.abspath(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base, "ecomp.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    for import_path, attr, url_prefix in BLUEPRINTS:
        module = __import__(import_path, fromlist=[attr])
        app.register_blueprint(getattr(module, attr), url_prefix=url_prefix)

    @app.route("/")
    def home():
        return render_template("base.html")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

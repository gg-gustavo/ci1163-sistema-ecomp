#!/usr/bin/env python3
"""Monta o PDF de entrega do trabalho (artefatos + diagramas renderizados)."""
import os
import re
import subprocess
import sys

import markdown

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
REN = os.path.join(REPO, "diagramas-render")

GRRS = "GRR20203935 GRR20224759 GRR20223829 GRR20224377 GRR20221261"

CSS = """
@page { size: A4; margin: 2cm 1.8cm; @bottom-center { content: counter(page); font-size: 9pt; color: #666; } }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 10pt; color: #1a1a1a; }
h1 { font-size: 16pt; border-bottom: 2px solid #1d3557; color: #1d3557; padding-bottom: 4px; margin-top: 0; }
h2 { font-size: 13pt; color: #1d3557; margin-top: 18px; }
h3 { font-size: 11pt; color: #457b9d; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 8px 0; }
th, td { border: 1px solid #999; padding: 4px 6px; text-align: left; vertical-align: top; }
th { background: #f1faee; }
img { max-width: 100%; max-height: 16cm; display: block; margin: 8px auto; }
.page-break { page-break-before: always; }
pre, code { font-size: 9pt; background: #f6f6f6; }
pre { padding: 6px; }
li { margin-bottom: 2px; }
"""


def md(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"\]\((\.\./|\./)?([^)#]+)(#[^)]*)?\)",
                  lambda m: f"](file://{os.path.join(os.path.dirname(path), m.group(2))})", text)
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


def fig(path, caption):
    return (f'<figure><img src="file://{path}"/>'
            f'<figcaption style="text-align:center;font-size:9pt;color:#555">{caption}</figcaption></figure>')


def main():
    p = []
    # Capa
    p.append(f"""
    <div style="text-align:center;margin-top:4cm">
      <h1 style="border:0;font-size:22pt">Sistema Ecomp</h1>
      <p style="font-size:13pt">Trabalho Prático<br>
      Design de Software<br>
      CI1163, 2026-2, Universidade Federal do Paraná</p>
      <p style="font-size:12pt;margin-top:2cm">
      Gustavo Gabriel Ripka, GRR20203935<br>
      Pedro Henrique Gurski, GRR20224759<br>
      Ulisses Curvello Ferreira, GRR20223829<br>
      Arthur Barreto Godoi, GRR20224377<br>
      Gabriel Shigueo, GRR20221261</p>
    </div>
    <div class="page-break"></div>""")

    # Sumário dos artefatos
    p.append("<h1>Sumário dos artefatos</h1><ul>"
             "<li>Artefato 1 - Diagramas de Sequência de Sistema (DSS)</li>"
             "<li>Artefato 2 - Contratos de Operação (2 por integrante)</li>"
             "<li>Artefato 3 - Diagramas de Interação</li>"
             "<li>Artefato 4 - Diagrama de Classes (Visão de Projeto)</li>"
             "<li>Artefato 5 - Implementação</li>"
             "<li>Artefato 6 - Verificação e Validação dos Diagramas</li>"
             "<li>Relatório</li></ul>")

    # Artefato 1: DSS
    p.append('<div class="page-break"></div><h1>Artefato 1 - Diagramas de Sequência de Sistema</h1>')
    for nome, titulo in [
        ("dss-01-cadastrar-projeto", "DSS 01 - Cadastrar Projeto (ECU001)"),
        ("dss-02-cadastrar-etapas", "DSS 02 - Cadastrar Etapas (ECU002)"),
        ("dss-03-adicionar-desenvolvedor", "DSS 03 - Adicionar Desenvolvedor (ECU003)"),
        ("dss-04-cadastrar-atividade", "DSS 04 - Cadastrar Atividade (ECU004)"),
        ("dss-05-cadastrar-item-fiscal", "DSS 05 - Cadastrar Item Fiscal (ECU005)"),
        ("dss-06-cadastrar-membro", "DSS 06 - Cadastrar Membro (ECU006)"),
        ("dss-07-gerar-relatorio", "DSS 07 - Gerar Relatório (ECU007)"),
    ]:
        p.append(fig(os.path.join(REN, "01-dss", nome + ".png"), titulo))

    # Artefato 2: contratos
    p.append('<div class="page-break"></div><h1>Artefato 2 - Contratos de Operação</h1>')
    for i in range(1, 11):
        for f in os.listdir(os.path.join(DOCS, "02-contratos")):
            if f.startswith(f"contrato-{i:02d}-"):
                p.append(f'<div class="page-break"></div>' + md(os.path.join(DOCS, "02-contratos", f)))
                break

    # Artefato 3: interação
    p.append('<div class="page-break"></div><h1>Artefato 3 - Diagramas de Interação</h1>')
    ops = ["cadastrarProjeto", "importarContrato", "cadastrarEtapasProjeto",
           "atualizarCronogramaEtapa", "adicionarDesenvolvedorProjeto", "cadastrarAtividade",
           "registrarHorasAtividade", "cadastrarItemFiscal", "cadastrarMembro", "gerarRelatorio"]
    for i, op in enumerate(ops, 1):
        p.append(fig(os.path.join(REN, "03-interacao", f"interacao-{i:02d}-{op}.png"),
                     f"Interação {i:02d} - {op}"))

    # Artefato 4: classes
    p.append('<div class="page-break"></div><h1>Artefato 4 - Diagrama de Classes (Visão de Projeto)</h1>')
    p.append((f'<figure><img src="file://{os.path.join(REN, "04-classes", "diagrama-classes-projeto.png")}" '
              'style="max-width:100%;max-height:23cm;display:block;margin:0 auto"/>'
              '<figcaption style="text-align:center;font-size:9pt;color:#555">'
              'Visão de projeto: UI → Controle → Domínio → Persistência</figcaption></figure>'))
    p.append(md(os.path.join(DOCS, "04-classes", "README.md")))

    # Artefato 5: implementação
    p.append('<div class="page-break"></div><h1>Artefato 5 - Implementação</h1>')
    p.append("<p>Software funcionando em Flask + SQLite (fontes em <code>src/</code> no .tar.gz e no repositório). "
             "Como executar: <code>cd src &amp;&amp; pip3 install -r requirements.txt &amp;&amp; python3 app.py</code> "
             "→ http://localhost:5000. Detalhes das telas e módulos no relatório e no README do repositório.</p>")
    p.append(md(os.path.join(DOCS, "06-verificacao-validacao.md")))

    # Relatório
    p.append('<div class="page-break"></div>' + md(os.path.join(DOCS, "relatorio.md")))

    html = f"<!doctype html><html lang=pt-BR><meta charset=utf-8><style>{CSS}</style><body>{''.join(p)}</body></html>"
    out_html = "/tmp/opencode/entrega.html"
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)

    out_pdf = os.path.join(REPO, f"{GRRS}.pdf")
    subprocess.run(["weasyprint", out_html, out_pdf], check=True, cwd="/tmp/opencode")
    print("PDF:", out_pdf)


if __name__ == "__main__":
    sys.exit(main())

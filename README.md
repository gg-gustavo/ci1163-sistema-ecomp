# CI1163 - Design de Software - Sistema Ecomp

Projeto e implementação do sistema de relatórios da Ecomp (Trabalho Prático - Design de Software, CI1163, 2026-2, UFPR).

## Equipe (5 integrantes - autorização do professor)

| Integrante | GRR |
|---|---|
| Gustavo Gabriel Ripka | GRR20203935 |
| Pedro Henrique Gurski | GRR20224759 |
| Ulisses Curvello Ferreira | GRR20223829 |
| Arthur Barreto Godoi | GRR20224377 |
| Gabriel Shigueo | GRR20221261 |

## Artefatos

| # | Artefato | Local | Pontos |
|---|---|---|---|
| 1 | Diagramas de Sequência de Sistema (DSS) | `docs/01-dss/` | 10 |
| 2 | Contratos de Operação (2 por integrante = 10) | `docs/02-contratos/` | 10 |
| 3 | Diagramas de Interação | `docs/03-interacao/` | 30 |
| 4 | Diagrama de Classes - Visão de Projeto | `docs/04-classes/` | 20 |
| 5 | Implementação (Flask + SQLite) | `src/` | 20 |
| 6 | Verificação e Validação dos Diagramas | `docs/06-verificacao-validacao.md` | 10 |

## Fluxo de execução (repo → entrega)

1. `main` contém apenas o esqueleto e o plano; artefatos entram por **branch + Pull Request**.
2. Branches: `artefato/01-dss`, `artefato/02-contratos`, `artefato/03-interacao`, `artefato/04-classes`, `impl/projetos`, `impl/atividades-financas`.
3. Reconciliação em `main`, revisão cruzada dos diagramas, geração do PDF e do `.tar.gz`.

## Entrega

- `GRR20203935 GRR20224759 GRR20223829 GRR20224377 GRR20221261.pdf` (artefatos + relatório)
- `GRR20203935 GRR20224759 GRR20223829 GRR20224377 GRR20221261.tar.gz` (fontes)

## Como rodar

```bash
cd src
pip3 install -r requirements.txt
python3 app.py   # http://localhost:5000
```

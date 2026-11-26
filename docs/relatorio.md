# Relatório - Trabalho Prático de Design de Software

**Disciplina:** Design de Software - CI1163 - **2026-2** - UFPR
**Tema:** Sistema Ecomp (relatório de atividades e prestação de contas da Ecomp)

## Equipe

| Integrante | GRR | Atribuições |
|---|---|---|
| Gustavo Gabriel Ripka | GRR20203935 | Contratos 01–02 (cadastrarProjeto, importarContrato); revisão do módulo Projetos |
| Pedro Henrique Gurski | GRR20224759 | Contratos 03–04 (cadastrarEtapasProjeto, atualizarCronogramaEtapa) |
| Ulisses Curvello Ferreira | GRR20223829 | Contratos 05–06 (adicionarDesenvolvedorProjeto, cadastrarAtividade) |
| Arthur Barreto Godoi | GRR20224377 | Contratos 07–08 (registrarHorasAtividade, cadastrarItemFiscal) |
| Gabriel Shigueo | GRR20221261 | Contratos 09–10 (cadastrarMembro, gerarRelatorio) |

Observação: a equipe foi composta por 5 integrantes conforme autorização do professor (o enunciado prevê até 4).

## 1. Artefatos entregues

| Artefato | Local | Pontos (enunciado) |
|---|---|---|
| 1. Diagramas de Sequência de Sistema | `docs/01-dss/` - 7 diagramas (um por ECU) | 10 |
| 2. Contratos de Operação | `docs/02-contratos/` - 10 contratos (2 por integrante) | 10 |
| 3. Diagramas de Interação | `docs/03-interacao/` - 10 diagramas (um por operação do sistema) | 30 |
| 4. Diagrama de Classes - Visão de Projeto | `docs/04-classes/` | 20 |
| 5. Implementação | `src/` - Flask + SQLite | 20 |
| 6. Verificação e Validação | `docs/06-verificacao-validacao.md` | 10 |

Diagramas em PlantUML (fontes `.puml` versionados no repositório); renders em PNG no diretório `diagramas-render/` e incorporados ao PDF de entrega.

## 2. Método de trabalho

O trabalho foi executado no repositório aberto **github.com/gg-gustavo/ci1163-sistema-ecomp**, com fluxo de execução até a entrega:

1. `docs/PLANO.md` como fonte única de nomes canônicos (10 operações do sistema, classes de domínio, arquitetura) - garante que DSS, contratos, diagramas de interação, classes e código falem a mesma língua.
2. Issues #1–#7 como backlog dos artefatos.
3. Uma branch por artefato/lane (`artefato/01-dss`, `artefato/02-contratos`, `artefato/03-interacao`, `artefato/04-classes`, `impl/projetos`, `impl/atividades-financas`), integradas por Pull Requests revisados.
4. Reconciliação em `main`: validação integrada do software, verificação gráfica dos diagramas e fechamento das issues.

## 3. Operações do sistema (espinha dorsal dos artefatos)

| # | Operação | ECU | Contrato (autor) |
|---|---|---|---|
| 1 | `cadastrarProjeto(dadosProjeto)` | ECU001 | 01 (GRR20203935) |
| 2 | `importarContrato(projeto, arquivoPdf)` | ECU001 | 02 (GRR20203935) |
| 3 | `cadastrarEtapasProjeto(projeto, etapas)` | ECU002 | 03 (GRR20224759) |
| 4 | `atualizarCronogramaEtapa(etapa, cronograma, status)` | ECU002 | 04 (GRR20224759) |
| 5 | `adicionarDesenvolvedorProjeto(projeto, desenvolvedor, papel)` | ECU003 | 05 (GRR20223829) |
| 6 | `cadastrarAtividade(dadosAtividade)` | ECU004 | 06 (GRR20223829) |
| 7 | `registrarHorasAtividade(atividade, membro, horas)` | ECU004 (ext.) | 07 (GRR20224377) |
| 8 | `cadastrarItemFiscal(projeto, tipo, data, valor)` | ECU005 | 08 (GRR20224377) |
| 9 | `cadastrarMembro(dadosMembro)` | ECU006 | 09 (GRR20221261) |
| 10 | `gerarRelatorio(tipo, filtros)` | ECU007 | 10 (GRR20221261) |

## 4. Implementação

Aplicação web **Flask + SQLAlchemy (SQLite)**, em camadas (GRASP): UI (templates Jinja) → Controladores (blueprints por área) → Domínio (`models.py`) → Persistência (`db.session`).

Funcionalidades (todas validadas por execução):
- Cadastro de projetos com cliente, datas, descrição e **upload do contrato em PDF** (ECU001), com fluxos alternativos (campos obrigatórios; projeto sem contrato).
- Cadastro e atualização de **etapas/cronograma/status** por projeto (ECU002).
- **Desenvolvedores** vinculados a projetos com papel, a partir dos membros cadastrados (ECU003).
- Cadastro de **atividades** com participantes (somente membros) e **registro de horas** por membro (ECU004 + ponto de extensão).
- **Notas fiscais e recibos** vinculados a projetos (ECU005).
- Cadastro de **membros** com validação de CPF (dígitos verificadores), cargo e diretoria (ECU006).
- **Relatórios** de atividades (horas por membro, com filtro de período) e de prestação de contas (itens fiscais por projeto, totais), persistidos e reexibíveis (ECU007).

Como executar: `cd src && pip3 install -r requirements.txt && python3 app.py` → http://localhost:5000

## 5. Verificação e validação

Resumo em `docs/06-verificacao-validacao.md`; destaques:
- 18 diagramas compilados sem erro e inspecionados um a um - **nenhum elemento sobreposto**;
- rastreabilidade completa 10/10: cada operação tem DSS, diagrama de interação, contrato e rota correspondente;
- testes integrados fim a fim do software (incluindo fluxos alternativos dos ECUs) e testes por módulo (18 + 32 verificações);
- ajustes aplicados após o V&V: ponto de extensão do ECU004 incluído no DSS, `secret_key` do app, dependência de pacote no diagrama de classes.

## 6. Entrega

- **PDF:** `GRR20203935 GRR20224759 GRR20223829 GRR20224377 GRR20221261.pdf`
- **Fontes:** `GRR20203935 GRR20224759 GRR20223829 GRR20224377 GRR20221261.tar.gz`

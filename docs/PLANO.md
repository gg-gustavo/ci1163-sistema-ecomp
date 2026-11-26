# CONTRATO DE DESIGN — fonte única de nomes canônicos

> TODOS os artefatos (DSS, contratos, diagramas de interação, classes de projeto e código)
> DEVEM usar exatamente estes nomes. Nada de sinônimos.

## 1. Operações do Sistema (10 — base dos DSS, contratos e diagramas de interação)

| # | Operação | ECU | Autor dos Contratos (2/integrante) |
|---|---|---|---|
| 1 | `cadastrarProjeto(dadosProjeto)` | ECU001 | Gustavo Ripka GRR20203935 |
| 2 | `importarContrato(projeto, arquivoPdf)` | ECU001 | Gustavo Ripka GRR20203935 |
| 3 | `cadastrarEtapasProjeto(projeto, etapas)` | ECU002 | Pedro Gurski GRR20224759 |
| 4 | `atualizarCronogramaEtapa(etapa, cronograma, status)` | ECU002 | Pedro Gurski GRR20224759 |
| 5 | `adicionarDesenvolvedorProjeto(projeto, desenvolvedor, papel)` | ECU003 | Ulisses Curvello GRR20223829 |
| 6 | `cadastrarAtividade(dadosAtividade)` | ECU004 | Ulisses Curvello GRR20223829 |
| 7 | `registrarHorasAtividade(atividade, membro, horas)` | ECU004 (ext.) | Arthur Godoi GRR20224377 |
| 8 | `cadastrarItemFiscal(projeto, tipo, data, valor)` | ECU005 | Arthur Godoi GRR20224377 |
| 9 | `cadastrarMembro(dadosMembro)` | ECU006 | Gabriel Shigueo GRR20221261 |
| 10 | `gerarRelatorio(tipo, filtros)` | ECU007 | Gabriel Shigueo GRR20221261 |

Atores: `Direção de Projetos`, `Desenvolvedor`, `Direção de Atividades`, `Adm-Fin`, `Usuário (membro)`.

## 2. Classes de domínio (conceitual → projeto; nomes fixos)

- `Ecomp` (facade/conceito raiz: possui projetos, atividades, membros; gera relatórios)
- `Cliente` (nome, email, cpfCnpj, telefone, contato)
- `Projeto` (cliente [1], dataInicio, prazoEntrega, descricao, contratoPdf; possui Etapas [1..*], Desenvolvedores [1..*], ItensFiscais [0..*])
- `Etapa` (cronograma, status)
- `Ecomper` (nome, cpf, email, cargo) — superclasse
- `Desenvolvedor` (papel; é um Ecomper; é desenvolvido por: Projeto)
- `Atividade` (nome, duracao, local, objetivo, resumo; participada por Participantes [1..*])
- `Participante` (é um Ecomper; participa de Atividade)
- `ItemFiscal` (tipo [nota|recibo], data, valor; pertence a Projeto)
- `Relatorio` (tipo [atividades|prestacaoContas], filtros, geradoEm; relata Projeto e Atividade)

## 3. Arquitetura da implementação (Flask + SQLite)

Camadas (GRASP): UI (Jinja/routes) → Controlador (blueprints por área) → Domínio (`models.py`) → Persistência (Flask-SQLAlchemy, SQLite `src/ecomp.db`).

Blueprints: `projetos` (ECU001–003), `atividades` (ECU004), `fiscal` (ECU005), `membros` (ECU006), `relatorios` (ECU007).

## 4. Regras de consistência

- DSS: um por ECU (7 no total), mensagens com os nomes das operações acima.
- Diagramas de interação: um por operação do sistema (10), no formato diagrama de sequência de projeto, mostrando UI → Controller → Domínio → Persistência.
- Contratos: pré/pós-condições sobre as classes conceituais da seção 2, no formato Larman.
- Nenhum diagrama renderizado pode ter elementos sobrepostos (verificação no `make render`).

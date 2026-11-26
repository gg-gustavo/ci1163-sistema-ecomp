# Artefato 6 - Verificação e Validação dos Diagramas

Disciplina: Design de Software - CI1163 - 2026-2 (UFPR)
Data da verificação: 26/11/2026

## Método

1. **Verificação sintática**: todos os 18 diagramas PlantUML compilados com `plantuml` (v1.2020.02) - 0 erros de sintaxe (`scripts/render.sh` falha em caso de erro).
2. **Verificação de consistência (rastreabilidade)**: grep dos nomes canônicos definidos em `docs/PLANO.md` em todos os artefatos - cada uma das 10 operações do sistema aparece em: 1 DSS (mensagem), 1 diagrama de interação (título) e 1 contrato de operação. Controladores citados nos diagramas de interação (ProjetosController ×5, AtividadesController ×2, FiscalController, MembrosController, RelatoriosController) são exatamente os mesmos do diagrama de classes e do código (`src/blueprints/`).
3. **Verificação de qualidade gráfica**: inspeção visual de cada um dos 18 PNGs renderizados - nenhuma sobreposição de elementos em nenhum diagrama. Um problema de poluição gráfica (dependências tracejadas cruzando o diagrama de classes) foi detectado e corrigido (dependências classe-a-classe → dependência de pacote `Controle ..> "Domínio"`).
4. **Validação por execução**: o projeto foi implementado e os diagramas validados contra o software funcionando (Flask + SQLite):
   - Teste integrado fim a fim do app completo (`src/app.py`): cadastro de membro (CPF válido e inválido), projeto, etapa, atualização de cronograma, desenvolvedor, atividade com participante, registro de horas, item fiscal e geração dos 2 tipos de relatório - todos os fluxos OK, incluindo os fluxos alternativos dos ECUs (campos obrigatórios, CPF inválido/repetido, projeto sem contrato).
   - Testes unitários por módulo: 18/18 (Projetos) e 32 checks (Atividades/Fiscal/Membros/Relatórios).

## Ajustes de V&V aplicados

| Achado | Correção |
|---|---|
| `registrarHorasAtividade` (ponto de extensão do ECU004) não aparecia em nenhum DSS | Incluído em `dss-04` via `ref` do ponto de extensão - rastreabilidade 10/10 fechada |
| Falta de `secret_key` no app fazia `flash()` falhar nos POSTs | Corrigido em `src/app.py` |
| Diagrama de classes com dependências tracejadas cruzando o layout | Substituídas por dependência única de pacote |

## Matriz de rastreabilidade

| Operação do sistema | ECU | DSS | Interação | Contrato | Implementação |
|---|---|---|---|---|---|
| cadastrarProjeto | ECU001 | dss-01 | interacao-01 | 01 (GRR20203935) | `projetos.nova` |
| importarContrato | ECU001 | dss-01 | interacao-02 | 02 (GRR20203935) | `projetos.nova` (upload) |
| cadastrarEtapasProjeto | ECU002 | dss-02 | interacao-03 | 03 (GRR20224759) | `projetos.cadastrar_etapas` |
| atualizarCronogramaEtapa | ECU002 | dss-02 | interacao-04 | 04 (GRR20224759) | `projetos.atualizar_cronograma_etapa` |
| adicionarDesenvolvedorProjeto | ECU003 | dss-03 | interacao-05 | 05 (GRR20223829) | `projetos.adicionar_desenvolvedor` |
| cadastrarAtividade | ECU004 | dss-04 | interacao-06 | 06 (GRR20223829) | `atividades.nova` |
| registrarHorasAtividade | ECU004 (ext.) | dss-04 (ref) | interacao-07 | 07 (GRR20224377) | `atividades.registrar_horas` |
| cadastrarItemFiscal | ECU005 | dss-05 | interacao-08 | 08 (GRR20224377) | `fiscal.nova` |
| cadastrarMembro | ECU006 | dss-06 | interacao-09 | 09 (GRR20221261) | `membros.novo` |
| gerarRelatorio | ECU007 | dss-07 | interacao-10 | 10 (GRR20221261) | `relatorios.gerar` |

## Decisões documentadas de projeto

- `Ecomp` (conceitual) não vira classe de projeto: a fachada é a aplicação Flask (`app.py`), conforme nota no diagrama de classes.
- `Ecomper` (conceitual) é representado por `Membro`; `Desenvolvedor` e `Participante` referenciam `Membro` (o enunciado modela herança conceitual; na visão de projeto usou-se associação por simplicidade de persistência).
- O enunciado cita RG no fluxo alternativo do ECU006; a implementação valida CPF (dígitos verificadores) e não persiste RG - decisão registrada nos contratos 09.

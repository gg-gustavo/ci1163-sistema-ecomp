# Contrato de Operação 05 — adicionarDesenvolvedorProjeto

Autor: Ulisses Curvello Ferreira (GRR20223829)

## Operação
`adicionarDesenvolvedorProjeto(projeto, desenvolvedor, papel)`

## Referências cruzadas
ECU003 — Cadastrar Desenvolvedor de algum projeto; DSS: [dss-03-adicionar-desenvolvedor.puml](../01-dss/dss-03-adicionar-desenvolvedor.puml).

## Pré-condições
- Direção de Projetos está autenticada.
- `projeto` identifica um `Projeto` existente.
- `desenvolvedor` identifica um `Ecomper` existente e elegível como desenvolvedor.

## Pós-condições
- Uma instância de `Desenvolvedor` (especialização de `Ecomper`) representa o desenvolvedor associado ao projeto, com `papel` informado.
- A associação entre `Projeto` e `Desenvolvedor` foi criada; o projeto passa a possuir o desenvolvedor vinculado.
- Não é criada uma segunda identidade `Ecomper` para um desenvolvedor já existente.

## Anotações
- Se nenhum desenvolvedor for selecionado, o sistema informa o erro e retorna à tela de associação; nenhuma associação é criada.
- O filtro de seleção considera os usuários presentes no sistema. As horas de atividade são registradas separadamente por `registrarHorasAtividade(atividade, membro, horas)`.

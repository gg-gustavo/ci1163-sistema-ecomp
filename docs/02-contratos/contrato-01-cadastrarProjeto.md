# Contrato de Operação 01 — cadastrarProjeto

Autor: Gustavo Gabriel Ripka (GRR20203935)

## Operação
`cadastrarProjeto(dadosProjeto)`

## Referências cruzadas
ECU001 — Cadastrar Projeto; DSS: [dss-01-cadastrar-projeto.puml](../01-dss/dss-01-cadastrar-projeto.puml).

## Pré-condições
- O ator Direção de Projetos está autenticado no sistema.
- `dadosProjeto` contém os dados obrigatórios do projeto e identifica um `Cliente` existente ou seus dados para cadastro.

## Pós-condições
- Uma instância de `Projeto` foi criada com dataInicio, prazoEntrega e descricao informados.
- O `Projeto` foi associado a um `Cliente` (associação obrigatória Cliente [1]). Se o cliente foi informado como novo, a instância de `Cliente` foi criada com os dados fornecidos.
- O `Projeto` foi associado à `Ecomp`, que passa a possuir esse projeto.
- `contratoPdf` permanece sem arquivo até a execução bem-sucedida de `importarContrato(projeto, arquivoPdf)`.

## Anotações
- Se faltar um campo obrigatório, o sistema informa o erro e retorna à tela de cadastro preservando os dados já preenchidos; não cria `Projeto` nem associações.
- A ausência de contrato não impede a confirmação do projeto; o fluxo apresenta a confirmação sem contrato.

# Contrato de Operação 02 — importarContrato

Autor: Gustavo Gabriel Ripka (GRR20203935)

## Operação
`importarContrato(projeto, arquivoPdf)`

## Referências cruzadas
ECU001 — Cadastrar Projeto; DSS: [dss-01-cadastrar-projeto.puml](../01-dss/dss-01-cadastrar-projeto.puml).

## Pré-condições
- O ator Direção de Projetos está autenticado no sistema.
- `projeto` identifica um `Projeto` existente, criado pelo fluxo de cadastro.
- `arquivoPdf` identifica um arquivo PDF disponível para importação.

## Pós-condições
- O atributo `contratoPdf` do `Projeto` identificado passa a referenciar o arquivo importado.
- O arquivo PDF fica associado ao mesmo `Projeto`; não são criadas instâncias de `Cliente`, `Etapa` ou `ItemFiscal` por esta operação.

## Anotações
- Se o ator não importar um arquivo, o fluxo de ECU001 mostra a tela de confirmação sem contrato; `contratoPdf` permanece sem arquivo.
- A validação dos dados obrigatórios do projeto pertence a `cadastrarProjeto(dadosProjeto)`.

# Contrato de Operação 03 — cadastrarEtapasProjeto

Autor: Pedro Henrique Gurski (GRR20224759)

## Operação
`cadastrarEtapasProjeto(projeto, etapas)`

## Referências cruzadas
ECU002 — Cadastrar etapas do desenvolvimento do Projeto; DSS: [dss-02-cadastrar-etapas.puml](../01-dss/dss-02-cadastrar-etapas.puml).

## Pré-condições
- Direção de Projetos está autenticada.
- `projeto` identifica um `Projeto` previamente criado.
- `etapas` contém uma ou mais etapas com os dados necessários para cadastro.

## Pós-condições
- Para cada elemento de `etapas`, uma instância de `Etapa` foi criada com seu cronograma e status inicial.
- Cada nova `Etapa` foi associada ao `Projeto` indicado; o projeto passa a possuir as etapas cadastradas.
- Não são alterados `Cliente`, `Desenvolvedor` ou `ItemFiscal`.

## Anotações
- Se faltar campo obrigatório em alguma etapa, o sistema informa o erro e retorna ao cadastro preservando os dados; as etapas inválidas não são criadas.
- A atualização posterior de cronograma e status é realizada por `atualizarCronogramaEtapa(etapa, cronograma, status)`.

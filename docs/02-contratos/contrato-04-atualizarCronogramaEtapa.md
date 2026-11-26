# Contrato de Operação 04 - atualizarCronogramaEtapa

Autor: Pedro Henrique Gurski (GRR20224759)

## Operação
`atualizarCronogramaEtapa(etapa, cronograma, status)`

## Referências cruzadas
ECU002 - Cadastrar etapas do desenvolvimento do Projeto; DSS: [dss-02-cadastrar-etapas.puml](../01-dss/dss-02-cadastrar-etapas.puml).

## Pré-condições
- Direção de Projetos está autenticada.
- `etapa` identifica uma instância de `Etapa` já associada a um `Projeto`.
- `cronograma` e `status` informados são válidos.

## Pós-condições
- O atributo `cronograma` da `Etapa` identificada contém o novo cronograma.
- O atributo `status` da mesma `Etapa` contém o novo status.
- A associação entre `Etapa` e `Projeto` permanece inalterada; nenhuma nova `Etapa` é criada.

## Anotações
- Se cronograma ou status obrigatório estiver ausente ou inválido, o sistema informa o erro e preserva os valores anteriores da `Etapa`.

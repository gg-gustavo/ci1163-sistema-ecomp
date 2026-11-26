# Contrato de Operação 10 — gerarRelatorio

Autor: Gabriel Shigueo (GRR20221261)

## Operação
`gerarRelatorio(tipo, filtros)`

## Referências cruzadas
ECU007 — Gerar relatório; DSS: [dss-07-gerar-relatorio.puml](../01-dss/dss-07-gerar-relatorio.puml).

## Pré-condições
- O usuário está autenticado no sistema.
- Existem dados de `Atividade` e `Projeto` cadastrados.
- `tipo` corresponde a `atividades` ou `prestacaoContas`; `filtros` contém critérios válidos para o tipo escolhido.

## Pós-condições
- Uma instância de `Relatorio` foi criada com o `tipo` solicitado, os `filtros` informados e `geradoEm` definido para o momento da geração.
- O `Relatorio` agrega referências aos `Projeto` e/ou `Atividade` correspondentes aos filtros e ao tipo solicitado.
- O relatório gerado fica disponível para visualização ou download em PDF; as instâncias de origem não são alteradas.

## Anotações
- ECU007 não define fluxos alternativos. O resultado disponibilizado corresponde ao tipo e aos filtros selecionados.

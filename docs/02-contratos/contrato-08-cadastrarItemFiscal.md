# Contrato de Operação 08 — cadastrarItemFiscal

Autor: Arthur Barreto Godoi (GRR20224377)

## Operação
`cadastrarItemFiscal(projeto, tipo, data, valor)`

## Referências cruzadas
ECU005 — Cadastrar notas fiscais e recibos; DSS: [dss-05-cadastrar-item-fiscal.puml](../01-dss/dss-05-cadastrar-item-fiscal.puml).

## Pré-condições
- Um usuário membro de Adm-Fin está autenticado.
- `projeto` identifica um `Projeto` existente.
- `tipo` é `nota` ou `recibo`; `data` e `valor` estão informados e são válidos.

## Pós-condições
- Uma instância de `ItemFiscal` foi criada com `tipo`, `data` e `valor` informados.
- O `ItemFiscal` foi associado ao `Projeto` indicado, que passa a possuir esse item fiscal.
- Nenhum outro `Projeto`, `Cliente` ou `Relatorio` é criado ou alterado.

## Anotações
- Se qualquer informação obrigatória estiver ausente ou inválida, o sistema alerta o erro e não cria `ItemFiscal` nem associação.

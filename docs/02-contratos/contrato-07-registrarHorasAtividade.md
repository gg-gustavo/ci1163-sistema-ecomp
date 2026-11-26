# Contrato de Operação 07 - registrarHorasAtividade

Autor: Arthur Barreto Godoi (GRR20224377)

## Operação
`registrarHorasAtividade(atividade, membro, horas)`

## Referências cruzadas
ECU004 (extensão); DSS: [dss-04-cadastrar-atividade.puml](../01-dss/dss-04-cadastrar-atividade.puml) - operação de extensão associada ao cadastro de atividade.

## Pré-condições
- O membro está autenticado no sistema e identifica um `Ecomper` cadastrado.
- `atividade` identifica uma `Atividade` existente.
- `membro` participa da `Atividade` e `horas` é uma quantidade positiva válida.

## Pós-condições
- Uma instância de `RegistroHoras` foi criada com a quantidade `horas` informada.
- O novo `RegistroHoras` foi associado à `Atividade` indicada e ao `membro` que realizou o trabalho.
- As instâncias e associações de `Atividade`, `Participante` e `Projeto` não são alteradas.

## Anotações
- Se atividade, membro ou quantidade de horas não satisfizer as pré-condições, a operação não cria `RegistroHoras` e informa a inconsistência.

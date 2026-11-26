# Contrato de Operação 09 — cadastrarMembro

Autor: Gabriel Shigueo (GRR20221261)

## Operação
`cadastrarMembro(dadosMembro)`

## Referências cruzadas
ECU006 — Cadastrar membro da Ecomp; DSS: [dss-06-cadastrar-membro.puml](../01-dss/dss-06-cadastrar-membro.puml).

## Pré-condições
- O usuário que realiza o cadastro está registrado no sistema.
- `dadosMembro` contém os dados pessoais, CPF, RG, cargo e diretorias associados ao membro.

## Pós-condições
- Uma instância de `Ecomper` foi criada com os dados pessoais, CPF, email e cargo informados para o novo membro.
- A `Ecomp` passou a possuir o novo membro; as associações com as diretorias informadas foram registradas.
- O membro pode ser selecionado como participante de `Atividade`; não são criados `Projeto` ou `Desenvolvedor` automaticamente.

## Anotações
- Campo obrigatório ausente: o sistema alerta o erro; não cria `Ecomper` nem associações.
- CPF ou RG inválido: o sistema alerta o erro; não cria `Ecomper` nem associações.

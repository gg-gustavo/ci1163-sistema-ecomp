# Contrato de Operação 06 - cadastrarAtividade

Autor: Ulisses Curvello Ferreira (GRR20223829)

## Operação
`cadastrarAtividade(dadosAtividade)`

## Referências cruzadas
ECU004 - Cadastrar atividade; DSS: [dss-04-cadastrar-atividade.puml](../01-dss/dss-04-cadastrar-atividade.puml).

## Pré-condições
- O usuário está autenticado no sistema.
- `dadosAtividade` contém nome, duração, local, objetivo e resumo, além dos participantes requeridos.
- Cada participante informado corresponde a uma pessoa cadastrada como membro (`Ecomper`).

## Pós-condições
- Uma instância de `Atividade` foi criada com nome, duracao, local, objetivo e resumo informados.
- Para cada membro selecionado, a associação de participação foi criada por meio de uma instância de `Participante` (especialização de `Ecomper`), ligada à `Atividade`.
- A `Ecomp` passa a possuir a nova `Atividade`; nenhuma instância de `RegistroHoras` é criada por esta operação.

## Anotações
- Se algum campo obrigatório estiver ausente, o sistema alerta o erro e não cria `Atividade` nem associações de participação.
- As horas realizadas são registradas posteriormente por `registrarHorasAtividade(atividade, membro, horas)`.

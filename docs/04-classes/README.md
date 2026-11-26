# Diagrama de Classes — Visão de Projeto

O arquivo `diagrama-classes-projeto.puml` mostra a implementação organizada em quatro camadas: templates Jinja (UI), blueprints (Controle), modelos persistidos (Domínio) e acesso a dados (Persistência). Os atributos das entidades reproduzem os campos de `src/models.py`, incluindo chaves primárias e estrangeiras. `Ecomp` não aparece como classe de projeto: na implementação, a facade é o próprio app Flask.

## Decisões GRASP

- **Controller:** cada controller recebe as operações do sistema da área correspondente e coordena os passos do caso de uso. `ProjetosController` atende as cinco operações de projetos; os demais controllers atendem as operações indicadas no plano.
- **Creator:** a criação foi atribuída ao objeto que agrega, contém ou registra a associação sempre que isso se aplica. `Projeto` mantém suas `Etapa`, `Desenvolvedor` e `ItemFiscal`; `Atividade` mantém seus `Participante` e `RegistroHoras`. O controller coordena a construção inicial dos objetos a partir dos dados da tela.
- **Information Expert:** os modelos de domínio guardam seus próprios dados e relações. `Projeto` conhece cliente, etapas, desenvolvedores e itens fiscais; `Atividade` conhece participantes e registros de horas; `Membro` mantém suas participações, desenvolvimentos e registros. Assim, a lógica que depende dessas informações fica próxima dos dados relevantes.
- **Low Coupling:** a UI conversa com controllers, e os controllers usam o `Repositorio` para consultar e persistir; templates não acessam `db.session` diretamente. As associações entre entidades seguem relações já representadas nos modelos, sem introduzir uma classe raiz `Ecomp` na aplicação.
- **High Cohesion:** os controllers são separados por área funcional, e cada modelo representa uma responsabilidade específica. `Repositorio` concentra operações de persistência apoiadas em Flask-SQLAlchemy (`db.session`), sem misturar apresentação ou regras de interface.

As multiplicidades indicam as relações do modelo: projeto–etapas, projeto–desenvolvedores por meio de `Desenvolvedor`, projeto–itens fiscais, atividade–participantes, além das relações de `Membro` com desenvolvimentos, participações e registros de horas.

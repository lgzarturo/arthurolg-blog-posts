# Ideas sobre temas por escribir

- Fundamentos, tokens, uso de modelos, herramientas.
- Agentes, con orquestador y trabajador, Spec Driven Design, Hooks y Worktrees.
- Ahorro de tokens, mcps, agentes personalizados, seguridad, linters y simplificadores de código.
- Depuración de código, integraciones con github actions.
- Claude Code con Ollama.


- Hablar sobre QUERY el nuevo verbo de HTTP
Con QUERY se resuelve este vacío:
- Permite enviar un body (por ejemplo, en JSON) con consultas complejas.
- Mantiene una semántica clara: indica explícitamente que la operación es de solo lectura.
- Es seguro, idempotente y cacheable, por lo que puede beneficiarse de las mismas optimizaciones que GET sin implicar cambios en el estado del servidor.

Este nuevo método puede tener un impacto importante en el diseño de APIs REST, motores de búsqueda, sistemas de filtrado avanzado e incluso en tecnologías como GraphQL, donde tradicionalmente se ha recurrido a POST para consultas complejas.

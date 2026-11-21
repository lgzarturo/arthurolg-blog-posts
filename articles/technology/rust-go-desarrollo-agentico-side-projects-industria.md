---
title: 'Rust y Go en el Desarrollo Agéntico: Del Side Project a la Supervivencia Operativa en la Empresa'
image: 'https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/rust-go-desarrollo-agentico-side-projects-industria.webp'
description: 'Rust y Go en el desarrollo agéntico brillan en side projects, pero en la empresa el stack, el equipo y las decisiones humanas siguen marcando la supervivencia.'
author: 'Arturo López'
date: '2026-11-21'
label: 'Tecnología'
---

Un sábado por la mañana abres la terminal, lanzas un agente de código y en dos horas tienes una utilidad CLI en Rust o un microservicio en Go que compila en un binario único y vuela en local. El lunes por la mañana, en la reunión de arquitectura, alguien propone reescribir un servicio crítico del negocio en ese mismo lenguaje «porque la IA ya escribe casi todo». ¿Cuál de esos dos impulsos sigues?

Conviene separar ambos mundos antes de tomar decisiones caras. **Rust y Go en el desarrollo agéntico** multiplican tu capacidad para construir herramientas enfocadas y de alto rendimiento en *side projects*, pero en la industria el éxito operativo sigue dependiendo de decisiones humanas sobre el stack, el equipo y la claridad del negocio.

Confundir la velocidad de tu taller personal con la estabilidad de una empresa suele terminar en deuda técnica silenciosa.

## El auge del taller personal

Durante años, probar un lenguaje de sistemas en un proyecto de fin de semana implicaba pagar un peaje alto de sintaxis y configuración antes de resolver el problema real. Hoy esa barrera inicial se ha encogido de forma drástica gracias a los agentes de programación.

Según el [Stack Overflow Developer Survey 2026](https://survey.stackoverflow.co/2026/ai), el **73 %** de los desarrolladores ya utiliza asistentes o agentes de código a diario, y entre quienes construyen software con ayuda de IA, un [74.2 % crea scripts pequeños y automatizaciones](https://survey.stackoverflow.co/2026/technology/data/build-tool-ai) mientras un **66.5 %** fabrica herramientas internas para su equipo. En mi propia experiencia con proyectos personales, ese cambio se siente de inmediato: cuando la tarea está bien acotada, Rust y Go dejan de sentirse lejanos y se convierten en piezas quirúrgicas.

El atractivo no es casual. En esa misma encuesta de [lenguajes de Stack Overflow 2026](https://survey.stackoverflow.co/2026/technology/data/languages), Rust alcanzó el **18.0 %** de uso —superando a Go, que marca **16.5 %**— con un **67.4 %** de desarrolladores que desean seguir trabajando con él. Ambos compiladores ofrecen algo que los agentes aprovechan muy bien: contratos estrictos y retroalimentación determinista. Cuando un agente genera código en Rust, el verificador de préstamos y tipos actúa como una red inmediata; cuando genera Go, la simplicidad sintáctica reduce las alucinaciones estructurales y entrega binarios limpios sin depender de entornos virtuales frágiles.

No hace falta imaginar casos abstractos para ver hacia dónde empuja esta ola. En el [Technology Radar Volumen 35](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2026/11/tr_technology_radar_vol_35_en.pdf), Thoughtworks sitúa en *Adopt* herramientas escritas en Rust como `mise` y destaca utilidades enfocadas para flujos agénticos como `nono.sh` o `Hunk`, además de señalar la reescritura del núcleo de `LiteLLM` de Python a Rust por rendimiento. Son herramientas concretas, rápidas y con un alcance claro, muy en la línea de mantener especificaciones acotadas como vimos al armar flujos en [OpenSpec y el stack agéntico definitivo](https://www.arthurolg.com/article/technology_openspec-stack-agentico-12-factor).

En un *side project*, ese enfoque funciona porque el ciclo es corto y el riesgo vive en tu propia máquina.

## Lo que el side project oculta

El problema empieza cuando intentas trasladar esa sensación de ligereza del sábado al entorno productivo del lunes. En tu proyecto personal tú eres el arquitecto, el único revisor, el equipo de soporte y el usuario final; si algo falla, reinicias el proceso y ajustas tres líneas.

En una empresa, el código no muere el domingo por la noche. Convive con sistemas heredados, auditorías de cumplimiento, rotación de personal, integraciones externas y trabajo en equipo. Cuando generas piezas nuevas a gran velocidad sin medir ese entorno, la factura llega por el lado menos esperado: la verificación. En el análisis de [DORA sobre tensiones de la IA](https://dora.dev/insights/balancing-ai-tensions/), basado en más de mil respuestas de ingenieros, se documenta que la inteligencia artificial reduce la fricción para iniciar tareas, pero impone un «impuesto de verificación» (*verification tax*) que eleva la inestabilidad de entrega cuando faltan plataformas internas y pruebas sólidas.

Los números sobre confianza diaria confirman esa brecha. La sección de [confianza en herramientas de IA de Stack Overflow 2026](https://survey.stackoverflow.co/2026/ai/data/ai-trust) muestra que apenas un **6.6 %** confía en la IA para decisiones laborales importantes, mientras que un **69.3 %** perdió tiempo depurando código «plausible pero erróneo» y un **54.2 %** batalló con código difícil de revisar. Si ya cuesta revisar cambios en el lenguaje que tu equipo domina desde hace cinco años, hacerlo en un lenguaje recién adoptado por moda multiplica el riesgo.

Incluso el entusiasmo técnico tiene aristas que un proyecto pequeño disimula. En los resultados del [2025 State of Rust Survey](https://blog.rust-lang.org/2026/03/02/2025-State-Of-Rust-Survey-results/), el **81.97 %** de los participantes señaló que los tiempos de compilación siguen siendo un problema o un aspecto mejorable, y un **41.6 %** expresó preocupación por que el lenguaje se vuelva demasiado complejo. Que un agente escriba el primer borrador rápido no elimina el costo de depurar, compilar ni sostener un sistema complejo en producción, un principio que ya aborde en [Más Allá de Teclear Código](https://www.arthurolg.com/article/technology_mas-alla-teclear-codigo-ia-ingenieria-productividad-condiciones).

Generar software rápido es fácil; asumir la responsabilidad de operarlo durante años es otra historia.

## Las decisiones que la IA no puede tomar

Esa diferencia entre generar y sostener revela dónde sigue estando el verdadero valor de nuestro oficio. Cuando escribir código se vuelve barato, el cuello de botella se desplaza hacia revisar, integrar y mantener acuerdos colectivos claros.

El propio equipo de Go expuso este cambio en [Why Go is an Ideal Language for AI-Assisted Software Engineering](https://developers.googleblog.com/why-go-is-an-ideal-language-for-ai-assisted-software-engineering/), recordando que la dificultad ya no reside en producir líneas nuevas, sino en leerlas y gobernarlas entre varias personas. De hecho, los datos del [2025 Go Developer Survey](https://go.dev/blog/survey2025) muestran una madurez serena que rara vez aparece en redes sociales: el **82 %** usa Go en su trabajo principal, pero el **66 %** reporta que el software que construye no incorpora ninguna función de IA. Los equipos profesionales adoptan Go por simplicidad operativa y concurrencia predecible, no para perseguir cada tendencia.

> «Ningún modelo de lenguaje puede negociar prioridades con producto, asumir la responsabilidad operativa, ni responder por una arquitectura que el equipo no entiende.»

Cuando las organizaciones olvidan esto, caen en lo que Thoughtworks denomina *Human-in-the-loop theater* dentro de su análisis sobre [Enterprise harness](https://www.thoughtworks.com/radar/techniques/enterprise-harness): desarrolladores que terminan aprobando *pull requests* enormes que no pueden auditar realmente, convirtiéndose en simples pararrayos de responsabilidad. Por su parte, el [reporte DORA 2025](https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/) describe a la IA como un espejo y un multiplicador: potencia a equipos cohesionados con límites claros y acelera el desorden en organizaciones fragmentadas.

Elegir el stack correcto, mantener las decisiones documentadas y alinear los objetivos entre ingeniería y negocio no es una tarea delegable a un *prompt*. Requiere contexto histórico, criterio sobre el costo humano de aprender otra herramienta y conversaciones francas que ningún agente puede tener por ti.

## Resistir la moda para sobrevivir operativamente

Aceptar que la IA no decide por nosotros obliga a recuperar una disciplina clásica de arquitectura: administrar con tacañería dónde gastamos nuestra complejidad.

En su ensayo [Choose Boring Technology](https://mcfunley.com/choose-boring-technology), Dan McKinley planteó que toda empresa dispone de un presupuesto muy corto —apenas unos tres *innovation tokens*— para introducir tecnología nueva antes de pagar un costo operativo desproporcionado en monitoreo, contratación y fallos imprevistos. Hoy la tentación es mucho mayor porque un agente puede simular que cualquier lenguaje nuevo es gratis, mientras algunas empresas premian métricas vanidosas de consumo de tokens —el llamado *tokenmaxxing* criticado en el [marco de ROI de DORA](https://dora.dev/ai/roi/report/)— en lugar de medir estabilidad real.

Resistir la moda no significa encerrarse en el pasado ni despreciar a Rust o a Go. Ambos tienen un lugar legítimo en la industria cuando responden a una necesidad real: Rust destaca en pasarelas críticas, *sandboxes* de ejecución y herramientas donde la seguridad de memoria justifica la curva; Go brilla en servicios *cloud-native* y automatización de infraestructura cuando el equipo comparte su cultura de simplicidad. Como defendí en [Liderazgo Técnico: Deja de Copiar Frameworks y Empieza a Copiar Principios](https://www.arthurolg.com/article/programming_liderazgo-tecnico-principios), el problema nunca es la herramienta, sino copiar el resultado ajeno sin entender las restricciones propias.

Para proteger tu operación sin apagar la curiosidad, sirve trazar una frontera explícita entre laboratorio y producción. Usa tus *side projects* con agentes para explorar Rust, Go y utilidades de alto rendimiento sin miedo; aprende sus límites reales mientras mantienes la mente fresca. Pero cuando cruces la puerta del trabajo profesional, exige tres respuestas humanas antes de introducir un stack nuevo: quién del equipo sabrá depurarlo bajo presión dentro de dos años, qué problema medible de negocio justifica la complejidad extra y qué parte del presupuesto operativo estás dispuesto a ceder a cambio.

Decir que no a tiempo cuesta prestigio en una charla de pasillo, pero salva proyectos enteros cuando toca sostenerlos.

## Conclusión

Ese sábado de experimentación y ese lunes de arquitectura no tienen por qué destruirse entre sí. El desarrollo agéntico nos devolvió el placer artesanal de crear herramientas rápidas en Rust o Go para problemas puntuales durante el fin de semana, sin que eso convierta cada ocurrencia personal en un estándar obligatorio para toda una organización.

Al final, la tecnología cambia cada trimestre, pero la supervivencia operativa de un equipo sigue apoyándose en lo mismo de siempre: un stack acorde al negocio, objetivos alineados y decisiones claras asumidas por ingenieros que entienden lo que ponen en producción.

La próxima vez que un agente te entregue en diez minutos un prototipo brillante en un lenguaje que tu equipo aún no opera, ¿tendrás la disciplina de dejarlo en tu taller personal o lo empujarás a producción solo porque hoy parece fácil escribirlo?

Si quieres comentar o compartir tu experiencia, escríbeme en [X (@algforge)](https://x.com/algforge) o abre un issue en el [repositorio](https://github.com/lgzarturo/arthurolg-blog-posts/issues). Una estrella en [GitHub](https://github.com/lgzarturo) también ayuda.

## Referencias

- [Stack Overflow Developer Survey 2026: AI Overview, Stack Exchange Inc.](https://survey.stackoverflow.co/2026/ai)
- [Did you build tools with AI assistance? — Stack Overflow Developer Survey 2026, Stack Exchange Inc.](https://survey.stackoverflow.co/2026/technology/data/build-tool-ai)
- [Programming, scripting, and markup languages — Stack Overflow Developer Survey 2026, Stack Exchange Inc.](https://survey.stackoverflow.co/2026/technology/data/languages)
- [Trust in AI tools — Stack Overflow Developer Survey 2026, Stack Exchange Inc.](https://survey.stackoverflow.co/2026/ai/data/ai-trust)
- [Technology Radar Volume 35, Thoughtworks](https://www.thoughtworks.com/content/dam/thoughtworks/documents/radar/2026/11/tr_technology_radar_vol_35_en.pdf)
- [Enterprise harness — Technology Radar, Thoughtworks](https://www.thoughtworks.com/radar/techniques/enterprise-harness)
- [Balancing AI tensions: Moving from AI adoption to effective SDLC use, DORA / Google Cloud](https://dora.dev/insights/balancing-ai-tensions/)
- [How are developers using AI? Inside our 2025 DORA report, Google Cloud / DORA](https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/)
- [ROI of AI-assisted Software Development report, DORA / Google Cloud](https://dora.dev/ai/roi/report/)
- [2025 State of Rust Survey Results, The Rust Blog](https://blog.rust-lang.org/2026/03/02/2025-State-Of-Rust-Survey-results/)
- [Why Go is an Ideal Language for AI-Assisted Software Engineering, Google Developers Blog](https://developers.googleblog.com/why-go-is-an-ideal-language-for-ai-assisted-software-engineering/)
- [Results from the 2025 Go Developer Survey, The Go Blog](https://go.dev/blog/survey2025)
- [Choose Boring Technology, Dan McKinley](https://mcfunley.com/choose-boring-technology)

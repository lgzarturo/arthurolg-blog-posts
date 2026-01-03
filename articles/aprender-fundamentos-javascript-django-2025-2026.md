---
title: 2025 volver a los fundamentos para construir mejor software, y por qué aprender será mi constante en 2026
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/2025-springboot-django-stack-side-projects.webp
description: Un recorrido técnico y honesto por mi aprendizaje en 2025, dominar JavaScript nativo, entender el DOM y React desde sus bases, apostar por PWAs, Django y arquitectura consciente, y la promesa de seguir aprendiendo en 2026 con criterio, no por moda.
author: Arturo López
date: 2025-01-02
label: Reflexión
---

2025 no fue un año de acumular tecnologías. Fue un año de **des-aprender**. Y eso, aunque incomoda, es señal de progreso real.

Durante mucho tiempo el ecosistema frontend empuja a correr antes de caminar. Frameworks encima de frameworks, abstracciones sobre abstracciones, y una falsa sensación de productividad que se evapora cuando algo se rompe fuera del “happy path”. En 2025 decidí frenar ese impulso de aprender el framework de moda y volver al terreno firme: **JavaScript nativo**. No como nostalgia, sino como ingeniería.

La decisión fue simple y humilde: no se puede dominar lo que no se entiende. Nextjs, React, Vue, Astro, Svelte o lo que venga después no son magia, son capas. Y una capa solo es útil cuando sabes qué está ocultando. Es imposible tomar buenas decisiones técnicas sin entender las bases. Así que 2025 fue el año de **reconstruir desde lo fundamental**.

Dominar JavaScript nativo me obligó a enfrentarme al DOM real, no al DOM idealizado que muestran los tutorials. El DOM como es: mutable, imperativo, a veces torpe, pero predecible si lo respetas. Entender el ciclo de vida de los eventos, la propagación, la diferencia entre delegación y listeners directos, el costo real de manipular nodos, la relación entre rendimiento y legibilidad. Nada glamoroso. Todo esencial. Esos conocimientos cambiaron por completo mi forma de escribir código frontend, hoy más consciente y pienso que más eficiente.

Desde ahí, construir **PWAs** dejó de sentirse como seguir una receta y empezó a sentirse como arquitectura. Service Workers dejaron de ser “ese archivo raro que copias y pegas” para convertirse en una herramienta concreta con tradeoffs claros. Cache strategies, offline-first, invalidación, sincronización en background. Todo eso solo tiene sentido cuando entiendes qué hace el navegador por ti y qué no.

> PWAs no son solo apps que funcionan offline. Son una forma de pensar la experiencia del usuario desde la resiliencia y la performance. Ahora lo entiendo mejor.

Ese entendimiento cambió por completo mi relación con React. Ya no lo veo como algo mágico, sino como una **implementación específica de una idea**: gestionar estado y eventos de forma declarativa sobre una capa virtual que reduce el costo cognitivo en ciertas clases de problemas. El Virtual DOM no es mejor porque sí. Es mejor cuando el problema lo justifica. Y ahora sé cuándo no lo hace. Desde esa perspectiva, he podido escribir componentes React más simples, más eficientes y más fáciles de razonar, porque ahora sé qué está pasando debajo del capó.

Ese fue uno de los aprendizajes más valiosos de 2025: **no hay soluciones universales, solo decisiones contextualizadas**. El Virtual DOM es una buena opción. No es la única. No siempre es la óptima. Y entender eso te libera de discusiones estériles y te devuelve el control técnico.

Al mismo tiempo, trabajar más cerca del metal me llevó a escribir aplicaciones **más modulares**, no por moda, sino por necesidad. Cuando no tienes un framework imponiéndote estructura, cada decisión pesa. Eso te obliga a pensar en límites claros, responsabilidades bien definidas y contratos explícitos entre módulos. Arquitectura por convicción, no por plantilla.

Así, 2025 fue un año de **menos dependencias**, no por minimalismo, sino por pragmatismo. Cada librería añadida es un costo: de mantenimiento, de seguridad, de performance. Aprender a evaluar ese costo frente al beneficio real que aporta fue un ejercicio constante. No todo lo que brilla es oro, y no todo lo que resuelve un problema vale la pena si introduce complejidad innecesaria.

El impacto más visible de ese enfoque fue en **SEO y performance**. No como necesidad, sino como parte del diseño inicial. Renderizar bien desde el inicio, minimizar JavaScript innecesario, entender qué bloquea el render, qué afecta el LCP, qué rompe la indexación. Cuando sabes cómo el navegador construye la página paso a paso, optimizar deja de ser un acto reactivo y se convierte en una consecuencia natural del diseño.

> Pensar en SEO desde el inicio no es solo para motores de búsqueda. Es pensar en accesibilidad, en performance y en experiencia de usuario. Todo está conectado. Es una forma de respeto hacia quienes usan tu software.

En paralelo, 2025 también fue un año de aceptar algo que muchos evitan decir en voz alta: **no todo necesita ser Node**. Node es una gran herramienta. También es una distracción cuando se usa por inercia. Decidir dejarlo de lado temporalmente no fue un rechazo, fue parte de tener un enfoque más claro.

El foco se movió hacia **aplicaciones monolíticas con Django**, por pragmatismo. Pienso que un monolito bien diseñado reduce fricción, acelera iteración y elimina complejidad innecesaria en side projects. Autenticación, ORM, admin, seguridad, todo integrado, todo probado. Menos glue code, más lógica de negocio.

Combinar Django con JavaScript nativo resultó ser una dupla sorprendentemente poderosa. Backend sólido, frontend consciente, límites claros. Nada de microservicios prematuros. Nada de pipelines inflados. Solo software que hace lo que promete y se puede mantener. Integrarlo con GitHub Actions y Digital Ocean me dio un stack completo, simple y efectivo.

Mientras tanto, en lo profesional (dentro del trabajo diario), la decisión no cambia. **Kotlin y Spring Boot** siguen siendo el estándar. Ahí el foco no está en explorar, sino en **profundizar**. Mejores prácticas, arquitectura limpia, observabilidad, resiliencia. No hay glamour en refinar un sistema en producción, pero ahí es donde se construye criterio técnico real.

En ese contexto nació y creció [**Spring Boot Challenge**](https://springboot-challenge.lgzarturo.com/). No como un curso más, sino como un artefacto de aprendizaje activo. Preguntas diarias, dificultad incremental, enfoque en fundamentos. Aprender Spring Boot no como framework, sino como consecuencia de entender Java, el ecosistema JVM y los principios detrás de las decisiones del framework.

[El repositorio complementario no es un adorno](https://github.com/lgzarturo/springboot-course). Es la prueba de que el conocimiento se consolida cuando se materializa. Código que se lee, se ejecuta, se rompe y se corrige. Enfocado en el aprendizaje real, busco que cada línea tenga un propósito claro. Me he tomado ese proyecto como un ejercicio de disciplina técnica, no como una exhibición, y eso se nota en cada commit.

Mirando hacia 2026, la promesa no es aprender “más cosas”. Es aprender **mejor**.

TypeScript llegará, pero no como un salto ciego. Llegará cuando el dolor de tipado dinámico lo justifique. Cuando el tamaño del proyecto y la complejidad del dominio lo pidan. No antes. TypeScript no es una mejora automática, es una inversión que debe pagarse sola.

Next.js también tendrá su lugar, especialmente cuando el equilibrio entre SSR, SSG y cliente lo haga razonable. Entendido como una herramienta para resolver problemas específicos de entrega y experiencia, no como un reemplazo automático de pensar.

Los side projects de 2026 que continuare trabajando y los nuevos seguirán ese stack: Django, JavaScript nativo, TypeScript cuando aporte, Next.js cuando tenga sentido. Menos experimentación caótica, más exploración dirigida.

Y esa es quizá la constante más importante que deja 2025: **aprender no es acumular, es refinar**.

Cada año debería reducir el ruido y aumentar la señal. Menos dependencias innecesarias. Más comprensión profunda. Más decisiones explícitas. Más responsabilidad técnica.

La industria premia la novedad. La ingeniería real premia el criterio. Para mi, 2025 fue un ejercicio de construir ese criterio desde abajo, sin atajos. 2026 será la continuación natural de ese proceso, con una promesa clara y no negociable: **seguir aprendiendo como única constante**, pero hacerlo con intención, contexto y rigor.

Porque al final, los lenguajes cambian, los frameworks pasan, las modas se reciclan. Lo que permanece es la capacidad de entender sistemas, cuestionar abstracciones y elegir conscientemente. Todo lo demás es ruido.

2026 será otro año para profundizar en eso.
¿Y el tuyo?

¡Feliz 2026!

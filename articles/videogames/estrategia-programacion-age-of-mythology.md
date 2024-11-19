---
title: Cómo Age of Mythology Enseña Tácticas para Desarrolladores
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/tacticas-para-programadores.webp
description: Las estrategias de Age of Mythology pueden aplicarse al desarrollo de software. Aprende a equilibrar recursos, adaptarte rápidamente y construir proyectos sostenibles mientras disfrutas de este clásico de los RTS.
author: Arturo López
date: 2024-11-18
label: AOE
---

## Lecciones desde el Mundo de Age of Mythology

En el mundo del desarrollo de software, muchas veces nos enfrentamos a desafíos similares a los de un estratega en un videojuego de estrategia en tiempo real (RTS). Juegos como *Age of Mythology*, con su combinación de gestión de recursos, batallas estratégicas y narrativa inmersiva, creo que ofrecen más que entretenimiento: nos brindan lecciones valiosas que pueden aplicarse al desarrollo de software. En este artículo voy a realizar analogías entre las tácticas de *Age of Mythology* y las estrategias de desarrollo de software, explorando cómo los principios de un RTS pueden ser útiles para escribir y mantener código eficiente, retrocompatible y sostenible.

## El Arte de la Planificación Inicial

En *Age of Mythology*, cada partida comienza con una evaluación del entorno. ¿Qué recursos tienes a tu disposición? ¿Cuáles son tus objetivos inmediatos y a largo plazo? Este análisis inicial es fundamental para determinar cómo vas a proceder: ¿priorizarás una economía fuerte con edificios y unidades básicas, o te arriesgarás en un ataque temprano?

El desarrollo de software comparte esta necesidad de una planificación sólida desde el principio. Antes de escribir una sola línea de código, debes analizar los requerimientos del proyecto, el entorno tecnológico y las necesidades del cliente. Así como construir un ejército homogéneo en *Age of Mythology* podría dejarte vulnerable a ciertos tipos de unidades enemigas, elegir una arquitectura inadecuada puede resultar en un sistema rígido e ineficiente.

- **En el juego**: Elegir al dios inicial y las tecnologías define tu estrategia.
- **En programación**: Elegir el stack tecnológico adecuado define la base del proyecto.

Por ejemplo, si en el juego eliges a Zeus, tienes ventajas en combate directo; si eliges a Hades, obtienes más apoyo defensivo. En programación, elegir Python puede ser ideal para prototipos rápidos, pero quizás no sea la mejor opción para sistemas de alta concurrencia. Como en un RTS, tus decisiones iniciales afectan todo el flujo posterior.

## Microgestión y Refactorización: Pequeños Ajustes, Grandes Resultados

Algo que a mi se me dificulta, es la microgestión, pero en el juego es fundamental. Es por eso que en *Age of Mythology*, controlar a tus héroes y unidades en tiempo real puede marcar la diferencia entre la victoria y la derrota. Por ejemplo, mover a Perseo para que use su habilidad especial contra un cíclope enemigo en el momento preciso puede salvar a tu ejército. Sin embargo, abusar de la microgestión puede distraerte de los objetivos más importantes, como construir una economía sólida o fortificar tus defensas.

En la programación, la microgestión se refleja en la refactorización. Ajustar pequeños fragmentos de código puede mejorar la legibilidad y eficiencia, pero si te obsesionas con detalles menores sin un propósito claro, podrías perder de vista la visión general del proyecto. Es importante equilibrar estas tareas: arreglar problemas locales sin comprometer el flujo global.

> La microgestión es una parte fundamental de cualquier RTS. En *Age of Mythology*, controlar a tus héroes y unidades en tiempo real puede marcar la diferencia entre la victoria y la derrota.

- **En el juego**: Usar la caballería para flanquear una catapulta requiere precisión y oportunidad.
- **En programación**: Cambiar funciones específicas para mejorar su eficiencia es crucial, pero no debe romper el sistema general.

Un ejemplo del juego es cuando debes usar a la caballería para atacar catapultas enemigas, mientras los arqueros y las médulas distraen a otras unidades. En programación, esto sería equivalente a arreglar un bug crítico sin crear regresiones en otras áreas del sistema.

## Pensar Fuera de la Caja: Soluciones Creativas a Problemas Complejos

Una de las misiones más memorables de *Age of Mythology* es enfrentarse al cíclope hijo de Poseidón. Esta misión te obliga a pensar estratégicamente: las catapultas son devastadoras, pero enfrentarlas directamente con la milicia es suicida. Además, el cíclope es resistente a la mayoría de las unidades convencionales. La solución no está en crear un ejército masivo, sino en aprovechar la velocidad de la caballería y la habilidad única de Perseo para derrotar a enemigos mitológicos.

En programación, también enfrentamos problemas que no tienen soluciones obvias. Un ejemplo podría ser modificar una funcionalidad crítica sin romper la retrocompatibilidad. Si abordas el problema sin un plan claro, puedes terminar con un código desordenado que será difícil de mantener. En cambio, encontrar una solución elegante, como introducir patrones de diseño o estrategias de abstracción, puede resolver el problema de manera eficiente.

- **En el juego**: Usar a Perseo en el momento exacto para derrotar al cíclope simboliza la necesidad de aplicar habilidades específicas.
- **En programación**: Implementar un patrón de diseño como Strategy o Decorator en lugar de realizar un hack rápido refleja un pensamiento a largo plazo.

## Adaptación y Solución de Problemas en Tiempo Real

Los RTS no perdonan la indecisión. En *Age of Mythology*, un ataque sorpresa enemigo puede desbaratar incluso las mejores estrategias. ¿Tienes recursos suficientes para reconstruir? ¿Puedes redirigir tus tropas a tiempo para defender tu base? Esta capacidad de adaptación rápida es crucial tanto en el juego como en la programación.

En el desarrollo de software, esto se traduce en la capacidad de resolver bugs o problemas críticos mientras mantienes el proyecto en marcha. Un ejemplo sería descubrir que una biblioteca de terceros tiene una vulnerabilidad y necesitas reemplazarla de inmediato. Si no tienes un plan de contingencia, como pruebas automatizadas o una arquitectura modular, este tipo de problemas puede descarrilar todo el proyecto.

- **En el juego**: Reaccionar a un ataque sorpresa con torres defensivas simboliza implementar un parche de emergencia.
- **En programación**: Resolver un bug crítico en producción mientras mantienes el sistema estable es una habilidad esencial.

## Optimización de Recursos: Modularidad y Economía en el Código

En *Age of Mythology*, manejar recursos como madera, oro y comida de manera eficiente es esencial para mantener tu ejército y avanzar en la campaña. Si gastas todo tu oro en unidades caras sin construir una economía sostenible, te quedarás sin opciones cuando el enemigo contraataque.

En programación, la economía de recursos se traduce en modularidad del código. Un sistema bien modularizado permite reutilizar componentes, reduciendo el esfuerzo necesario para implementar nuevas funcionalidades. Por el contrario, un diseño monolítico consume más tiempo y esfuerzo, como un ejército desbalanceado que depende de una sola táctica.

- **En el juego**: Mantener un equilibrio entre economía y ejército simboliza un sistema bien diseñado.
- **En programación**: Dividir el código en módulos reutilizables asegura eficiencia y escalabilidad.

## Retrocompatibilidad y Sustentabilidad a Largo Plazo

Una de las claves para avanzar en *Age of Mythology* es construir sobre una base sólida. No solo necesitas derrotar a los enemigos actuales, sino también prepararte para los desafíos futuros. Esto incluye mantener tus defensas mientras expandes tu territorio y acumulas recursos para fases avanzadas.

En programación, esto se refleja en la retrocompatibilidad. Al agregar nuevas funcionalidades, es crucial no romper las existentes. Cambiar el comportamiento de una API, por ejemplo, puede causar fallos en los sistemas que dependen de ella. Esto requiere un enfoque cuidadoso, como lo harías al planificar un ataque mientras mantienes tus defensas intactas.

- **En el juego**: Crear un ejército equilibrado para adaptarse a diferentes enemigos refleja la preparación para desafíos desconocidos.
- **En programación**: Implementar pruebas automatizadas para asegurar la estabilidad del sistema simboliza la previsión estratégica.

## El Peligro de "Avanzar por Avanzar"

En *Age of Mythology*, apresurarte a atacar al enemigo sin una estrategia clara puede ser desastroso. Si gastas todos tus recursos en un ejército sin planificar tus defensas o economía, podrías encontrarte en una posición insostenible. En programación, este error se manifiesta cuando se toman atajos para implementar funcionalidades rápidamente sin considerar el impacto a largo plazo. Esto resulta en "spaghetti code", un sistema difícil de mantener y propenso a errores.

- **En el juego**: Enviar todas tus tropas al ataque sin prever refuerzos es como modificar el código sin pensar en la retrocompatibilidad.
- **En programación**: Agregar funcionalidades sin refactorizar o documentar adecuadamente genera deuda técnica.

## El Arte de la Estrategia Aplicada al Desarrollo

*Age of Mythology* no es solo un juego; es una lección de planificación, gestión y adaptación. Desde manejar recursos hasta tomar decisiones críticas en tiempo real, los principios que aprendemos en el juego son sorprendentemente aplicables al desarrollo de software. La paciencia, el análisis y la capacidad de pensar fuera de la caja son habilidades clave tanto para los estrategas como para los programadores.

La próxima vez que enfrentes un bug complejo o una tarea desafiante en tu proyecto, considera abordarlo como lo harías en *Age of Mythology*: analiza el terreno, planea tu estrategia y ejecuta con precisión. Y, sobre todo, recuerda que tanto en el juego como en el desarrollo, el verdadero éxito no es solo avanzar, sino construir algo sostenible y eficiente que pueda resistir la prueba del tiempo.

¿Y tú, cómo aplicarías estas lecciones estratégicas en tu día a día como programador?

---
title: Cómo aplicar TDD paso a paso en un CRUD con Spring Boot y arquitectura hexagonal
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/tdd-crud-spring-boot-arquitectura-hexagonal-header.webp
description: Aprende a crear un CRUD con Spring Boot aplicando Desarrollo Guiado por Pruebas (TDD) y arquitectura hexagonal. Descubre cómo estructurar tu proyecto, escribir pruebas unitarias y de integración con MockMvc, y mantener un código limpio y escalable.
author: Arturo López
date: 2025-10-28
label: SpringBoot
---

## Cómo aplicar TDD en proyectos reales con Spring Boot y Kotlin

En desarrollo backend, escribir pruebas no debería sentirse como un trámite. Si lo haces bien, las pruebas se convierten en una herramienta para pensar, no solo para verificar. Esa es la esencia de **TDD (Test-Driven Development)**: diseñar software a través de las pruebas.

Este principio está reflejado en el proyecto [**springboot-course**](https://github.com/lgzarturo/springboot-course), particularmente en la rama [**feature/milestone-01-persistence**](https://github.com/lgzarturo/springboot-course/tree/feature/milestone-01-persistence). No es un curso tradicional, sino un **recurso técnico gratuito**, pensado para mostrar cómo construir una API REST con **Spring Boot y Kotlin** aplicando patrones de arquitectura limpia, hexagonal y buenas prácticas de ingeniería.

---

## TDD como brújula de diseño

TDD no es solo escribir tests antes del código. Es una forma de diseñar sistemas más mantenibles y predecibles.
El ciclo clásico —**Red → Green → Refactor**— nos obliga a pensar primero en la intención del código antes de su implementación.

En este enfoque, cada prueba responde a una pregunta concreta:

> ¿Qué debería hacer esta pieza de código si todo funciona como espero,
> y qué debería hacer si algo sale mal?

Cuando te haces esa pregunta antes de escribir una línea, estás construyendo software que se entiende solo.

---

## Qué tiene sentido probar (y qué no)

Uno de los errores más comunes es medir la calidad del proyecto solo por el porcentaje de cobertura.
La cobertura sirve como guía, pero el objetivo real es **cubrir los caminos que importan**.

### Qué sí probar

* La lógica que tú escribiste y que puede fallar: validaciones, decisiones, transformaciones.
* Los servicios que definen reglas de negocio.
* Los flujos con errores controlados.
* Los endpoints que agregan lógica o validaciones antes de llamar al servicio.

### Qué no probar

* El framework. No tiene sentido comprobar que `@Autowired` o JPA funcionen.
* Entidades, DTOs y repositorios simples.
* Configuraciones triviales o beans sin lógica condicional.

En otras palabras, simplificando:

> “Si el código puede romper algo que el framework no controla, pruébalo.
> Si el código solo pasa datos al framework, no lo hagas.”

---

## Cómo aplicarlo en el proyecto

El repositorio `springboot-course` expone una estructura clara basada en **arquitectura hexagonal**, donde el dominio está completamente separado de la infraestructura.
Esto facilita que cada capa tenga sus propias pruebas enfocadas:

* **Dominio:** se prueba con mocks, aislado de frameworks.
* **Infraestructura:** se valida con tests de integración (por ejemplo, con `@DataJpaTest`).
* **Controladores:** se prueban con `MockMvc` solo cuando hay lógica o validaciones relevantes.

Este diseño te permite aplicar TDD sin fricción: primero defines el comportamiento esperado (test), luego escribes el código mínimo para pasarlo y finalmente lo mejoras.

---

## Más que un curso, un recurso vivo

El objetivo de `springboot-course` no es enseñar Spring Boot desde cero, sino mostrar **cómo se construye un proyecto profesional desde la base**, aplicando prácticas que escalan.

Cada milestone del repositorio se enfoca en un aspecto clave del desarrollo backend:

* Persistencia y entidades.
* Casos de uso y servicios.
* Exposición de endpoints REST.
* Manejo de errores y validaciones.
* Integración con herramientas reales.

El valor está en que puedes clonar el proyecto, navegar el código y entender cómo las piezas encajan. Es una guía viva, no una presentación estática.

---

## Una reflexión final

Escribir pruebas no es una tarea adicional. Es parte del diseño.
Cuando trabajas con TDD, no piensas solo en que el código funcione, sino en **por qué** y **bajo qué condiciones** debería hacerlo.

El resultado no es solo un sistema con menos bugs, sino un código más claro, más estable y más fácil de evolucionar.
Y eso, al final, es lo que separa a un desarrollador que escribe código de uno que **diseña software**.

---

📚 Puedes explorar el repositorio aquí:
👉 [github.com/lgzarturo/springboot-course](https://github.com/lgzarturo/springboot-course)
📂 Rama: [feature/milestone-01-persistence](https://github.com/lgzarturo/springboot-course/tree/feature/milestone-01-persistence)
📂 Proceso de pruebas: [TDD en acción](https://github.com/lgzarturo/springboot-course/blob/feature/milestone-01-persistence/docs/course/week-03/01-crud-con-tdd.md)

¡Happy coding! 🚀

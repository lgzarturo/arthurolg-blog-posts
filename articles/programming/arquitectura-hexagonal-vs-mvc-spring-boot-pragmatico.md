---
title: Arquitectura Hexagonal vs. MVC - El fin de la ceremonia innecesaria en Spring Boot
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/arquitectura-hexagonal-mvc-spring-boot-tablet.webp
description: ¿La arquitectura hexagonal está matando tu productividad? Descubre por qué la "ceremonia" técnica aleja a los desarrolladores junior y cómo migrar a un MVC orientado al dominio para recuperar la agilidad sin perder la calidad técnica.
author: Arturo López
date: 2026-03-08
label: Programación
---

## La Ilusión de la Catedral de Código: De la Arquitectura Hexagonal al Pragmatismo del Dominio

Muchos ingenieros senior caen en la misma trampa: construir un búnker nuclear para proteger una caseta de jardín. Mi estructura inicial, basada en una arquitectura hexagonal (Ports & Adapters), es técnicamente impecable en el papel. Separar el dominio de la infraestructura, utilizar mappers para cada transición de estado y definir contratos mediante puertos de entrada y salida. Sin embargo, el abandono de tres meses del proyecto y he visto la dificultad de programadores junior para navegar en él han revelado una verdad incómoda: la arquitectura está sofocando la agilidad.

A mi, también me ha pasado. Al volver al proyecto, me encontré con un laberinto de carpetas y clases que me obligó a reconstruir mentalmente el mapa de mi propio código. La "ceremonia" técnica, que en su momento parecía una inversión en calidad, se ha convertido en una barrera de entrada. Es hora de admitir que la arquitectura hexagonal, aunque elegante, no es la solución universal para todos los proyectos. En su lugar, propongo una migración hacia un **MVC orientado al dominio**, que mantiene la separación de responsabilidades sin la sobrecarga de los puertos y adaptadores, permitiendo que el código sea más accesible y mantenible para desarrolladores de todos los niveles.

### 1. El Costo Oculto de la "Ceremonia" Técnica

La arquitectura hexagonal no es gratuita; se paga con "ceremonia" (boilerplate y saltos cognitivos). En la implementación actual, para realizar un simple health check de un `Ping`, el flujo debe atravesar:

1. Un `PingController` en la capa de infraestructura.
2. Un `PingMapper` para convertir el DTO.
3. Una interfaz `PingUseCase` (puerto de entrada).
4. Una implementación `PingService` en el dominio.
5. Un modelo `Ping` (POKO).
6. Un `PingResponse` de vuelta a la infraestructura.

Para un desarrollador junior o mid, esta fragmentación es una barrera de entrada. En lugar de entender la lógica de negocio, gastan su energía mental mapeando el rastro de migajas entre paquetes. La arquitectura "gritona" (Screaming Architecture) que buscaba, donde las carpetas revelan el propósito del sistema, terminó gritando demasiado fuerte sobre *cómo* está construida y demasiado poco sobre *qué* hace el software.

Entonces, ¿cuál es la alternativa? Un MVC orientado al dominio que mantenga la esencia de la separación de responsabilidades pero sin la burocracia de los puertos. En este modelo, el controlador se comunica directamente con el servicio, y el servicio maneja la lógica de negocio sin necesidad de interfaces intermedias a menos que realmente aporten valor (por ejemplo, para casos de uso complejos o para facilitar pruebas). Esto reduce la cantidad de clases y capas que un desarrollador debe entender para contribuir al proyecto, aumentando la productividad y la satisfacción del equipo.

### 2. El Test de los Tres Meses: La Memoria Caché del Desarrollador

Esta decisión surge de mi incapacidad para retomar el proyecto tras 90 días de pausa, por lo tanto creo que es el indicador definitivo de que la carga cognitiva es excesiva. La arquitectura hexagonal pura asume que el desarrollador mantendrá un mapa mental de las abstracciones. Cuando ese mapa se borra, volver a entrar en el proyecto requiere una "rehidratación" de contexto lenta y costosa.

El modelo MVC tradicional, aunque a menudo criticado por su tendencia al acoplamiento, tiene una ventaja imbatible: la **predictibilidad**. Cualquier desarrollador de Spring Boot sabe dónde buscar un controlador y un servicio. Al intentar "forzar" la pureza del dominio mediante puertos y adaptadores en un proyecto que aún está definiendo su núcleo, terminé creando una estructura rígida que no permitió el crecimiento orgánico.

Es por ello, que lo dejo como anécdota personal, pero creo que es un test de estrés real para cualquier arquitectura: si el desarrollador no puede recordar su propio código después de tres meses, la arquitectura ha fallado el test de la realidad. En este caso, la solución no es más documentación o entrenamiento, sino una reestructuración que permita que el código sea más intuitivo y accesible para cualquier programador, sin sacrificar la calidad técnica.

### 3. La Falacia de la Flexibilidad Total

El argumento principal para usar Puertos y Adaptadores es la capacidad de cambiar de tecnología sin afectar el dominio (por ejemplo, pasar de JPA a MongoDB). Seamos realistas: en el 95% de los proyectos empresariales, ese cambio nunca ocurre. Construir interfaces para repositorios que solo tienen una implementación (`JpaUserRepository`) es aplicar ingeniería para un futuro hipotético a costa de un presente ineficiente.

| Arquitectura Actual (Hexagonal) | Propuesta (MVC Orientado al Dominio) |
| --- | --- |
| Alta separación, alta fricción. | Separación moderada, baja fricción. |
| Inversión de dependencias total. | Dependencia directa sobre el framework (Spring). |
| Múltiples DTOs y Mappers por entidad. | DTOs compartidos cuando el riesgo es bajo. |
| Difícil de navegar para principiantes. | Curva de aprendizaje plana. |

En lugar de diseñar para un futuro incierto, he llegado a la conclusión de que es más pragmático diseñar para el presente. Esto no significa sacrificar la calidad o la mantenibilidad, sino encontrar un equilibrio que permita a los desarrolladores ser productivos sin sentirse atrapados en una arquitectura que parece más un rompecabezas que una herramienta para resolver problemas de negocio. El MVC orientado al dominio ofrece esa flexibilidad sin la sobrecarga de la "ceremonia" técnica, permitiendo que el equipo se enfoque en lo que realmente importa: escribir código limpio y efectivo que resuelva problemas reales.

### 4. Reestructuración: MVC con Enfoque en el Dominio

No se trata de volver al "código espagueti", sino de adoptar un **MVC Pragmático**. Puedo mantener la esencia de tus principios de diseño sin la burocracia de los puertos. La propuesta es consolidar las capas:

* **Web (Controller + DTOs):** El punto de entrada. Spring Boot nació para esto. Me basare en el controlador para manejar las solicitudes HTTP y los DTOs para la validación y transformación de datos.
* **Service (Negocio):** Aquí reside la lógica. Si un servicio es simple, no necesita un `UseCase` previo.
* **Domain/Entity:** En proyectos Spring modernos, a menudo es más eficiente que la entidad JPA y el modelo de dominio sean lo mismo, a menos que la lógica de persistencia sea radicalmente distinta a la de negocio.
* **Data/Repository:** Acceso directo a Spring Data JPA. Sin interfaces innecesarias a menos que realmente aporten valor (por ejemplo, para casos de uso complejos o para facilitar pruebas).

### 5. TDD: El Único Superviviente Innegociable

Independientemente de si las carpetas se llaman `infrastructure` o `web`, el TDD (Test Driven Development) debe seguir siendo el norte. La ventaja de tu arquitectura actual es que facilita los tests unitarios al no depender de Spring en el dominio. En el nuevo esquema, mantendremos esta capacidad:

* **Tests de Unidad:** Para la lógica de negocio pura en los servicios.
* **Tests de Integración:** Para validar que la API responde correctamente (MockMvc).

### Conclusión

Mi decisión de restructurar hacia un estándar MVC orientado al dominio es un movimiento de **pragmático**. Estoy priorizando la mantenibilidad real sobre la elegancia teórica. Un proyecto que nadie puede mantener no es una buena arquitectura; es un monumento al ego del arquitecto. Al simplificar la estructura de carpetas y reducir la ceremonia de mappers y puertos, permito que el código "respire" y que mi tiempo lo pueda dedicar a lo que realmente importa: resolver problemas de negocio con código limpio, tipado y modular.

La arquitectura debe servir al desarrollador, no al revés. Si el patrón hexagonal te impide recordar tu propio código tras tres meses, el patrón ha fallado el test de estrés de la realidad.

---
title: 'El Retorno a la Trinchera: Spring Boot 4.1.1, JDK 25 y la Hoja de Ruta del Gran Hotel Pokémon'
image: 'https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/spring-boot-4-1-1-jdk-25-hoja-de-ruta-hotel-pokemon.webp'
description: 'Retomamos el desarrollo del Gran Hotel Pokémon tras migrar a Spring Boot 4.1.1 y JDK 25 con 80% de cobertura, encarando la seguridad y la Liga de Campeones.'
author: 'Arturo López'
date: '2026-09-06'
label: 'Spring Boot'
---

## La Realidad del Aprendizaje: Cuando el Calendario Choca con la Vida

Voy muy atrasado con el curso de Spring Boot. Lo digo sin rodeos, sin excusas corporativas y sin adornos. Cuando tracé el cronograma original para construir la API REST del Gran Hotel Pokémon en diez semanas temáticas, imaginé un avance lineal y constante: cada fin de semana representaría un templo conquistado, cada commit cerraría un capítulo narrativo impecable y para estas fechas ya deberíamos tener el sistema de reservas y pagos operando a pleno rendimiento en la nube.

La realidad del desarrollo de software, sin embargo, rara vez respeta las tablas de Excel o los tableros Kanban. Entre responsabilidades laborales, resolución de incidentes de producción, compromisos familiares y la inevitable fricción técnica de cualquier proyecto serio, el calendario previsto se desbordó por completo. Durante días sentí esa punzada de culpa que cualquier programador reconoce: la sensación de que el proyecto se enfría y de que las buenas intenciones quedan archivadas en un rincón olvidado de GitHub.

Fue en ese momento cuando recurrí a una de mis lecturas de cabecera: las *Meditaciones* de Marco Aurelio y el principio estoico de la dicotomía del control. No controlamos los imprevistos externos ni el ritmo al que avanza el resto del mundo; lo único que está bajo nuestro dominio absoluto es la actitud con la que nos sentamos frente al teclado y la integridad técnica del código que producimos en el presente.

En los videojuegos de estrategia en tiempo real, enviar a tus soldados a una batalla sin antes asegurar las canteras de piedra, los almacenes de madera y las torres de defensa es una receta garantizada para la derrota. Lo mismo sucede en la arquitectura de software. Kai, nuestro entrenador protagonista en el Gran Hotel Pokémon, no podía lanzarse a ciegas contra los gimnasios avanzados de Ciudad Azafrán sin antes afianzar su equipo base.

> "El verdadero valor del artesano del software no se mide por la velocidad con la que acumula commits apresurados, sino por su paciencia para forjar cimientos que resistan el paso del tiempo y los embates del cambio."

Aceptar el retraso no significó rendirse. Significó hacer una pausa estratégica, evaluar el estado de la base de código, actualizar nuestras herramientas al estado del arte más moderno y rediseñar una hoja de ruta pragmática que nos lleve no solo a completar el proyecto base, sino a dominar los desafíos de ingeniería más avanzados del mercado.

---

## El Salto Tecnológico

La primera decisión deliberada durante esta pausa fue técnica y contundente: en lugar de continuar construyendo sobre dependencias que envejecían en nuestro repositorio, decidí actualizar el proyecto completo a **Spring Boot 4.1.1** y **JDK 25**. Esta migración quedó documentada y probada en la rama [`feature/milestone-03-update-sb`](https://github.com/lgzarturo/springboot-course/pull/64).

Muchos equipos temen actualizar dependencias mayores a mitad de un proyecto. Existe un pánico justificado a romper contratos, descubrir incompatibilidades de plugins en Gradle o sufrir la depreciación de métodos en Hibernate. No obstante, cuando trabajas con una arquitectura limpia y una suite de pruebas automatizadas que respalda cada capa, una actualización de esta magnitud se convierte en un ejercicio revelador de salud estructural.

JDK 25 representa un punto de madurez excepcional para el ecosistema backend. Las capacidades de los hilos virtuales (*Virtual Threads*) introducidos con Project Loom operan ahora con una estabilidad y eficiencia asombrosas, eliminando la sobrecarga clásica de memoria por hilo y permitiendo un modelo de concurrencia masiva sin necesidad de adoptar la complejidad sintáctica de las arquitecturas puramente reactivas.

Por su parte, Spring Boot 4.1.1, combinado con Kotlin 2.2.x, potencia la experiencia de desarrollo a niveles que hace unos años parecían lejanos. La inferencia de tipos mejorada, el procesamiento AOT (*Ahead-Of-Time*) refinado para compilación nativa y el soporte integral para *null safety* reducen el código repetitivo a su mínima expresión.

```kotlin
// build.gradle.kts: Declaración moderna de dependencias y toolchain en Kotlin DSL
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.spring)
    alias(libs.plugins.kotlin.jpa)
    alias(libs.plugins.spring.boot)
    alias(libs.plugins.spring.dependency.management)
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(25))
    }
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("org.flywaydb:flyway-core")
    implementation("org.flywaydb:flyway-database-postgresql")

    // Observabilidad y seguimiento de errores
    implementation("io.sentry:sentry-spring-boot-starter-jakarta")

    // Testing moderno sin levantar contextos innecesarios
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("io.mockk:mockk:1.13.12")
    testImplementation("org.testcontainers:postgresql:1.20.1")
}
```

Al habilitar los hilos virtuales en nuestro archivo de configuración `application.yaml`:

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

Tomcat delega automáticamente el despacho de peticiones HTTP a hilos virtuales ligeros en lugar de agotar el pool de hilos de la plataforma del sistema operativo. Esto significa que nuestra API hotelera puede atender picos masivos de peticiones durante las temporadas altas del Gran Hotel Pokémon consumiendo una fracción ínfima de memoria RAM.

---

## Screaming Architecture, Validaciones y la Barrera del 80%

Antes de iniciar una nueva semana de trabajo, quise realizar una auditoría rigurosa del estado actual del repositorio. Con la finalización de la Semana 4, alcanzamos un hito del que me siento profundamente satisfecho: **la base de código mantiene una cobertura de pruebas automatizadas cercana al 80% global**, validada por JaCoCo y reforzada con linters estrictos como Detekt y KtLint.

El diseño de la aplicación adopta **Screaming Architecture por features**, combinada con una separación hexagonal interna en aquellas áreas con reglas de dominio ricas. Cuando cualquier desarrollador clona el proyecto y examina el árbol de directorios, la estructura grita de inmediato qué hace el negocio:

```
src/main/kotlin/com/hotelpokemon/
├── features/
│   ├── ping/             # Healthcheck ligero y pruebas de humo
│   ├── examples/         # Plantilla arquitectónica de referencia
│   ├── hotels/           # Gestión completa de complejos hoteleros
│   ├── rooms/            # Habitaciones temáticas (entidad y repositorio JPA)
│   ├── users/            # Dominio de usuarios, stubs de servicio y puertos
│   └── sentry/           # Endpoints de diagnóstico y rastreo de excepciones
└── shared/
    ├── domain/           # Clases base, Value Objects genéricos y paginación
    ├── infrastructure/   # Configuración de OpenAPI, CORS, HikariCP y excepciones
    └── error/            # DTOs de error estandarizados y GlobalExceptionHandler
```

Cada feature encapsula su modelo de dominio, sus DTOs de transferencia, sus controladores REST y sus adaptadores de persistencia. En lugar de dispersar la lógica de un hotel en diez paquetes genéricos (`controllers`, `services`, `repositories`, `entities`), todo lo relativo a un concepto convive en su propio módulo cohesivo.

El logro más significativo hasta la Semana 4 reside en la disciplina de pruebas estructurada en niveles. Diseñamos una pirámide de verificación donde cada capa se prueba con la herramienta justa para no malgastar recursos de computación:

```
┌──────────────────────────────────────────────────────────────┐
│                 PIRÁMIDE DE PRUEBAS EN 6 NIVELES             │
├───────────────────────────────────┬──────────────────────────┤
│ Nivel de Prueba                   │ Herramientas Clave       │
├───────────────────────────────────┼────────────────────'─────┤
│ 1. Dominio Puro (Unitarias)       │ MockK (Sin Spring, <50ms)│
│ 2. Controladores REST             │ @WebMvcTest + MockMvc    │
│ 3. Adaptadores de Persistencia    │ Unitarias con Mock Repo  │
│ 4. Integración de Componentes     │ @SpringBootTest + H2     │
│ 5. Consultas de Datos             │ @DataJpaTest             │
│ 6. Extremo a Extremo (E2E)        │ Testcontainers Postgres  │
└───────────────────────────────────┴──────────────────────────┘
```

Esta separación garantiza que ejecutar la suite de pruebas unitarias tome menos de dos segundos en cualquier máquina de desarrollo, mientras que los tests pesados de Testcontainers validan con precisión las consultas complejas y las migraciones de Flyway contra una instancia real de PostgreSQL.

> "Un test unitario que tarda tres segundos en ejecutarse es un test que tarde o temprano será comentado o ignorado. La velocidad de la suite de pruebas es la que determina la confianza del desarrollador para refactorizar sin miedo."

A continuación, una muestra de cómo modelamos los Value Objects en el dominio de usuarios empleando Kotlin para garantizar que las reglas de negocio se verifiquen en el momento de la instanciación:

```kotlin
package com.hotelpokemon.features.users.domain.model

import com.hotelpokemon.shared.error.ValidationException

@JvmInline
value class Email(val value: String) {
    init {
        val emailRegex = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}$".toRegex()
        if (!value.matches(emailRegex)) {
            throw ValidationException("El formato del correo electrónico es inválido: '$value'")
        }
    }
}

@JvmInline
value class RawPassword(val value: String) {
    init {
        if (value.length < 8) {
            throw ValidationException("La contraseña debe contener al menos 8 caracteres")
        }
        if (!value.any { it.isUpperCase() } || !value.any { it.isDigit() }) {
            throw ValidationException("La contraseña debe incluir al menos una mayúscula y un número")
        }
    }
}
```

Gracias a los *value classes* (`@JvmInline`), Kotlin no genera objetos adicionales en memoria en tiempo de ejecución para envolver cadenas de texto simples, pero en tiempo de compilación nos proporciona una barrera infranqueable contra errores de asignación accidental de datos.

---

## Semana 5 a la Vista: Resucitando el CRUD de Usuarios y la Muralla de Spring Security

Con la casa en orden y el motor actualizado, ha llegado el momento de retomar el avance narrativo del curso adentrándonos en el templo de la Semana 5: **La Fortaleza de la Seguridad en Ciudad Azafrán**.

En la auditoría descubrí que el feature de `users` se encuentra actualmente incompleto: contamos con un modelo de dominio rico y pruebas unitarias de sus Value Objects, pero `UserController` está vacío, los servicios son meros stubs y todavía no existe una entidad JPA vinculada a la base de datos relacional. Además, las habitaciones (`rooms`) cuentan con entidad y repositorio, pero carecen de servicio y controlador propios.

La Semana 5 aborda directamente esta deuda técnica a través de tres ejercicios fundamentales guiados por el ciclo TDD (Rojo → Verde → Refactor):

### Ejercicio 5.1: Completar el CRUD de Usuarios con Persistencia Real

Transformaremos los stubs actuales en casos de uso plenamente operativos:

- Creación de `UserEntity` mapeando el modelo `User` con campos inmutables y auditoría.
- Implementación de `UserJpaRepository` con Spring Data y `UserRepositoryAdapter` que satisface el puerto de dominio `UserRepository`.
- Lógica de negocio en `CreateUserService`: verificación de correos duplicados y hashing obligatorio de contraseñas mediante BCrypt antes de tocar la base de datos.
- Endpoints REST en `UserController` (`POST`, `GET`, `PUT`, `DELETE`) documentados y con validaciones estrictas.
- Migración Flyway `V3__Add_Users_Table.sql`.

### Ejercicio 5.2: Spring Security con Autenticación JWT Stateless

En la narrativa del curso, el Team Rocket intenta vulnerar los sistemas del hotel con ataques de fuerza bruta y suplantación de identidad. La respuesta es levantar una muralla de seguridad basada en tokens:

- Configuración de `SecurityFilterChain` completamente stateless, deshabilitando sesiones de servidor y CSRF innecesario en APIs REST.
- Creación del feature `auth/` con endpoints públicos para `/api/auth/login` y `/api/auth/register`.
- Implementación de `JwtService` y `JwtAuthenticationFilter` para extraer y validar los claims en cada petición entrante.
- Inyección de `PasswordEncoder` configurado con BCrypt para erradicar cualquier posibilidad de almacenar contraseñas en texto plano.

### Ejercicio 5.3: Roles y Autorizaciones Granulares (RBAC)

No todos los entrenadores tienen los mismos privilegios en el Gran Hotel Pokémon. Un huésped ordinario no debe tener la facultad de modificar tarifas ni cancelar reservaciones ajenas:

- Modelado de entidades `Role` y `Authority` vinculadas mediante relaciones de muchos a muchos (`@ManyToMany`).
- Definición de roles canónicos: `ROLE_GUEST`, `ROLE_STAFF` y `ROLE_ADMIN`.
- Migración Flyway `V4__Add_Roles_Authorities.sql` con roles y permisos preconfigurados.
- Protección declarativa de métodos y endpoints mediante la anotación `@PreAuthorize`.

> "La seguridad en una API no es una capa superficial que se añade el día previo al lanzamiento; es una disciplina de diseño que condiciona la forma en que viajan los datos y se resuelven las identidades en cada capa del sistema."

---

## Del Backlog Central a la Liga de Campeones

Completar el backlog central de diez semanas es solo la primera mitad del viaje. Al revisar los objetivos de largo plazo para este repositorio, quedó claro que un proyecto educativo sobresaliente debe trascender los tutoriales básicos y ofrecer desafíos de nivel industrial.

Por ello, he articulado formalmente dos documentos complementarios en el repositorio:

1. **El Backlog Central (Semanas 0 a 10):** Que cubre el ciclo de vida completo del hotel: desde el CRUD de habitaciones en la Semana 7, el empaquetado con Docker y observabilidad en la Semana 8, hasta las reservaciones con máquinas de estado en la Semana 9 y los pagos y reseñas en la Semana 10.
2. **La Liga de Campeones:** Una colección de **22 ejercicios avanzados de práctica deliberada** organizados en seis fases temáticas posteriores al curso para alcanzar la excelencia técnica.

El roadmap para el curso sigue la idea de avanzar por semana, sin embargo, **no es una carrera contra el calendario**. Soy consciente de que puedo atrasarme y, de hecho, este curso no es mi prioridad absoluta. Es una práctica deliberada, un intento de organizar mi proceso de aprendizaje para que también pueda servirle a otros programadores como base e inspiración.

El objetivo es simple: **mi proceso creativo necesita consolidar el conocimiento**. No me basta con entender algo una vez, necesito trabajarlo, ponerlo a prueba y convertirlo en criterio. Por eso este curso comenzó antes de que la IA se convirtiera en una herramienta tan presente en mi desarrollo.

Hoy es más fácil que nunca pedirle a una IA que complete un curso entero. Pero esa nunca ha sido la intención. **No puedo delegar el proceso de pensamiento ni el criterio de ingeniería.** Puedo delegar parte de la ejecución, pero no la responsabilidad de entender qué estoy construyendo, por qué lo estoy construyendo y si realmente es una buena solución.

Por eso la práctica se vuelve todavía más relevante. No se trata de competir con la IA escribiendo código más rápido, sino de aprender a utilizarla sin perder la capacidad de pensar como ingeniero.

Aquí es donde estoy ahora: **uso la IA para avanzar, pero mantengo el criterio y afianzo el conocimiento**. Las siguientes semanas las trabajaré con diferentes agentes, utilizando el arnés que ya desarrollé, [**CodeConductor**](https://codeconductor.appsutiles.dev/), con la idea de seguir probando y refinando mis prácticas de desarrollo.

El curso es, en cierta forma, otra manera de experimentar con mi propio proceso. No busco demostrar que puedo terminarlo a cualquier costo, sino construir algo que tenga valor, aprender de lo que ocurra y compartirlo para que a otros también les sirva.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    MAPA DE EVOLUCIÓN: GRAN HOTEL POKÉMON                 │
├──────────────────────────────────────────────────────────────────────────┤
│  FASE INICIAL (Completada) ─────── Semanas 0-4: Base, JPA y Cobertura 80%│
│  FORTALEZA ACTUAL (En curso) ───── Semana 5: Users CRUD + JWT Security   │
│  EXPANSIÓN DEL NEGOCIO ─────────── Semanas 6-10: Rooms, Docker, Pagos    │
│                                                                          │
│  ═══════════════════ LIGA DE CAMPEONES (POST-CURSO) ═══════════════════  │
│  Fase 1: Resiliencia ───────────── Resilience4j (Circuit Breaker/Retry)  │
│  Fase 2: Consultas Flexibles ───── Spring for GraphQL & gRPC             │
│  Fase 3: Concurrencia y Loom ───── Virtual Threads vs Coroutines vs R2DBC│
│  Fase 4: Inteligencia Artificial ── Spring AI (RAG, Chatbot con PGVector)│
│  Fase 5: Sistemas Distribuidos ─── Redis L2 Cache & Problem Details      │
│  Fase 6: Compilación Nativa ────── GraalVM Native Image (Sub-200ms cold) │
└──────────────────────────────────────────────────────────────────────────┘
```

Visualizar este horizonte transforma por completo la perspectiva del proyecto. Lo que comenzó como un simple ejercicio de aprendizaje se convierte en un laboratorio exhaustivo de ingeniería backend moderna.

Imaginar a Rotom, nuestro asistente virtual integrado mediante **Spring AI**, consultando disponibilidad en tiempo real gracias a técnicas de RAG sobre bases de datos vectoriales en PostgreSQL, o compilar la aplicación completa a un binario nativo con **GraalVM** que arranque en menos de 150 milisegundos en un contenedor ligero, demuestra la enorme potencia del ecosistema cuando se combina la visión arquitectónica con la perseverancia técnica.

---

## Conclusión

Haber admitido el retraso en el cronograma fue el paso necesario para recuperar el control y la claridad mental. Cuando nos liberamos de la presión arbitraria de los plazos ficticios, recordamos por qué elegimos esta profesión: por el placer artesanal de diseñar sistemas elegantes, por el desafío intelectual de resolver problemas complejos y por la satisfacción de construir software del que podamos sentirnos orgullosos.

El Gran Hotel Pokémon no será una API escrita deprisa para salir del paso en un portafolio personal. Será un testimonio vivo de cómo aplicar Screaming Architecture, TDD riguroso, pruebas de integración reproducibles y tecnologías de vanguardia como Spring Boot 4.1.1 y JDK 25.

¿Ya estás implementando este enfoque en tu entorno de desarrollo? Me encantaría conocer tu experiencia y los desafíos que has enfrentado. ¡Hasta la próxima línea de código! 🚀

Deja tus comentarios en el [repositorio](https://github.com/lgzarturo/arthurolg-blog-posts/issues) o en mi perfil de [X@algforge](https://x.com/algforge). Si te es de utilidad, una estrella en [GitHub](https://github.com/lgzarturo/arthurolg-blog-posts) es de gran ayuda o no dudes en compartir este artículo con tus colegas y amigos. ¡Gracias por leer!

## Referencias

- [Repositorio del Curso: Gran Hotel Pokémon](https://github.com/lgzarturo/springboot-course)
- [Rama de Actualización a Spring Boot 4.1.1 y JDK 25](https://github.com/lgzarturo/springboot-course/tree/feature/milestone-03-update-sb)
- [Documentación Oficial de Spring Boot 4.x](https://docs.spring.io/spring-boot/reference/)
- [Referencia del Lenguaje Kotlin y Coroutines](https://kotlinlang.org/docs/reference/)
- [JEP 444: Hilos Virtuales en la Plataforma Java](https://openjdk.org/jeps/444)
- [Guía de Arquitectura Screaming y Hexagonal Pragmática](https://github.com/lgzarturo/arthurolg-blog-posts)

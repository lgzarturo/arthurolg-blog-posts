---
title: 'Kotlin, Spring Boot 4.1 y Java 25: Corrutinas, Virtual Threads y Conexiones PostgreSQL al Límite'
image: 'https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/kotlin-springboot-4-java-25-concurrencia-postgresql.webp'
description: 'Guía técnica sobre Kotlin en Spring Boot 4.1 con Java 25: corrutinas, virtual threads sin pinning y optimización de pools en PostgreSQL para alto rendimiento.'
author: 'Arturo López'
date: '2026-09-06'
label: 'Spring Boot'
---

## La Ilusión del Millón de Hilos

Ocurrió durante un ensayo de carga previo al lanzamiento de un servicio de scraping masiva. Habíamos configurado la aplicación bajo el entorno de Java JDK 25 y Spring Boot 4.1, activando con entusiasmo la propiedad de hilos virtuales: `spring.threads.virtual.enabled=true`. En las pruebas sintéticas aisladas, la consola mostraba métricas deslumbrantes. Podíamos sostener decenas de miles de peticiones concurrentes por segundo sin que el uso de memoria de la JVM se inmutara ni viéramos el temido agotamiento de hilos del sistema operativo. Parece que habíamos desbloqueado una suerte de truco de recursos ilimitados.

La complacencia duró exactamente cuatro minutos. En cuanto se conecto el flujo de negocio real contra nuestra base de datos PostgreSQL, el panel de monitoreo exploto. Las peticiones comenzaron a acumularse en colas interminables, el tiempo de respuesta saltó de 18 milisegundos a más de 30 segundos, y los logs empezaron a escupir excepciones en cascada: `ConnectionTimeoutException: Connection is not available, request timed out after 30002ms`.

¿Qué había fallado? La máquina virtual de Java estaba ejecutando 40,000 hilos virtuales de manera impecable, pero todos ellos intentaban cruzar simultáneamente por una puerta diminuta: un pool de HikariCP configurado con apenas 20 conexiones hacia una instancia de PostgreSQL que ya consumía el 100% de su CPU resolviendo contención de bloqueos.

> "Multiplicar los hilos en el servidor de aplicaciones sin comprender la capacidad de procesamiento de tu base de datos no crea concurrencia; únicamente traslada el embotellamiento al eslabón más vulnerable de tu infraestructura."

Aquel incidente me recordó una verdad elemental de la ingeniería de software: de nada sirve expandir lo que está bajo tu control inmediato si descuidas las leyes inmutables del entorno circundante. La llegada de Java 25 y la consolidación de Spring Boot 4.1 junto al compilador K2 de Kotlin representan una de las eras más potentes para el ecosistema backend, pero también exigen desterrar mitos. No se trata de elegir a ciegas entre Corrutinas de Kotlin o Hilos Virtuales de Java, sino de dominar cómo interactúan con la persistencia relacional y cómo diseñar endpoints que respondan con agilidad quirúrgica.

---

## Por Qué Actualizar el Stack

Actualizar las versiones mayores de nuestras herramientas principales suele generar fricción en los equipos de desarrollo. Existe una inercia natural a mantener operando lo que ya funciona bajo Java 17 o Java 21 con Spring Boot 3.x. Sin embargo, dar el paso hacia Java 25 y Spring Boot 4.1 en proyectos Kotlin no es un capricho cosmético; es un salto cualitativo en eficiencia de ejecución y ergonomía del lenguaje.

```
┌─────────────────────────────────────────────────────────────┐
│                    EVOLUCIÓN DEL RUNTIME                    │
├──────────────────────────────┬──────────────────────────────┤
│ Java 21 / Spring Boot 3.x    │ Java 25 / Spring Boot 4.1    │
├──────────────────────────────┼──────────────────────────────┤
│ Pinning en synchronized      │ JEP 491: Pinning eliminado   │
│ Compilador Kotlin K1/K2 early│ Kotlin 2.x K2 maduro y veloz │
│ Soporte Loom experimental    │ Virtual Threads integrados   │
│ R2DBC y JDBC desconectados   │ Integración reactiva limpia  │
│ Arranque JVM tradicional     │ CDS y AOT preoptimizados     │
└──────────────────────────────┴──────────────────────────────┘
```

Existen tres razones determinantes para planificar esta actualización en tus servicios:

### 1. El Compilador K2 de Kotlin

Kotlin 2.x no solo compila los proyectos hasta el doble de rápido que la generación previa, sino que su backend de generación de bytecode genera instrucciones alineadas con las optimizaciones de la JVM moderna. Al compilar con destino Java 25, Kotlin aprovecha las mejoras en llamadas dinámicas, registros de tipos y estructuras de datos internas que reducen las asignaciones en el *heap* durante la ejecución de lambdas y funciones de orden superior.

### 2. Spring Boot 4.1 y la Nueva Generación de Configuración Declarativa

La rama 4.1 de Spring Boot refina la introspección de dependencias y adopta por completo la inicialización anticipada (AOT) y Class Data Sharing (CDS) optimizado para contenedores. Los tiempos de arranque en frío se reducen a fracciones de segundo sin sacrificar la flexibilidad del modelo de inyección de dependencias. Además, el framework detecta de forma nativa la presencia de funciones de suspensión (`suspend`) de Kotlin en controladores web, integrándolas sin adaptadores intermediarios engorrosos.

### 3. Rendimiento en Memoria y Gobernanza de Recursos

Java 25 introduce recolección de basura con latencias sub-milisegundas en cargas elevadas (optimizaciones en ZGC generacional) y reduce la huella de memoria por hilo virtual. Esto permite que microservicios compactos desplegados en clústeres de Kubernetes operen con perfiles de memoria mucho más estrechos sin sufrir degradaciones repentinas por pausas de recolección de basura.

---

## Corrutinas vs Virtual Threads en Java 25

Uno de los debates más frecuentes en comunidades de arquitectura es si los Virtual Threads de Java vuelven obsoletas a las Corrutinas de Kotlin, o si las Corrutinas hacen innecesario a Project Loom. Plantear esto como una guerra entre dos tecnologías es un error de diagnóstico. Operan en niveles de abstracción totalmente distintos y resuelven dolencias diferentes.

```
                  ┌───────────────────────────────────────────┐
                  │          PETICIÓN HTTP ENTRANTE           │
                  └─────────────────────┬─────────────────────┘
                                        │
           ┌────────────────────────────┴────────────────────────────┐
           ▼                                                         ▼
┌─────────────────────────────────────┐   ┌─────────────────────────────────────┐
│    VIRTUAL THREADS (JAVA 25)        │   │        CORRUTINAS (KOTLIN)          │
├─────────────────────────────────────┤   ├─────────────────────────────────────┤
│ Nivel: Runtime JVM                  │   │ Nivel: Lenguaje y Compilador        │
│ Paradigma: Imperativo bloqueante    │   │ Paradigma: Concurrencia estructurada│
│ Mecanismo: Park / Unpark en carrier │   │ Mecanismo: Máquina de estados       │
│ Ideal: I/O síncrono tradicional     │   │ Ideal: Flujos, cancelación y racing │
└─────────────────────────────────────┘   └─────────────────────────────────────┘
```

### ¿Qué es exactamente un Virtual Thread en Java 25?

Un hilo virtual es una instancia de `java.lang.Thread` que no está atada de forma fija a un hilo del sistema operativo. Cuando el hilo virtual ejecuta una operación de I/O bloqueante (como esperar la respuesta de un socket de red o una consulta SQL mediante JDBC), la máquina virtual suspende el hilo virtual y libera el hilo portador subyacente (*carrier thread*, que es un hilo real del sistema operativo) para que atienda a otros hilos virtuales.

En versiones previas (Java 21), los hilos virtuales sufrían de un grave inconveniente: el **thread pinning**. Si una operación bloqueante ocurría dentro de un bloque o método marcado con `synchronized`, o llamaba a código nativo en C, el hilo virtual quedaba "anclado" al hilo portador. El hilo de la plataforma no podía liberarse, destruyendo la escalabilidad prometida.

**Aquí reside la gran revolución de Java 25:** con la aprobación e implementación de **JEP 491 (Synchronize Virtual Threads without Pinning)**, los monitores de objetos en bloques `synchronized` ya no fijan el hilo portador. La JVM ahora puede suspender y reanudar hilos virtuales con total libertad incluso dentro de bibliotecas legadas y controladores JDBC que todavía dependen intensamente de sincronización clásica.

### ¿Qué son las Corrutinas de Kotlin?

Las corrutinas no son hilos; son cálculos suspendibles gestionados por el compilador mediante una máquina de estados. Cuando invocas una función `suspend`, el hilo actual no se detiene; la función guarda su contexto de ejecución y cede el control cooperativamente.

Las corrutinas destacan por encima del modelo imperativo de hilos virtuales cuando necesitas:

- **Concurrencia estructurada:** Si una tarea padre falla, todas las subtareas hijas se cancelan automáticamente en cascada sin dejar procesos zombis consumiendo CPU.
- **Manejo de reactividad declarativa con `Flow`:** Transformación de secuencias asíncronas con operadores funcionales como `map`, `filter`, `debounce` y `buffer`.
- **Control milimétrico de cancelaciones y tiempos de espera:** Interrumpir operaciones concurrentes de forma cooperativa sin depender de interrupciones forzadas de hilos que puedan corromper estados en memoria.

> "Los Virtual Threads otorgan ligereza a tu viejo código imperativo bloqueante; las Corrutinas te otorgan un vocabulario superior para componer y orquestar flujos asíncronos complejos."

Ambas tecnologías no se anulan: se complementan. En Spring Boot 4.1 con Java 25 puedes despachar corrutinas de Kotlin sobre ejecutores respaldados por Virtual Threads, obteniendo lo mejor de dos mundos: la elegancia sintáctica de Kotlin junto a la absorción transparente de I/O de la JVM moderna.

---

## El Cuello de Botella Físico: Hilos Masivos frente al Pool de PostgreSQL

Regresemos a la lección que nos dejó el incidente de carga inicial. Imaginemos un servidor web que recibe 5,000 peticiones por segundo. Con hilos virtuales habilitados, Spring MVC crea gustosamente 5,000 hilos concurrentes para procesarlas. Cada hilo llega al repositorio de persistencia e intenta obtener una conexión JDBC hacia PostgreSQL.

PostgreSQL utiliza un modelo de arquitectura de procesos: por cada conexión TCP abierta, el servidor de base de datos genera un proceso dedicado del sistema operativo (`postgres: client process`). Estos procesos compiten ferozmente por memoria compartida (*shared buffers*), candados en tablas e índices (*locks* y *latches*), y tiempo de procesamiento en las CPUs del motor de base de datos.

```
                 TRÁFICO CONCURRENTE
            [ 10,000 Peticiones HTTP ]
                        │
                        ▼
      ┌────────────────────────────────────┐
      │  JVM / Spring Boot 4.1             │
      │  (10,000 Virtual Threads activos)  │
      └─────────────────┬──────────────────┘
                        │
                        ▼
            ╔════════════════════════╗
            ║    HIKARICP POOL       ║
            ║  (25 Conexiones Máx.)  ║
            ╚═══════════╦════════════╝
                        │  ◄── ¡CUELLO DE BOTELLA!
                        │      9,975 hilos esperando conexión
                        ▼
      ┌────────────────────────────────────┐
      │     POSTGRESQL INSTANCE            │
      │     (Límites físicos de CPU y I/O) │
      └────────────────────────────────────┘
```

Si intentas solucionar este problema aumentando el tamaño del pool de conexiones de HikariCP a 5,000 para emparejarlo con tus hilos virtuales, provocarás el colapso absoluto de PostgreSQL. El procesador del servidor de base de datos pasará casi todo su tiempo alternando el contexto entre miles de procesos en lugar de ejecutar consultas SQL útiles.

### La Ecuación Óptima del Pool de Conexiones

Como documentó hace años el equipo de desarrollo de HikariCP, el cálculo del número máximo de conexiones efectivas para una base de datos con discos SSD rápidos responde a una fórmula sorprendentemente compacta:

$$\text{Conexiones Máximas} = (\text{Núcleos de CPU de la BD} \times 2) + \text{Efecto de Concurrencia de Disco}$$

Para una instancia de PostgreSQL con 8 núcleos dedicados de CPU y almacenamiento NVMe moderno, un pool de entre **16 y 25 conexiones** suele entregar un rendimiento total (*throughput*) mucho mayor y una latencia media más baja que un pool sobredimensionado de 200 conexiones.

¿Cómo atendemos entonces 10,000 peticiones concurrentes con solo 25 conexiones físicas hacia PostgreSQL? Aquí es donde se bifurcan nuestras estrategias arquitectónicas:

1. **Estrategia A (Imperativa Optimizada):** Spring MVC + Virtual Threads + HikariCP estrictamente dimensionado + PgBouncer en la capa de persistencia.
2. **Estrategia B (Reactiva No Bloqueante):** Spring WebFlux + Corrutinas de Kotlin + R2DBC (`r2dbc-postgresql`), donde las consultas no retienen conexiones ociosas durante los tiempos muertos de red o procesamiento en la aplicación.

---

## Optimizando Endpoints en la Práctica

Veamos cómo estructurar ambos enfoques en un proyecto real con Spring Boot 4.1 y Kotlin, analizando el impacto de cada decisión.

### Enfoque 1: Spring MVC con Virtual Threads y Acceso JDBC Tradicional

Si tu equipo cuenta con una base de código basada en Spring Data JPA o JDBC tradicional y no desea la complejidad de un modelo reactivo, Java 25 te permite escalar horizontalmente de manera transparente.

Primero, habilitamos los hilos virtuales y ajustamos el pool de HikariCP en nuestro archivo `application.yml`:

```yaml
spring:
  threads:
    virtual:
      enabled: true
  datasource:
    url: jdbc:postgresql://localhost:5432/orders_db
    username: postgres_user
    password: secret_password
    hikari:
      maximum-pool-size: 25
      minimum-idle: 10
      connection-timeout: 5000
      idle-timeout: 300000
      max-lifetime: 1800000
      leak-detection-threshold: 2000
```

En la capa de servicio y controlador, el código se mantiene limpio, secuencial y directo. Gracias a la eliminación del anclaje de hilos en Java 25, cualquier bloqueo dentro del driver JDBC suspende el hilo virtual sin congelar el hilo del sistema operativo:

```kotlin
package com.arturo.orders.infrastructure.web

import com.arturo.orders.domain.dto.OrderSummaryDto
import com.arturo.orders.domain.service.OrderQueryService
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/api/v1/orders")
class OrderController(
    private val orderQueryService: OrderQueryService
) {

    @GetMapping
    fun listRecentOrders(
        @RequestParam(defaultValue = "0") lastSeenId: Long,
        @RequestParam(defaultValue = "50") limit: Int
    ): ResponseEntity<List<OrderSummaryDto>> {
        // Ejecución síncrona en un hilo virtual ligero de Java 25
        val orders = orderQueryService.findRecentOrders(lastSeenId, limit.coerceAtMost(100))
        return ResponseEntity.ok(orders)
    }
}
```

Para maximizar la velocidad de respuesta, aplicamos dos técnicas esenciales en la consulta SQL dentro de nuestro repositorio:

- **Paginación Keyset (Seek Method):** Evitamos a toda costa `OFFSET` y `LIMIT`, ya que obligan a PostgreSQL a escanear y descartar miles de tuplas en páginas profundas.
- **Proyecciones DTO Directas:** Consultamos únicamente las columnas estrictamente necesarias en lugar de cargar entidades pesadas de Hibernate con relaciones perezosas.

```kotlin
package com.arturo.orders.infrastructure.persistence

import com.arturo.orders.domain.dto.OrderSummaryDto
import org.springframework.jdbc.core.simple.JdbcClient
import org.springframework.stereotype.Repository

@Repository
class OrderJdbcRepository(private val jdbcClient: JdbcClient) {

    fun findRecentOrders(lastSeenId: Long, limit: Int): List<OrderSummaryDto> {
        val sql = """
            SELECT id, customer_uuid, total_amount, status, created_at
            FROM customer_orders
            WHERE id > :lastSeenId
            ORDER BY id ASC
            LIMIT :limit
        """.trimIndent()

        return jdbcClient.sql(sql)
            .param("lastSeenId", lastSeenId)
            .param("limit", limit)
            .query { rs, _ ->
                OrderSummaryDto(
                    id = rs.getLong("id"),
                    customerUuid = rs.getString("customer_uuid"),
                    totalAmount = rs.getBigDecimal("total_amount"),
                    status = rs.getString("status"),
                    createdAt = rs.getTimestamp("created_at").toInstant()
                )
            }
            .list()
    }
}
```

### Enfoque 2: Spring WebFlux con Corrutinas de Kotlin y R2DBC

Cuando el servicio debe manejar transmisión continua de datos (*streaming*), notificaciones en tiempo real o volúmenes masivos de lectura sin saturar conexiones persistentes, la combinación de WebFlux, Corrutinas y R2DBC se convierte en un arma letal.

Configuramos la conexión no bloqueante en `application.yml`:

```yaml
spring:
  r2dbc:
    url: r2dbc:postgresql://localhost:5432/orders_db
    username: postgres_user
    password: secret_password
    pool:
      initial-size: 10
      max-size: 30
      max-idle-time: 30m
```

En este modelo, el controlador utiliza la palabra clave `suspend` y flujos asíncronos mediante `Flow`:

```kotlin
package com.arturo.orders.reactive.web

import com.arturo.orders.domain.dto.OrderSummaryDto
import com.arturo.orders.reactive.repository.OrderR2dbcRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import org.springframework.http.MediaType
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/api/v2/orders")
class ReactiveOrderController(
    private val orderRepository: OrderR2dbcRepository
) {

    @GetMapping(produces = [MediaType.APPLICATION_NDJSON_VALUE])
    fun streamOrders(
        @RequestParam customerUuid: String
    ): Flow<OrderSummaryDto> {
        // Retorna un flujo reactivo asíncrono sin bloquear ningún hilo ni conexión
        return orderRepository.findAllByCustomerUuid(customerUuid)
            .map { entity ->
                OrderSummaryDto(
                    id = entity.id,
                    customerUuid = entity.customerUuid,
                    totalAmount = entity.totalAmount,
                    status = entity.status,
                    createdAt = entity.createdAt
                )
            }
    }
}
```

```kotlin
package com.arturo.orders.reactive.repository

import kotlinx.coroutines.flow.Flow
import org.springframework.data.r2dbc.repository.Query
import org.springframework.data.repository.kotlin.CoroutineCrudRepository
import org.springframework.stereotype.Repository

@Repository
interface OrderR2dbcRepository : CoroutineCrudRepository<OrderEntity, Long> {

    @Query("SELECT * FROM customer_orders WHERE customer_uuid = :customerUuid ORDER BY id DESC")
    fun findAllByCustomerUuid(customerUuid: String): Flow<OrderEntity>
}
```

Con R2DBC, una única conexión física de red puede multiplexar solicitudes de lectura de manera no bloqueante. La memoria requerida por la aplicación es mínima y la base de datos no sufre la sobrecarga de miles de procesos bloqueados en contención de hilos.

---

## Matriz de Decisión Arquitectónica y Trade-offs

Ninguna arquitectura es perfecta en todos los escenarios. Adoptar ciegamente la última novedad técnica sin sopesar sus compromisos operativos suele terminar en desastre. En mi labor como líder técnico, aplico una regla de discernimiento pragmático para definir cuándo implementar cada solución:

| Criterio de Evaluación         | Spring MVC + Virtual Threads (Java 25)              | Spring WebFlux + Corrutinas + R2DBC                        |
| :----------------------------- | :-------------------------------------------------- | :--------------------------------------------------------- |
| **Curva de Aprendizaje**       | Mínima. Código imperativo secuencial habitual.      | Moderada. Requiere comprender reactividad y `Flow`.        |
| **Ecosistema y Librerías**     | Universal. Compatible con Hibernate, JPA y JDBC.    | Específico. Limitado a librerías con soporte reactivo.     |
| **Transaccionalidad Compleja** | Madura y robusta mediante `@Transactional`.         | Más compleja con `TransactionalOperator` reactivo.         |
| **Throughput con I/O Simple**  | Excepcional tras JEP 491 (sin *pinning*).           | Máximo rendimiento con menor huella de memoria.            |
| **Streaming y SSE**            | Posible pero demanda más recursos por cliente.      | Nativo, fluido y de costo casi nulo en recursos.           |
| **Presión sobre PostgreSQL**   | Requiere límites estrictos en HikariCP / PgBouncer. | Absorción natural mediante contrapresión (*backpressure*). |

```
                     ¿CÓMO DECIDIR TU ARQUITECTURA?
                                   │
                   ¿Tu sistema depende de JPA/Hibernate
                 o de un ecosistema amplio de librerías?
                                   │
                    ┌──────────────┴──────────────┐
                   SÍ                             NO
                    │                             │
                    ▼                             ▼
       ¿Tu carga principal es CRUD     ¿Requieres streaming masivo,
      empresarial con transacciones      SSE, microservicios ultra
          relacionales densas?          ligeros o alta concurrencia?
                    │                             │
                    ▼                             ▼
        [ SPRING MVC + KOTLIN         [ SPRING WEBFLUX + KOTLIN
         + VIRTUAL THREADS 25 ]            + CORRUTINAS + R2DBC ]
```

### Lecciones de Trinchera para Optimizar PostgreSQL

Independientemente de cuál modelo elijas para tu capa de aplicación, la base de datos siempre impondrá las fronteras físicas de tu sistema. Toma en cuenta estas tres recomendaciones prácticas:

1. **Introduce PgBouncer frente a PostgreSQL:** Si decides utilizar Spring MVC con Virtual Threads bajo picos agresivos de tráfico, sitúa un concentrador de conexiones como PgBouncer en modo de agrupamiento por transacción (*transaction pooling*). Esto permite que miles de hilos de la aplicación compartan un grupo reducido de conexiones físicas reales con el motor.
2. **Monitorea activamente la contención de cerraduras:** En PostgreSQL, ejecuta periódicamente consultas sobre `pg_stat_activity` filtrando por `wait_event_type = 'Lock'`. Un aumento súbito en este indicador delata que los hilos concurrentes están chocando por actualizar los mismos registros en la base de datos.
3. **Evita la trampa del mapeo bidireccional indiscriminado:** En endpoints de alta concurrencia, prescinde de grafos de entidades profundos con colecciones marcadas en `FetchType.EAGER`. La serialización de objetos innecesarios genera recolección de basura destructiva y consultas SQL ocultas que multiplican la latencia de red.

---

## Conclusión

La ingeniería de software madura no consiste en perseguir la herramienta más reluciente del momento, sino en entender con serenidad los límites de cada componente de nuestro sistema. Java 25 y Spring Boot 4.1 han alcanzado un grado de madurez extraordinario.

Al mismo tiempo, las Corrutinas de Kotlin continúan siendo la abstracción más limpia y expresiva para gobernar flujos de datos complejos, orquestaciones asíncronas y cancelaciones en cascada. Ninguno de estos avances mágicamente ensancha el canal de procesamiento de un disco duro o multiplica los núcleos de un servidor de base de datos. El verdadero arte reside en equilibrar la ligereza de la máquina virtual con el respeto riguroso hacia el pool de conexiones de PostgreSQL. Cuando alineas ambos mundos con disciplina y sencillez, el sistema responde con una solidez inquebrantable ante cualquier tormenta de tráfico.

¿Ya estás implementando este enfoque en tu entorno de desarrollo? Me encantaría conocer tu experiencia y los desafíos que has enfrentado. ¡Hasta la próxima línea de código! 🚀

Deja tus comentarios en el [repositorio](https://github.com/lgzarturo/arthurolg-blog-posts/issues) o en mi perfil de [X@algforge](https://x.com/algforge). Si te es de utilidad, una estrella en [GitHub](https://github.com/lgzarturo/arthurolg-blog-posts) es de gran ayuda o no dudes en compartir este artículo con tus colegas y amigos. ¡Gracias por leer!

## Referencias

- [Documentación Oficial de Spring Boot 4.x](https://docs.spring.io/spring-boot/)
- [JEP 491: Synchronize Virtual Threads without Pinning](https://openjdk.org/jeps/491)
- [Guía de Concurrencia Estructurada y Corrutinas en Kotlin](https://kotlinlang.org/docs/coroutines-overview.html)
- [HikariCP: About Pool Sizing and Performance](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)
- [R2DBC PostgreSQL Driver Documentation](https://r2dbc.io/spec/1.0.0.RELEASE/spec/html/)

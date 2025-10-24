---
title: Guía práctica de calidad de código para Spring Boot con Kotlin
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/software-programmer-with-kotlin-springboot-and-best-practices.webp
description: Por qué KtLint, Detekt, JaCoCo, Codecov y GitHub Actions son cruciales en proyectos Spring Boot con Kotlin. Pasos claros, beneficios y buenas prácticas para equipos.
author: Arturo López
date: 2025-10-24
label: SpringBoot
---

## Configuración práctica

Tienes un proyecto Spring Boot con Kotlin y quieres buena higiene de código, cobertura y releases automáticos. Eso implica alinear versiones, configurar herramientas estáticas y poner CI que ejecute checks y publique artefactos. Lo más común que rompe todo es la incompatibilidad de versiones entre Kotlin y herramientas como Detekt o plugins. Aprende a evitar eso primero.

En proyectos Spring Boot con Kotlin la coherencia del stack no es opcional, es supervivencia. Si las versiones de Kotlin, plugins y herramientas no están alineadas, te pasas días persiguiendo errores crípticos en CI en vez de entregar funciones (*[me ha pasado en el curso de spring boot, al intentar aplicar buenas prácticas](https://lgzarturo.com/springboot-course?utm_source=direct&utm_medium=blog&utm_campaign=article)*). Herramientas como Detekt y KtLint no son un lujo estético, son la primera línea de defensa contra deuda técnica trivial: detectan malos patrones, inconsistencias y problemas que luego se vuelven costosos cuando el código crece. Mantener estas herramientas bien configuradas y con versiones fijadas evita interrupciones en el flujo del equipo y reduce el tiempo perdido en "arreglar el entorno".

Las ventajas prácticas son claras y directas. KtLint impone un estilo único, lo que hace que las diffs sean legibles y las revisiones más rápidas. Detekt encuentra problemas estáticos que no saltan en compilación, como patrones de rendimiento o code smells recurrentes. JaCoCo y Codecov te dan visibilidad sobre qué código está cubierto por pruebas, no para inflar métricas sino para priorizar lo que realmente importa. GitHub Actions automatiza todo esto en cada push y cada PR, lo que mantiene la calidad sin depender de la memoria o la buena voluntad de los desarrolladores. Y cuando automatizas releases con semantic-release, reduces errores humanos al publicar artefactos y generar changelogs (*esto último me ha costado mucho tiempo para configurarlo correctamente*).

Desde la trinchera del equipo y del líder técnico, estas prácticas aceleran el onboarding, mejoran la disciplina en las revisiones y hacen más predecible el mantenimiento. Lo práctico: fija versiones de Kotlin y plugins, documenta la política en el repo, obliga a correr checks locales antes de abrir PR y deja claras las excepciones con supresiones puntuales y comentarios justificando la decisión. Es molesto al inicio, sí, pero crea un entorno donde el trabajo real se puede hacer sin pelear con herramientas. Para un junior o un nuevo líder, adoptar esto temprano es la diferencia entre empujar parches y construir software que puedas sostener.

---

### 1. Compatibilidad Kotlin versus Detekt: problema y soluciones

#### Qué pasa y por qué importa

Detekt usa artefactos Kotlin internamente. Si Detekt fue compilado con una versión de Kotlin diferente a la que tú usas, el runtime se rompe con errores tipo:

```plaintext
detekt was compiled with Kotlin X but is currently running with Y
```

Eso rompe CI y el workflow de calidad. Es una incompatibilidad binaria, no algo que se arregle con config.

#### Opciones prácticas

1. Bajar Kotlin a la versión con la que Detekt es compatible.
2. Subir Kotlin a la versión con la que Detekt fue compilado.

#### Recomendaciones concretas

* Si quieres estabilidad rápida: baja Kotlin a 1.9.21 y usa Detekt 1.23.4.
* Si quieres modernizar y tu stack lo permite: sube a Kotlin 2.0.21 y usa Detekt 1.23.8 o 1.23.9.
  Esto te deja a futuro con menos fricciones, pero valida todas tus dependencias.

#### Ejemplo en `build.gradle.kts` para Kotlin 2.0.21 y Detekt 1.23.9

```kotlin
plugins {
    kotlin("jvm") version "2.0.21"
    kotlin("plugin.spring") version "2.0.21"
    kotlin("plugin.jpa") version "2.0.21"
    id("org.springframework.boot") version "3.5.6"
    id("io.spring.dependency-management") version "1.1.7"
    id("io.gitlab.arturbosch.detekt") version "1.23.9"
}

repositories { mavenCentral() }

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    detektPlugins("io.gitlab.arturbosch.detekt:detekt-formatting:1.23.9")
}

detekt {
    config.setFrom(files("$rootDir/config/detekt/detekt.yml"))
    buildUponDefaultConfig = true
}
```

---

### 2. Error "Property 'formatting' is misspelled or does not exist" y cómo resolverlo

#### Por qué ocurre

Detekt movió las reglas de formateo a un plugin separado llamado `detekt-formatting`. Antes se ponía un bloque `formatting:` dentro de `detekt.yml`. Hoy eso no funciona.

#### Solución rápida

* **Eliminar** el bloque `formatting:` del `detekt.yml`.
* **Agregar** la dependencia plugin en Gradle:

```kotlin
detektPlugins("io.gitlab.arturbosch.detekt:detekt-formatting:1.23.9")
```

#### Buen tip

Después de cambiar la config, genera un config base limpito para ver cómo queda:

```bash
./gradlew detektGenerateConfig
```

---

### 3. Cómo desactivar solo la regla SpreadOperator en `detekt.yml`

#### Por qué podrías quererlo

La regla `performance.SpreadOperator` alerta por el operador `*array` que copia arrays. En muchos casos reales el impacto es mínimo y la regla ruidosa. Si tu equipo la considera ruido, desactívala.

#### Cómo hacerlo (en `config/detekt/detekt.yml`)

```yaml
performance:
  active: true
  SpreadOperator:
    active: false
```

#### Alternativa más conservadora

Suprime la advertencia en el código solo donde sea necesario:

```kotlin
@Suppress("SpreadOperator")
fun example(vararg args: String) {
    other(*args)
}
```

---

### 4. KtLint y la obsolescencia de `disabled_rules` en `.editorconfig`

#### Contexto

En versiones modernas de KtLint la propiedad `disabled_rules` quedó obsoleta y fue removida. Si la usas aparece el mensaje:

```plaintext
Editorconfig property 'disabled_rules' is obsolete and is not used by KtLint starting from version 0.49
```

#### Forma correcta de deshabilitar reglas ahora

Usar la nomenclatura `ktlint_<ruleSet>_<ruleId> = disabled` o `ktlint_<ruleSet> = disabled`.

Para el caso concreto de `no-space-in-parentheses`:

```ini
[*.{kt,kts}]
ktlint_standard_no-space-in-parentheses = disabled
```

#### Opciones de alcance

* Global: `.editorconfig` raíz con la línea anterior.
* Archivo o línea: usar comentarios en el código

  * Desactivar en una línea:

    ```kotlin
    fun ejemplo( x: Int, y: Int ) = x + y // ktlint-disable-line no-space-in-parentheses
    ```
  * Desactivar en todo el archivo:

    ```kotlin
    // ktlint-disable no-space-in-parentheses
    ```

#### Tip práctico

Prefiere `.editorconfig` para reglas de estilo del equipo. Usa supresiones en código solo cuando haya una razón técnica.

---

### 5. Comandos útiles para ejecutar localmente y depurar

```bash
./gradlew clean assemble test
./gradlew ktlintCheck
./gradlew detekt
./gradlew jacocoTestReport
```

Si un task falla, ejecuta con `--info` o `--stacktrace` para obtener más contexto.

---

### 6. JaCoCo y Codecov, para cobertura

#### Por qué es importante

Cobertura no es la verdad absoluta, pero te da visibilidad de qué código está siendo testeado. En equipo, ayuda a no romper contratos y detectar regresiones.

#### Configuración mínima en `build.gradle.kts`

```kotlin
jacoco {
    toolVersion = "0.8.12"
}

tasks.test {
    useJUnitPlatform()
    finalizedBy(tasks.jacocoTestReport)
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required.set(true)
        html.required.set(true)
    }
}
```

#### Subir a Codecov desde CI

En GitHub Actions usar:

```yaml
- name: Generate Coverage Report
  run: ./gradlew jacocoTestReport

- name: Upload Coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    files: build/reports/jacoco/test/jacocoTestReport.xml
    token: ${{ secrets.CODECOV_TOKEN }}
```

Tip: proteger el token con `secrets` y marcar que falle si la subida no se puede hacer.

---

### 7. GitHub Actions: build.yml y release.yml, lo esencial

#### build.yml, jobs que deberías tener

* checkout
* setup JDK
* setup Gradle
* build assemble test
* ktlintCheck
* detekt
* jacocoTestReport
* upload coverage a Codecov

Ejemplo mínimo:

```yaml
name: Build and Test
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: 21 }
      - uses: gradle/gradle-build-action@v3
      - run: ./gradlew clean assemble test
      - run: ./gradlew ktlintCheck
      - run: ./gradlew detekt
      - run: ./gradlew jacocoTestReport
      - uses: codecov/codecov-action@v4
        with:
          files: build/reports/jacoco/test/jacocoTestReport.xml
          token: ${{ secrets.CODECOV_TOKEN }}
```

#### release.yml, cuando creas tags v*

* checkout
* build jar
* upload artifacts
* ejecutar semantic-release para versionado semántico y CHANGELOG.md

Fragmento clave:

```yaml
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: 21 }
      - run: ./gradlew clean build
      - uses: actions/upload-artifact@v4
        with: { name: app-jar, path: build/libs/*.jar }
      - name: Semantic Release
        uses: cycjimmy/semantic-release-action@v4
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Y `.releaserc.json` con plugins `@semantic-release/changelog` y `@semantic-release/github` para adjuntar el JAR en el release y generar `CHANGELOG.md`.

---

### 8. Buenas prácticas y por qué son cruciales para el equipo

1. **Alinear versiones**: evita horas de debugging por incompatibilidades. Si subes Kotlin, revisa Detekt, KtLint y plugins nativos.
2. **Reglas en `.editorconfig`**: hace que el estilo sea reproducible por todos, incluyendo IDE y CI.
3. **No silenciar reglas sin criterio**: si apagas una regla, documenta por qué. Las supresiones en código deben ir acompañadas de comentario en el commit o en la PR.
4. **CI que falle rápido**: es mejor fallar temprano en la pipeline que llegar a release con tech debt.
5. **Reglas locales vs globales**: usa `ktlint` y `detekt` en CI, pero permite supresiones locales para casos justificados.
6. **Version pinning**: fija versiones de plugins en Gradle para evitar sorpresas. Actualiza de forma planificada.
7. **Logs y trazas**: cuando algo falla, corre con `--stacktrace` y compártelos en la PR para quien revise. Facilita la colaboración.
8. **Documenta decisiones**: en el README del repo deja la política de versiones y cómo ejecutar checks localmente.

---

### 9. Tips rápidos y prácticos (de los que evitan reuniones innecesarias)

* Antes de abrir una PR, corre `./gradlew ktlintCheck detekt test jacocoTestReport` en tu máquina. **No es opcional**.
* Mantén un archivo `MAINTAINERS.md` con la versión de Kotlin aprobada y pasos para actualizar dependencias principales.
* Cuando cambies Kotlin mayor, haz una PR con solo el upgrade y la corrección de incompatibilidades. Esa PR es más fácil de revisar que mezclar cambios funcionales.
* Si usas IntelliJ, instala los plugins de KtLint y Detekt para feedback inmediato.
* No confundas cobertura alta con calidad. **Prioriza tests que verifiquen comportamiento crítico**.

---

### 10. Resumen de acciones a ejecutar ahora mismo

1. Decide ruta: bajar Kotlin a 1.9.21 o subir a 2.0.21.
2. Ajusta `build.gradle.kts` con versiones coherentes y añade `detekt-formatting` como `detektPlugins`.
3. Limpia `detekt.yml` de la sección `formatting:` y desactiva `SpreadOperator` si lo deseas.
4. Actualiza `.editorconfig` usando `ktlint_standard_no-space-in-parentheses = disabled` si usas KtLint 0.49+.
5. Ejecuta local:

   ```bash
   ./gradlew clean detekt ktlintCheck test jacocoTestReport
   ```

6. Asegura CI: actualiza `build.yml` y `release.yml` con los pasos vistos.

### Conclusión

Adoptar estas buenas prácticas en proyectos Spring Boot con Kotlin no es solo una cuestión técnica, es una inversión en la salud a largo plazo del código y la productividad del equipo. La coherencia en versiones, la automatización de checks y la disciplina en el estilo de código crean un entorno donde los desarrolladores pueden enfocarse en lo que realmente importa: construir software de calidad que resuelva problemas reales.

No subestimes el poder de una buena configuración desde el inicio. Evita la deuda técnica trivial que consume tiempo y energía. Con estas prácticas, tu equipo podrá moverse más rápido, con menos fricciones y mayor confianza en cada release.

Adopta estas recomendaciones hoy mismo y observa cómo la calidad y la eficiencia de tu equipo mejoran significativamente. 

¡Happy Coding!
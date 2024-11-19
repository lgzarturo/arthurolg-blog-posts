---
title: Anotaciones Personalizadas en Spring Boot - Potencia tu Aplicación y Optimiza tu Código
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/potencia-tu-aplicacion-con-las-anotaciones.webp
description: Entiende cómo las anotaciones personalizadas pueden transformar tu desarrollo en Spring Boot. Aprende a crear y aplicar anotaciones para simplificar la configuración, mejorar la seguridad y optimizar el rendimiento de tu aplicación. Esta guía práctica te enseña desde cero cómo aprovechar todo el poder de las anotaciones en proyectos Java.
author: Arturo López
date: 2024-11-08
label: Guía
---

### ¿Por qué el equipo de Spring utiliza anotaciones?

En general uso de anotaciones en el desarrollo de aplicaciones con Java y, en particular, en Spring Boot, es una herramienta poderosa que permite simplificar y estructurar el código de manera eficiente. Las anotaciones, en términos simples, son etiquetas que podemos agregar al código para dar instrucciones a la aplicación sobre cómo debe comportarse o cómo debe configurarse sin necesidad de escribir tanto código adicional. En lugar de tener que hacer configuraciones manuales o escribir código repetitivo, las anotaciones ayudan a que Spring se encargue de esos detalles por nosotros.

Spring es un framework diseñado para hacer el desarrollo en Java más eficiente y manejable. Una de las filosofías de Spring es la **Inversión de Control (IoC)**, es decir, que el propio framework maneje la creación y gestión de objetos y configuraciones. Para que esto sea posible sin cargar al desarrollador con configuraciones detalladas y repetitivas, Spring recurre a las anotaciones. Las anotaciones facilitan al framework saber qué clase debe actuar como controlador, cuál se conecta a la base de datos o cómo deben comportarse los servicios de manera automática.

Además, las anotaciones permiten que el código sea más **declarativo** y **autodocumentado**. Esto significa que podemos ver de un vistazo qué está haciendo una clase o un método, sin tener que profundizar en su lógica. Es como poner etiquetas a cada pieza de código para que sea fácilmente entendible y flexible.

### Importancia de las anotaciones en el desarrollo de aplicaciones

El desarrollo de aplicaciones modernas requiere velocidad, flexibilidad y claridad. Las anotaciones en Spring logran estos objetivos:

1. **Reducción del Código Complejo**: Anteriormente, los desarrolladores debían escribir configuraciones largas y detalladas en archivos XML para definir cómo funcionaría cada componente. Con anotaciones, la mayor parte de esta configuración es automática, lo que reduce el tiempo y el esfuerzo necesario para iniciar un proyecto.

2. **Modularidad y Flexibilidad**: Las anotaciones hacen que el código sea más modular. Puedes cambiar el comportamiento de una aplicación simplemente aplicando o eliminando anotaciones, sin necesidad de modificar toda la estructura. Esto hace que sea más fácil agregar nuevas funcionalidades o ajustar el comportamiento sin romper el código existente.

3. **Código Más Limpio y Legible**: Con las anotaciones, el código se vuelve más fácil de leer. Puedes ver las funcionalidades principales de un componente al observar sus anotaciones, lo que también hace que el código sea más mantenible y menos propenso a errores.

4. **Escalabilidad**: A medida que el proyecto crece, la gestión de cada componente puede ser compleja. Las anotaciones permiten que Spring gestione y configure automáticamente las interacciones entre componentes, lo que ayuda a mantener el orden y escalabilidad en proyectos de gran tamaño.

### ¿Por qué muchos usan las anotaciones sin conocer su potencial?

Es común que los desarrolladores adopten las anotaciones de Spring porque son recomendadas en la mayoría de los tutoriales y documentación, pero pocos exploran su verdadero poder y flexibilidad. Muchos desarrolladores se limitan a usarlas sin profundizar en cómo funcionan o en cómo crear anotaciones personalizadas. El desconocimiento de su potencial puede llevar a una **subutilización** de esta herramienta, perdiendo la oportunidad de hacer el código aún más eficiente y ajustado a las necesidades específicas del proyecto.

### Recomendaciones para aprovechar al máximo las anotaciones en Spring

1. **Entender su Función y Contexto**: Antes de usar una anotación, es útil entender qué hace y por qué se utiliza. No todas las anotaciones son necesarias en todos los casos. Conocer las básicas (como `@Component`, `@Service`, `@Controller`) y comprender cuándo y cómo usarlas te permitirá organizar mejor tu código.

2. **Aprender a Crear Anotaciones Personalizadas**: Spring permite la creación de anotaciones personalizadas, lo cual es muy útil cuando necesitas una funcionalidad que no está cubierta por las anotaciones existentes. Las anotaciones personalizadas son ideales para agrupar funcionalidades repetitivas y estandarizar comportamientos en todo el proyecto, reduciendo errores y mejorando la mantenibilidad.

3. **No Abusar de las Anotaciones**: Aunque las anotaciones son muy poderosas, es importante no abusar de ellas. Incluir anotaciones innecesarias puede sobrecargar el código y hacerlo más difícil de entender. Utiliza solo las que realmente añaden valor y simplifican el código.

4. **Documentar y Experimentar**: Dado que las anotaciones pueden parecer "mágicas" a veces, documentar cómo y por qué se usan ciertas anotaciones es una buena práctica. Además, experimentar con diferentes combinaciones y probar a crear anotaciones personalizadas te permitirá descubrir nuevas formas de optimizar tu aplicación.

5. **Aprovechar las Anotaciones en las Pruebas**: Spring proporciona anotaciones específicas para pruebas (`@SpringBootTest`, `@WebMvcTest`, etc.), las cuales permiten configurar entornos de prueba aislados y más rápidos. Conocer cómo utilizarlas puede hacer una gran diferencia en la calidad del software.

Para abordar las anotaciones mas importantes de Spring Boot, vamos a dar una explicación detallada junto con ejemplos prácticos y consejos sobre su uso. Este artículo se basa en una arquitectura de aplicación que simula un sistema bancario, donde se manejan entidades como `Banco`, `Cuenta` y `Cliente`, lo que facilitará entender la implementación de cada anotación en un contexto real.

### 1. **@SpringBootApplication**

La anotación `@SpringBootApplication` se utiliza para inicializar la aplicación Spring Boot. Combina tres anotaciones: `@Configuration`, `@EnableAutoConfiguration` y `@ComponentScan`.

**Ejemplo:**

```java
@SpringBootApplication
public class BancoApplication {
    public static void main(String[] args) {
        SpringApplication.run(BancoApplication.class, args);
    }
}
```

> Usa esta anotación en la clase principal de tu aplicación para habilitar la configuración automática y el escaneo de componentes, lo que simplifica la configuración inicial.

---

### 2. **@EnableAutoConfiguration**

Esta anotación permite que Spring Boot configure automáticamente el proyecto según las dependencias presentes en el classpath.

**Ejemplo:**

```java
@EnableAutoConfiguration
@Configuration
public class BancoConfig {
    // Configuración personalizada
}
```

> No suele ser necesario declararla explícitamente, ya que `@SpringBootApplication` la incluye. Es útil cuando necesitas habilitar configuración automática en clases individuales.

---

### 3. **@SpringBootConfiguration**

Indica que una clase proporciona configuraciones específicas de Spring Boot, esencialmente similar a `@Configuration`.

**Ejemplo:**

```java
@SpringBootConfiguration
public class ConfiguracionBanco {
    // Configuración específica para el banco
}
```

> Se usa principalmente para separar configuraciones específicas de Spring Boot en diferentes clases, especialmente en proyectos complejos.

---

### 4. **@ComponentScan**

Esta anotación especifica los paquetes que deben escanearse para detectar componentes.

**Ejemplo:**

```java
@SpringBootApplication
@ComponentScan(basePackages = {"com.banco.servicios", "com.banco.controladores"})
public class BancoApplication {
    // Clase principal
}
```

> Es especialmente útil cuando tus componentes estén en paquetes fuera del paquete base de la aplicación para asegurarte de que todos los beans sean detectados.

---

### 5. **@RestController y @Controller**

Estas anotaciones se usan en controladores web. `@RestController` combina `@Controller` y `@ResponseBody`.

**Ejemplo:**

```java
@RestController
@RequestMapping("/cuentas")
public class CuentaController {
    @GetMapping("/{id}")
    public Cuenta obtenerCuenta(@PathVariable Long id) {
        // Lógica para obtener cuenta
        return new Cuenta(id, "12345", 500.0);
    }
}
```

> Usa `@RestController` para servicios REST y `@Controller` si necesitas devolver vistas HTML.

---

### 6. **@RequestMapping, @GetMapping, @PostMapping, @PutMapping, @DeleteMapping, @PatchMapping**

Estas anotaciones se usan para mapear métodos HTTP a controladores.

**Ejemplo:**

```java
@RestController
@RequestMapping("/clientes")
public class ClienteController {
    @PostMapping
    public Cliente crearCliente(@RequestBody Cliente cliente) {
        // Lógica para crear cliente
        return cliente;
    }
}
```

> Define métodos claros en tus controladores para que las peticiones sean intuitivas y coincidan con el estándar RESTful.

---

### 7. **@ResponseBody**

Indica que el tipo de retorno de un método debe ser escrito directamente en el cuerpo de la respuesta HTTP.

**Ejemplo:**

```java
@Controller
public class SaludoController {
    @RequestMapping("/saludo")
    @ResponseBody
    public String saludo() {
        return "Hola, bienvenido a nuestro banco!";
    }
}
```

> Esta anotación es implícita en `@RestController`, pero es útil en métodos individuales en un `@Controller`.

---

### 8. **@Component, @Service, @Repository**

Estas anotaciones indican el rol de una clase en la capa de persistencia o lógica de negocio.

**Ejemplo:**

```java
@Service
public class CuentaService {
    // Lógica de negocio para cuentas
}
```

> Usa `@Component` para clases generales, `@Service` para lógica de negocio, y `@Repository` para interacción con la base de datos.

---

### 9. **@PathVariable, @RequestParam**

Permiten la captura de parámetros de ruta y parámetros de consulta.

**Ejemplo:**

```java
@RestController
@RequestMapping("/cuentas")
public class CuentaController {
    @GetMapping("/{id}")
    public Cuenta obtenerCuenta(@PathVariable Long id, @RequestParam(defaultValue = "false") boolean detalles) {
        // Lógica para obtener cuenta con opción de detalles
        return new Cuenta(id, "12345", 500.0);
    }
}
```

> Usa `@PathVariable` para variables obligatorias en la URL y `@RequestParam` para parámetros opcionales.

---

### 10. **@CrossOrigin**

Permite solicitudes entre dominios (CORS).

**Ejemplo:**

```java
@RestController
@CrossOrigin(origins = "http://clientes.app")
public class ClienteController {
    // Métodos para controlar clientes
}
```

> Úsala para controlar los permisos de acceso cuando el frontend y el backend están en dominios distintos.

---

### 11. **@Autowired**

Se usa para la inyección de dependencias en Spring.

**Ejemplo:**

```java
@Service
public class ClienteService {
    @Autowired
    private ClienteRepository clienteRepository;

    // Lógica del servicio
}
```

> Usa `@Autowired` en constructores preferentemente para mejorar la inmutabilidad y la prueba de tu código.

---

### 12. **@Qualifier**

Designa cuál bean autowirear cuando hay múltiples candidatos.

**Ejemplo:**

```java
@Service
public class CuentaService {
    @Autowired
    @Qualifier("cuentaAhorro")
    private Cuenta cuenta;

    // Lógica del servicio
}
```

> Úsala cuando tengas múltiples implementaciones del mismo tipo para elegir una específica.

---

### 13. **@Primary**

Define un bean como preferido cuando hay múltiples candidatos. Esto resulta útil cuando tienes varias implementaciones del mismo servicio y necesitas establecer una por defecto.

**Ejemplo:**

```java
@Configuration
public class ConfiguracionCuenta {
    @Bean
    @Primary
    public Cuenta cuentaAhorro() {
        return new Cuenta("12345", 1000.0);
    }

    @Bean
    public Cuenta cuentaAlternativa() {
        return new Cuenta("6789", 2000.0);
    }
}
```

> Se usa `@Primary` para establecer una implementación predeterminada cuando varias implementaciones del mismo bean están disponibles. Esto simplifica la inyección de dependencias cuando solo necesitas una implementación principal.

---

### 14. **@Bean**

Define un bean para el contexto de Spring. Este será administrado por el contenedor de Spring. Es comúnmente utilizado en clases de configuración para crear y configurar objetos que no puedes anotar directamente como `@Component`.

**Ejemplo:**

```java
@Configuration
public class ConfiguracionCliente {
    @Bean
    public Cliente cliente() {
        return new Cliente("John Doe", "1234");
    }
}
```

> Úsala en configuraciones para instancias personalizadas y evitar la duplicación de código. `@Bean` es una alternativa para definir beans cuando necesitas más control sobre su creación. Úsalo cuando la instancia requiere inicialización específica que no se puede realizar solo con `@Component`.

---

### 15. **@Value**

Permite inyectar valores de configuración.

**Ejemplo:**

```java
@Service
public class ConfiguracionService {
    @Value("${banco.nombre}")
    private String nombreBanco;

    // Uso de nombreBanco
}
```

> Usa `@Value` para parámetros de configuración que pueden cambiar según el entorno (por ejemplo, desarrollo vs producción).

---

### 16. **@ConfigurationProperties**

Permite enlazar configuraciones externas a una clase.

**Ejemplo:**

```java
@ConfigurationProperties(prefix = "banco")
public class BancoProperties {
    private String nombre;
    private String direccion;

    // Getters y setters
}
```

> Es útil cuando se tienen múltiples parámetros de configuración relacionados entre sí.

---

### 17. **@PropertySource**

Especifica la ubicación de propiedades para agregar al entorno de Spring.

**Ejemplo:**

```java
@Configuration
@PropertySource("classpath:configuracionBanco.properties")
public class ConfiguracionBanco {
    // Configuración usando propiedades externas
}
```

> Úsala cuando necesites añadir archivos de propiedades adicionales a tu aplicación.

---

Continuando con las últimas anotaciones que figuran en la imagen:

### 18. **@Profile**

La anotación `@Profile` permite definir beans específicos o configuraciones para diferentes entornos (por ejemplo, `desarrollo`, `producción`, `pruebas`). Esto facilita la gestión de configuraciones para cada ambiente, evitando cambios manuales.

**Ejemplo:**

```java
@Configuration
@Profile("desarrollo")
public class ConfiguracionDesarrollo {
    @Bean
    public Cliente clienteDesarrollo() {
        return new Cliente("Cliente de desarrollo", "0001");
    }
}
```

> Define perfiles como `application-dev.yml`, `application-prod.yml`, etc., para configurar de manera automática las propiedades del entorno. Esta práctica es común en proyectos donde se debe asegurar que los entornos tengan configuraciones y datos específicos sin afectar la lógica de producción.

---

### 19. **@Scheduled**

Permite programar la ejecución de métodos en intervalos fijos o cron, útil para tareas periódicas, como reportes o limpieza de datos.

**Ejemplo:**

```java
@Service
public class ReporteService {
    @Scheduled(cron = "0 0 12 * * ?")
    public void generarReporteDiario() {
        // Lógica para generar reporte
        System.out.println("Reporte generado a las 12:00 PM");
    }
}
```

> Usa esta anotación para tareas recurrentes, como notificaciones diarias o procesos de mantenimiento. Asegúrate de configurar correctamente el `cron` para evitar errores en la periodicidad de ejecución.

---

### 20. **@Conditional**

Permite incluir o excluir beans o configuraciones según ciertas condiciones. Es útil cuando necesitas activar configuraciones específicas solo si se cumplen determinados criterios.

**Ejemplo:**

```java
@Configuration
public class ConfiguracionCondicional {
    @Bean
    @Conditional(ProduccionCondition.class)
    public Cliente clienteProduccion() {
        return new Cliente("Cliente en producción", "1001");
    }
}
```

> Implementa condiciones personalizadas extendiendo `Condition`, especialmente cuando dependes de variables del sistema o configuraciones de entorno. Esto ayuda a personalizar el contexto de la aplicación en diferentes escenarios.

---

### 21. **@ConfigurationProperties**

Permite enlazar propiedades de configuración externa a un objeto Java, facilitando la administración de configuraciones agrupadas en un solo lugar. Es ideal para propiedades complejas, como configuraciones de bases de datos o parámetros de servicios externos.

**Ejemplo:**

```java
@ConfigurationProperties(prefix = "banco")
public class BancoConfigProperties {
    private String nombre;
    private String direccion;
    private int numeroSucursales;

    // Getters y setters
}
```

> Usa `@ConfigurationProperties` en combinación con archivos `.yml` o `.properties` para centralizar y estructurar configuraciones. Esto facilita cambios y mejora la organización de la configuración en entornos complejos.

---

### 22. **@PropertySource**

Especifica ubicaciones de archivos de propiedades que deben ser cargados en el entorno de Spring. Esto es útil cuando deseas utilizar configuraciones externas sin incluirlas directamente en el `application.yml` o `application.properties`.

**Ejemplo:**

```java
@Configuration
@PropertySource("classpath:banco.properties")
public class BancoConfig {
    @Value("${banco.nombre}")
    private String nombreBanco;

    // Otros métodos y configuraciones
}
```

> Usa `@PropertySource` para cargar propiedades específicas desde archivos adicionales. Esto es útil para modular configuraciones en proyectos grandes, especialmente cuando deseas aislar ciertas propiedades en diferentes archivos.

---

### 23. **@SpringBootTest, @DataJpaTest, @WebMvcTest, @JsonTest, @WebFluxTest**

Estas anotaciones son específicas para pruebas, facilitando la configuración de entornos de prueba en Spring Boot. Cada una tiene un propósito distinto:

- `@SpringBootTest`: Carga el contexto completo de Spring, útil para pruebas de integración.
- `@DataJpaTest`: Configura solo los repositorios JPA, ideal para pruebas de persistencia.
- `@WebMvcTest`: Configura solo el contexto MVC, ideal para probar controladores.
- `@JsonTest`: Configura pruebas de serialización/deserialización JSON.
- `@WebFluxTest`: Configura el entorno para probar aplicaciones WebFlux (reactivas).

**Ejemplo:**

```java
@SpringBootTest
public class CuentaServiceTest {
    @Autowired
    private CuentaService cuentaService;

    @Test
    public void testCrearCuenta() {
        Cuenta cuenta = cuentaService.crearCuenta(new Cuenta("001", 500.0));
        assertNotNull(cuenta);
    }
}
```

> Usa estas anotaciones según el alcance de la prueba que desees realizar. `@SpringBootTest` es útil para pruebas integrales, mientras que `@WebMvcTest` o `@DataJpaTest` son más eficientes para pruebas unitarias en entornos específicos.

## Patrón decorador

Las anotaciones en Java y, en particular, en Spring Boot, se desarrollan siguiendo el **patrón de diseño Decorator (Decorador)**. Este patrón permite "*decorar*" o "*anotar*" una clase, método o campo con información adicional sin alterar su estructura original. En lugar de modificar el código fuente directamente, las anotaciones se aplican sobre el código para agregarle responsabilidades o instrucciones adicionales. Así, se logra que el framework interprete estas anotaciones y actúe en consecuencia, configurando, inyectando o gestionando los componentes de manera más declarativa y menos invasiva.

### ¿Qué problemas solucionan las anotaciones?

1. **Simplicidad en la Configuración**: Antes de las anotaciones, se tenía que configurar los componentes de la aplicación de forma manual en archivos XML o en código fuente, lo que era engorroso y propenso a errores. Las anotaciones permiten especificar directamente en el código cómo deben configurarse los componentes.

2. **Desacoplamiento y Flexibilidad**: Las anotaciones permite separar el "*qué hace*" el componente del "*cómo se configura*", manteniendo el código más limpio y modular. Esto facilita el mantenimiento y la escalabilidad de las aplicaciones.

3. **Autodocumentación**: Al colocar anotaciones en los componentes, el código se vuelve más comprensible. Al ver anotaciones como `@Service` o `@Controller`, otros desarrolladores pueden entender inmediatamente el rol de esa clase sin necesidad de leer toda su implementación.

4. **Eliminación de Código Repetitivo**: Muchas configuraciones son comunes en varias partes de una aplicación (*por ejemplo, la inyección de dependencias*). Las anotaciones permiten que estos comportamientos se definan una sola vez y se reutilicen fácilmente en todo el proyecto.

### ¿Es fácil crear anotaciones?

Crear anotaciones es bastante sencillo en Java, aunque agregarles una funcionalidad real requiere conocimiento sobre aspectos avanzados como el uso de *AOP (Programación Orientada a Aspectos)* o *Reflection*. Con AOP, puedes interceptar métodos y agregar lógica adicional cuando se encuentran ciertas anotaciones. En el contexto de Spring, también puedes crear anotaciones personalizadas para ayudar en tareas como la validación de datos o el manejo de transacciones.

### Ejemplos prácticos para crear anotaciones personalizadas

A continuación, exploraremos cómo crear anotaciones que podrían ser útiles en un contexto de una aplicación bancaria.

#### Ejemplo 1: Anotación para Validar Permisos de Acceso

Supongamos que queremos asegurar que solo ciertos usuarios (*por ejemplo, administradores*) puedan acceder a ciertas operaciones, como ver el saldo de todas las cuentas. Podemos crear una anotación `@RequiereRol` para restringir el acceso a métodos específicos.

1. **Definir la anotación `@RequiereRol`:**

   ```java
   import java.lang.annotation.ElementType;
   import java.lang.annotation.Retention;
   import java.lang.annotation.RetentionPolicy;
   import java.lang.annotation.Target;

   @Target(ElementType.METHOD)
   @Retention(RetentionPolicy.RUNTIME)
   public @interface RequiereRol {
       String value(); // Rol necesario para acceder al método
   }
   ```

2. **Aplicar la anotación en un método:**

   ```java
   public class CuentaService {

       @RequiereRol("ADMIN")
       public List<Cuenta> obtenerTodasLasCuentas() {
           // Lógica para obtener todas las cuentas
       }
   }
   ```

3. **Implementar la lógica de validación con AOP:**

   Utilizando AspectJ o AOP de Spring, interceptamos los métodos anotados y verificamos el rol del usuario actual.

   ```java
   import org.aspectj.lang.annotation.Aspect;
   import org.aspectj.lang.annotation.Before;
   import org.springframework.stereotype.Component;

   @Aspect
   @Component
   public class VerificacionRolAspecto {

       @Before("@annotation(requiereRol)")
       public void verificarAcceso(RequiereRol requiereRol) throws Exception {
           String rolRequerido = requiereRol.value();
           // Lógica para verificar el rol del usuario
           String rolUsuario = obtenerRolDelUsuarioActual();
           if (!rolUsuario.equals(rolRequerido)) {
               throw new Exception("Acceso denegado: se requiere el rol " + rolRequerido);
           }
       }

       private String obtenerRolDelUsuarioActual() {
           // Lógica para obtener el rol del usuario actual
           return "USER"; // Ejemplo de rol predeterminado
       }
   }
   ```

   **Uso:** Esta anotación `@RequiereRol` permite restringir el acceso a ciertos métodos según el rol del usuario, agregando seguridad y manteniendo el código limpio.

---

#### Ejemplo 2: Anotación para Medir el Tiempo de Ejecución

En algunas aplicaciones, es útil medir cuánto tiempo toma ejecutar ciertos métodos, especialmente en consultas de alto rendimiento o en operaciones costosas. Podemos crear una anotación `@TiempoEjecucion` para medir y registrar el tiempo de ejecución de un método.

1. **Definir la anotación `@TiempoEjecucion`:**

   ```java
   import java.lang.annotation.ElementType;
   import java.lang.annotation.Retention;
   import java.lang.annotation.RetentionPolicy;
   import java.lang.annotation.Target;

   @Target(ElementType.METHOD)
   @Retention(RetentionPolicy.RUNTIME)
   public @interface TiempoEjecucion {
   }
   ```

2. **Aplicar la anotación en un método:**

   ```java
   public class TransaccionService {

       @TiempoEjecucion
       public void procesarTransaccion() {
           // Lógica para procesar una transacción
       }
   }
   ```

3. **Implementar la lógica para medir el tiempo de ejecución:**

   Utilizando AOP, interceptamos el método y calculamos el tiempo que tarda en ejecutarse.

   ```java
   import org.aspectj.lang.ProceedingJoinPoint;
   import org.aspectj.lang.annotation.Around;
   import org.aspectj.lang.annotation.Aspect;
   import org.springframework.stereotype.Component;

   @Aspect
   @Component
   public class TiempoEjecucionAspecto {

       @Around("@annotation(TiempoEjecucion)")
       public Object medirTiempo(ProceedingJoinPoint joinPoint) throws Throwable {
           long inicio = System.currentTimeMillis();
           Object resultado = joinPoint.proceed();
           long fin = System.currentTimeMillis();
           System.out.println("Tiempo de ejecución de " + joinPoint.getSignature() + ": " + (fin - inicio) + " ms");
           return resultado;
       }
   }
   ```

   **Uso:** La anotación `@TiempoEjecucion` permite monitorear el rendimiento de métodos específicos y ver cuántos milisegundos tardan en ejecutarse. Esto es especialmente útil para optimización en métodos que interactúan con bases de datos o manejan cálculos intensivos.

---

#### Ejemplo 3: Anotación para Validar Campos No Vacíos en Entradas de Usuario

En una aplicación bancaria, podemos crear una anotación para validar que ciertos campos no sean nulos o vacíos, como el nombre del cliente o el número de cuenta. Para ello, creamos una anotación `@NoVacio`.

1. **Definir la anotación `@NoVacio`:**

   ```java
   import java.lang.annotation.ElementType;
   import java.lang.annotation.Retention;
   import java.lang.annotation.RetentionPolicy;
   import java.lang.annotation.Target;
   import javax.validation.Constraint;
   import javax.validation.Payload;

   @Target({ ElementType.FIELD, ElementType.PARAMETER })
   @Retention(RetentionPolicy.RUNTIME)
   @Constraint(validatedBy = NoVacioValidator.class)
   public @interface NoVacio {
       String message() default "El campo no debe estar vacío";
       Class<?>[] groups() default {};
       Class<? extends Payload>[] payload() default {};
   }
   ```

2. **Crear el validador `NoVacioValidator`:**

   ```java
   import javax.validation.ConstraintValidator;
   import javax.validation.ConstraintValidatorContext;

   public class NoVacioValidator implements ConstraintValidator<NoVacio, String> {

       @Override
       public void initialize(NoVacio constraintAnnotation) {}

       @Override
       public boolean isValid(String valor, ConstraintValidatorContext context) {
           return valor != null && !valor.trim().isEmpty();
       }
   }
   ```

3. **Aplicar la anotación en la clase `Cliente`:**

   ```java
   public class Cliente {
       @NoVacio(message = "El nombre no debe estar vacío")
       private String nombre;

       @NoVacio(message = "El número de cuenta no debe estar vacío")
       private String numeroCuenta;

       // Constructor, getters y setters
   }
   ```

   **Uso:** La anotación `@NoVacio` permite validar automáticamente que ciertos campos no estén vacíos, simplificando la validación de entrada de datos y centralizando las reglas de negocio.

## ¿Porque usar anotaciones?

Crear anotaciones personalizadas permite resolver problemas específicos de manera eficiente y sin redundancia de código. En los ejemplos anteriores las anotaciones como `@RequiereRol`, `@TiempoEjecucion` y `@NoVacio` ofrecen soluciones prácticas para escenarios comunes en una aplicación, mejorando la seguridad, el rendimiento y la validación de datos. Además, gracias a la integración de Spring con AOP y el sistema de validación, estas anotaciones personalizadas pueden implementarse y gestionarse de manera sencilla, maximizando el potencial de las anotaciones y haciendo el código más limpio y modular.

Las anotaciones en Spring Boot son una herramienta invaluable. A través de ellas, se logra una configuración automática y una arquitectura limpia y escalable, eliminando configuraciones manuales y permitiendo un enfoque más claro y estructurado en el desarrollo. Sin embargo, como cualquier herramienta poderosa, requieren un conocimiento adecuado para ser utilizadas de forma efectiva. Profundizar en su funcionamiento y aprender a crear anotaciones personalizadas puede transformar el código de un proyecto, haciéndolo más robusto, flexible y fácil de mantener. Las anotaciones no solo simplifican, sino que también potencian el desarrollo backend en Java, y aprender a aprovecharlas al máximo es una inversión que vale la pena.

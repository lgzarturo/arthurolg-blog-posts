---
title: Buenas Prácticas para el Diseño de API REST. Evita Exponer Entidades JPA y Usa DTOs Eficientemente
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/mejores-practicas-api-rest-java-spring-boot-dtos.webp
description: Te enseño cómo mejorar el diseño de tu API REST en Java utilizando DTOs en lugar de exponer entidades JPA directamente. Aprende a estructurar tus paquetes siguiendo buenas prácticas que optimizan el rendimiento, la seguridad y la mantenibilidad de tu aplicación en Spring Boot.
author: Arturo López
date: 2024-10-30
label: Arquitectura, Microservicios, Spring Boot, Java
---

## Diseño de API: No expongas tus entidades JPA en tu API REST

Cuando se diseña una API REST, una de las decisiones más importantes que los desarrolladores deben tomar es cómo manejar los datos que se expondrán a través de los endpoints. Una de las prácticas comunes, pero problemáticas, es exponer directamente las entidades JPA que representan el modelo de persistencia en la base de datos. Aunque esta estrategia puede parecer conveniente y simple al principio, genera múltiples desafíos que pueden afectar la escalabilidad, la mantenibilidad y el rendimiento a largo plazo.

En este artículo, exploraremos la teoría y la practica de por qué no deberías exponer tus entidades JPA directamente en tu API REST y cómo usar DTOs (*Data Transfer Objects*) puede ser una solución más adecuada. Además, analizaremos los problemas que pueden surgir al trabajar con asociaciones complejas y cómo esta separación de capas puede ayudarte a construir APIs más robustas y flexibles.

## El problema de exponer entidades JPA directamente

### 1. Acoplamiento fuerte entre la API y la base de datos

Uno de los principales problemas de exponer directamente las entidades JPA es el **acoplamiento fuerte** que esto genera entre tu API y la base de datos. Las entidades JPA están diseñadas para interactuar con la capa de persistencia y, a menudo, contienen anotaciones y lógica específicas para esa capa. Si estas entidades se exponen a través de la API, cualquier cambio en el modelo de la base de datos afectará directamente a los clientes de la API.

> El acoplamiento fuerte es cuando dos módulos o componentes de un sistema dependen excesivamente entre sí, lo que dificulta modificar uno sin afectar al otro.
>
> Es como si dos amigos fueran tan inseparables que no pudieran hacer planes sin consultarse mutuamente. Si uno cambia de idea o ubicación, el otro siempre tiene que adaptarse, complicando cualquier decisión.

Por ejemplo, imagina que tu entidad JPA contiene información sobre un cliente con detalles como su nombre, dirección y número de teléfono. Si en el futuro decides cambiar la estructura de tu base de datos para mejorar el rendimiento o agregar nuevas funcionalidades (*como dividir la dirección en múltiples campos*), cualquier cliente que consuma esa API se verá afectado por esos cambios, lo que puede romper la compatibilidad y causar errores en producción.

En lugar de depender de las entidades, una mejor práctica es utilizar DTOs, que permiten desacoplar el modelo de persistencia del modelo de API. Esto significa que puedes hacer cambios en tu base de datos sin afectar la estructura de tu API, permitiendo que ambas capas evolucionen de manera independiente.

### 2. Problemas con las asociaciones entre entidades

Otro desafío al exponer entidades JPA en una API es cómo manejar las asociaciones entre ellas. En el mundo de la persistencia, las relaciones entre entidades (*como las de uno a muchos o muchos a muchos*) se gestionan a nivel de base de datos, lo que funciona bien dentro de ese contexto. Sin embargo, cuando se trata de exponer estas relaciones a través de una API REST, las cosas se complican.

Por ejemplo, si tienes una entidad de `Pedido` que está asociada con múltiples `Productos`, exponer esta entidad directamente en la API puede llevar a una serie de problemas:

- **Cargas adicionales**: Al serializar un `Pedido`, la API podría intentar serializar todos los productos asociados, lo que podría generar consultas adicionales a la base de datos, impactando negativamente el rendimiento de la aplicación.
- **Problemas de consistencia**: Si los productos asociados a un pedido cambian mientras la API está serializando la respuesta, podrías terminar con datos inconsistentes.
- **Exceso de información**: Es posible que no desees exponer todos los detalles de los productos en la API. Exponer la entidad directamente podría significar enviar más datos de los necesarios, lo que genera problemas de privacidad y eficiencia.

> Serializar es convertir un objeto o dato en un formato que pueda ser transmitido o almacenado (*como JSON o XML*), y deserializar es el proceso inverso, convirtiendo ese formato de nuevo en un objeto utilizable.
>
> Es como empaquetar un regalo (*serializar*) para que pueda enviarse por correo y luego abrir el paquete (*deserializar*) cuando llega a su destino para usar lo que hay dentro.

El uso de DTOs te permite controlar cómo estas asociaciones se representan en la API. Por ejemplo, en lugar de devolver todos los detalles de los productos asociados a un pedido, podrías devolver solo los identificadores de esos productos o enlaces a los recursos correspondientes, siguiendo el principio HATEOAS (*Hypermedia as the Engine of Application State*).

### 3. Dificultad en la implementación de principios REST

Un buen diseño de API REST no se trata solo de enviar y recibir datos; también se trata de seguir ciertos principios fundamentales que hacen que la API sea flexible y fácil de usar a largo plazo. Uno de estos principios es HATEOAS, que sugiere que en lugar de incrustar asociaciones directamente en los objetos de respuesta, deberías proporcionar enlaces a otros recursos.

> Ya hablamos de HATEOAS, pero para recordar: Es una práctica importante dentro de RESTful APIs que ayuda a hacerlas más flexibles y evolutivas. Gracias a la implementación en Spring Boot con el starter de HATEOAS (`org.springframework.boot:spring-boot-starter-hateoas`), puedes fácilmente añadir enlaces que guíen a los clientes a través de las posibles acciones de tu API, haciéndola más auto-descriptiva y desacoplada de los clientes que la consumen.
>
> HATEOAS fue introducido como parte del concepto REST por [Roy Fielding](https://en.wikipedia.org/wiki/Roy_Fielding) en el año 2000. Su intención era permitir que las aplicaciones web fueran más adaptables y menos dependientes del conocimiento previo de las rutas y las interacciones con el servidor.

Cuando expones entidades JPA directamente, tiendes a incrustar asociaciones dentro del objeto de respuesta, lo que va en contra de este principio. Además, las entidades JPA a menudo contienen lógica que está muy atada a la capa de persistencia, lo que puede hacer que sea más difícil implementar características como paginación, filtrado o búsquedas eficientes.

Al utilizar DTOs, puedes estructurar tus respuestas de API de una manera que sea más amigable para los clientes, siguiendo principios RESTful y proporcionando enlaces a otros recursos en lugar de enviar objetos anidados complejos.

### 4. Problemas de rendimiento

El rendimiento es una consideración clave al diseñar una API. Al exponer entidades JPA directamente, puedes introducir cuellos de botella de rendimiento que son difíciles de optimizar. Aquí algunos ejemplos comunes:

- **Cargas ansiosas**: Las entidades JPA a menudo están configuradas para realizar cargas diferidas o ansiosas de datos relacionados. Si expones estas entidades en tu API, podrías terminar realizando más consultas a la base de datos de las necesarias, lo que afecta el rendimiento de tu aplicación.
- **Serialización costosa**: Las entidades JPA a menudo contienen muchas relaciones y campos que no son relevantes para el cliente de la API. Serializar toda esa información puede ser costoso en términos de rendimiento, especialmente si la API necesita manejar grandes volúmenes de datos.

Al usar DTOs, puedes seleccionar exactamente qué datos deseas incluir en la respuesta de la API. Esto te permite optimizar la cantidad de datos que se envían a través de la red, reduciendo el tiempo de procesamiento y mejorando el rendimiento general de la aplicación.

### 5. Mantenibilidad y escalabilidad

La mantenibilidad es uno de los factores más importantes a tener en cuenta en el desarrollo de software a largo plazo. A medida que tu API crece y evoluciona, es probable que necesites realizar cambios tanto en la capa de persistencia como en la capa de presentación. Si has acoplado estas dos capas al exponer entidades JPA directamente, cada cambio en la base de datos requerirá un cambio correspondiente en la API, lo que puede ser costoso y propenso a errores.

Usar DTOs para desacoplar estas capas te permite hacer cambios en la base de datos sin romper la API, lo que facilita la evolución de ambas capas de manera independiente. Además, el uso de DTOs también facilita la implementación de pruebas unitarias y de integración, ya que puedes probar cada capa por separado sin depender de la otra.

## La solución: Usar DTOs (Data Transfer Objects)

### 1. Separación de preocupaciones

Los DTOs te permiten separar claramente la capa de persistencia de la capa de presentación de datos. Mientras que las entidades JPA están optimizadas para interactuar con la base de datos, los DTOs están diseñados para transportar datos entre el servidor y el cliente. Esto significa que puedes estructurar tus DTOs de una manera que sea óptima para la API sin preocuparte por los detalles de cómo los datos están almacenados en la base de datos.

Por ejemplo, un DTO para un cliente podría incluir solo los datos relevantes para la API, como el nombre y el correo electrónico, mientras que la entidad JPA correspondiente podría contener mucha más información, como la dirección o el historial de compras. Esto no solo reduce la cantidad de datos que se envían a través de la red, sino que también permite una mayor flexibilidad en la evolución de tu API.

### 2. Mejora del rendimiento

Con los DTOs, tienes un control preciso sobre qué datos se serializan y se envían al cliente. Esto te permite evitar la serialización de datos innecesarios y optimizar la forma en que se representan las asociaciones entre entidades. Por ejemplo, en lugar de enviar toda la información de un pedido y sus productos asociados, podrías enviar solo el identificador del pedido y enlaces a los productos, siguiendo el principio HATEOAS.

### 3. Flexibilidad en el diseño de la API

Al utilizar DTOs, también tienes la flexibilidad de diseñar diferentes representaciones de los mismos datos para diferentes clientes. Por ejemplo, un cliente móvil podría necesitar una representación más simple de los datos en comparación con un cliente web. Con DTOs, puedes crear diferentes versiones de los mismos datos según las necesidades de cada cliente, sin cambiar la estructura de las entidades subyacentes.

## Reflexión antes de la práctica

Si lo que quieres es construir una API REST que sea flexible, eficiente y capaz de evolucionar a medida que tu aplicación crece, la mejor práctica es evitar exponer entidades JPA directamente y, en su lugar, utilizar DTOs para manejar la transferencia de datos. Aunque puede requerir un poco más de trabajo inicial, esta estrategia te permitirá mantener tu API escalable, mantenible y optimizada para el rendimiento a largo plazo.

Exponer entidades JPA directamente en tu API REST puede parecer una solución rápida y fácil, pero a largo plazo, genera una serie de problemas relacionados con el rendimiento, la mantenibilidad y la flexibilidad (*lo digo por experiencia*). Usar DTOs para desacoplar la capa de persistencia de la capa de presentación de datos es una estrategia mucho más robusta que te permite optimizar el rendimiento, seguir principios RESTful y mantener tu API escalable y mantenible.

Recuerda que el diseño de una API REST es una tarea compleja que requiere equilibrar múltiples consideraciones, como el rendimiento, la seguridad, la escalabilidad y la mantenibilidad. Al adoptar buenas prácticas, como el uso de DTOs en lugar de entidades JPA, puedes construir APIs más robustas y eficientes que satisfagan las necesidades de tus clientes y de tu aplicación a largo plazo.

> "La simplicidad es el último grado de sofisticación." - *Leonardo da Vinci*

---

## Práctica: Implementando DTOs en una API REST con Spring Boot

Para demostrar las diferencias entre exponer entidades JPA directamente en una API y usar DTOs, primero mostraré un ejemplo en el que se exponen las entidades JPA utilizando anotaciones para la serialización y deserialización. Luego, presentaré un ejemplo más limpio y eficiente utilizando DTOs en lugar de las entidades.

> **Nota importante**: Recuerda que el código es mejor escribirlo en inglés para mantener la consistencia y facilitar la colaboración con otros desarrolladores. Aunque en este artículo utilizo ejemplos en español, te recomiendo que en tu código y proyectos utilices el inglés como idioma principal.

### Ejemplo 1: Exposición directa de Entidades JPA

En este primer caso, estamos exponiendo directamente las entidades JPA en la API. Aunque esto puede parecer más simple al principio, notarás cómo las anotaciones para la serialización y la deserialización empiezan a ensuciar el código y se introducen varios problemas de acoplamiento.

#### Entidad `Producto`

```java
@Entity
public class Producto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String nombre;

    @Column(nullable = false)
    private Double precio;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "categoria_id")
    @JsonBackReference // Esto evita la recursión infinita en la serialización
    private Categoria categoria;

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public Double getPrecio() { return precio; }
    public void setPrecio(Double precio) { this.precio = precio; }

    public Categoria getCategoria() { return categoria; }
    public void setCategoria(Categoria categoria) { this.categoria = categoria; }
}
```

#### Entidad `Categoria`

```java
@Entity
public class Categoria {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String nombre;

    @OneToMany(mappedBy = "categoria", cascade = CascadeType.ALL, orphanRemoval = true)
    @JsonManagedReference // Esto evita la recursión infinita en la serialización
    private List<Producto> productos = new ArrayList<>();

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public List<Producto> getProductos() { return productos; }
    public void setProductos(List<Producto> productos) { this.productos = productos; }
}
```

#### Controlador que expone las Entidades JPA

```java
@RestController
@RequestMapping("/api/productos")
public class ProductoController {

    @Autowired
    private ProductoRepository productoRepository;

    @GetMapping
    public List<Producto> obtenerProductos() {
        return productoRepository.findAll();
    }

    @PostMapping
    public Producto crearProducto(@RequestBody Producto producto) {
        return productoRepository.save(producto);
    }
}
```

### Problemas del enfoque anterior

1. **Exceso de datos**: La API podría estar exponiendo más información de la necesaria (*por ejemplo, toda la información de la `Categoria` cuando tal vez solo se necesita su `id`*).
2. **Anotaciones innecesarias**: Como puedes ver, necesitamos anotaciones como `@JsonManagedReference` y `@JsonBackReference` para evitar la recursión infinita al serializar relaciones bidireccionales.
3. **Acoplamiento fuerte**: Cualquier cambio en las entidades JPA (*como la adición de un nuevo campo*) impactará directamente la API.
4. **Mantenibilidad**: El código está mezclando la lógica de persistencia con la de presentación, lo que dificulta su mantenimiento a largo plazo.

> Es importante no mezclar la lógica de persistencia (*cómo y dónde se guardan los datos*) con la de presentación (*cómo se muestran o transmiten los datos*) porque cada una tiene un propósito diferente. La persistencia se centra en el manejo de datos en la base de datos, mientras que la presentación está enfocada en la experiencia del usuario o cliente. Si se mezclan, cualquier cambio en la forma en que se almacenan los datos puede afectar cómo se presentan o viceversa, lo que dificulta la mantenibilidad y escalabilidad del sistema.
>
> Imagina que es como construir una casa donde las tuberías de agua y el cableado eléctrico están entrelazados. Si necesitas arreglar algo en el sistema eléctrico, podrías terminar dañando las tuberías, causando más problemas. Mantenerlas separadas permite que cada sistema funcione correctamente sin interferir con el otro.

---

### Ejemplo 2: Usando DTOs (Data Transfer Objects)

En este segundo caso, usamos DTOs para desacoplar la lógica de persistencia de la presentación, lo que nos permite tener un mayor control sobre qué datos se exponen y cómo se estructuran.

#### Entidad `Producto`

```java
@Entity
public class Producto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String nombre;

    @Column(nullable = false)
    private Double precio;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "categoria_id")
    private Categoria categoria;

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public Double getPrecio() { return precio; }
    public void setPrecio(Double precio) { this.precio = precio; }

    public Categoria getCategoria() { return categoria; }
    public void setCategoria(Categoria categoria) { this.categoria = categoria; }
}
```

#### Entidad `Categoria`

```java
@Entity
public class Categoria {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String nombre;

    @OneToMany(mappedBy = "categoria", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Producto> productos = new ArrayList<>();

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public List<Producto> getProductos() { return productos; }
    public void setProductos(List<Producto> productos) { this.productos = productos; }
}
```

#### DTO `ProductoDTO`

```java
public class ProductoDTO {

    private Long id;
    private String nombre;
    private Double precio;
    private Long categoriaId; // Solo mostramos el ID de la categoría

    public ProductoDTO() {}

    public ProductoDTO(Long id, String nombre, Double precio, Long categoriaId) {
        this.id = id;
        this.nombre = nombre;
        this.precio = precio;
        this.categoriaId = categoriaId;
    }

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public Double getPrecio() { return precio; }
    public void setPrecio(Double precio) { this.precio = precio; }

    public Long getCategoriaId() { return categoriaId; }
    public void setCategoriaId(Long categoriaId) { this.categoriaId = categoriaId; }
}
```

#### Conversor de Entidad a DTO

```java
public class ProductoMapper {

    public static ProductoDTO toDTO(Producto producto) {
        return new ProductoDTO(
            producto.getId(),
            producto.getNombre(),
            producto.getPrecio(),
            producto.getCategoria() != null ? producto.getCategoria().getId() : null
        );
    }

    public static Producto toEntity(ProductoDTO productoDTO, Categoria categoria) {
        Producto producto = new Producto();
        producto.setId(productoDTO.getId());
        producto.setNombre(productoDTO.getNombre());
        producto.setPrecio(productoDTO.getPrecio());
        producto.setCategoria(categoria);
        return producto;
    }
}
```

#### Controlador usando DTOs

```java
@RestController
@RequestMapping("/api/productos")
public class ProductoController {

    @Autowired
    private ProductoRepository productoRepository;

    @Autowired
    private CategoriaRepository categoriaRepository;

    @GetMapping
    public List<ProductoDTO> obtenerProductos() {
        return productoRepository.findAll()
                .stream()
                .map(ProductoMapper::toDTO)
                .collect(Collectors.toList());
    }

    @PostMapping
    public ProductoDTO crearProducto(@RequestBody ProductoDTO productoDTO) {
        Categoria categoria = categoriaRepository.findById(productoDTO.getCategoriaId())
                                .orElseThrow(() -> new RuntimeException("Categoria no encontrada"));
        Producto producto = ProductoMapper.toEntity(productoDTO, categoria);
        Producto productoGuardado = productoRepository.save(producto);
        return ProductoMapper.toDTO(productoGuardado);
    }
}
```

### Ventajas del enfoque con DTOs

1. **Mayor control sobre los datos expuestos**: Puedes seleccionar qué información deseas exponer en la API y omitir datos innecesarios o sensibles.
2. **Código más limpio y mantenible**: El código no está sobrecargado con anotaciones para manejar la serialización y deserialización de entidades. En su lugar, los DTOs están diseñados específicamente para la API.
3. **Desacoplamiento**: La capa de persistencia (*entidades JPA*) está desacoplada de la capa de presentación (*API*), lo que permite modificar el esquema de la base de datos sin romper la API.
4. **Facilidad de pruebas**: Las pruebas de unidad y de integración se vuelven más fáciles de escribir y mantener, ya que las entidades no están directamente involucradas en la lógica de la API.

> Como puedes ver, usar DTOs en lugar de exponer directamente las entidades JPA en una API REST resulta en un código más limpio, mantenible y fácil de escalar, lo que a largo plazo facilita el mantenimiento y la evolución de tu aplicación.

Es importante recordar que no hay una solución única para todos los problemas de diseño de API REST. Cada aplicación es única y tiene sus propias necesidades y restricciones. Sin embargo, al seguir buenas prácticas como el uso de DTOs en lugar de entidades JPA, puedes construir APIs más robustas y eficientes que satisfagan las necesidades de tus clientes y de tu aplicación a largo plazo.

Es por ello que te invito a reflexionar sobre cómo estás diseñando tus APIs y considerar si el uso de DTOs podría ser beneficioso para tu caso particular. Es posible que al principio requiera un poco más de esfuerzo, pero a largo plazo, te permitirá construir APIs más flexibles, eficientes y fáciles de mantener.

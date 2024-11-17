---
title: Comparaciones Precisas para Evitar Errores con Double
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/bigdecimal-representa-monedas-double-calculos-cientificos.webp
description: Por qué usar BigDecimal en Java para realizar comparaciones precisas en cantidades monetarias. Aprende a evitar los errores de precisión comunes con double y a mejorar la exactitud en tus aplicaciones financieras con esta guía práctica.
author: Arturo López
date: 2024-11-14
label: Java
---

En este artículo, aprenderás por qué es importante usar `BigDecimal` en Java para realizar comparaciones precisas. Verás cómo evitar los errores de precisión comunes con `double` y mejorar la exactitud para evitar problemas en las validaciones de cuando se representan cantidades monetarias.

Por ejemplo si tienes dos cantidades monetarias y deseas compararlas para saber si son iguales, podrías hacer algo como esto:

```java
double cantidad1 = 112264.3501;
double cantidad2 = 112264.35010000001;

if (cantidad1 == cantidad2) {
  System.out.println("Las cantidades son iguales");
}
```

En este ejemplo es claro que las cantidades `cantidad1` y `cantidad2` son iguales, pero si ejecutas este código, verás que no imprime el mensaje "Las cantidades son iguales". Esto se debe a que los números de punto flotante, como `double`, no siempre pueden representar valores decimales de forma exacta, lo que puede llevar a errores de precisión en comparaciones directas.

> **Nota:** En este caso, `cantidad1` y `cantidad2` son `double`, que es un tipo de dato primitivo en Java para números de punto flotante. Sin embargo, al compararlos directamente, podrías obtener resultados inesperados debido a errores de precisión.

Para comparar valores `Double` en Java evitando falsos positivos debido a las diferencias en los decimales, se puede hacer uso de una tolerancia como una estrategia acertada. Esto es especialmente útil en contextos financieros, donde la precisión es crucial.

La expresión:

```java
if (Math.abs(cantidad1 - cantidad2) > 0.0001) return false;
```

Es adecuada para estos casos porque permite una diferencia mínima entre los valores antes de considerar que son distintos. Este enfoque es común para evitar problemas con la precisión de coma flotante. Vamos explicando cómo funciona y algunos ajustes para mejorar su claridad:

### Análisis de la Expresión

1. **Al usar `Math.abs`:** Esta función obtiene el valor absoluto de la diferencia entre ambos valores, permitiendo evaluar si la diferencia es lo suficientemente pequeña para ser considerada insignificante.

2. **Tolerancia epsilon (`0.0001`):** Este valor define qué tan precisos se requieren que sean los valores para que se consideren "iguales". En este caso, se ha usado una diferencia de hasta `0.0001` se considerará aceptable. Dado que los valores que estás comparando difieren solo en los decimales, esto debería evitar el falso positivo.

3. **Compatibilidad con valores `Double`:** Esta estrategia es válida y confiable al trabajar con números de punto flotante en Java, ya que `Double` a menudo presenta pequeños errores de precisión.

> El término "tolerancia epsilon" o "epsilon" se refiere a un número positivo pequeño utilizado para definir un rango de valores aceptables al comparar dos números de punto flotante. Se usa para compensar la imprecisión inherente al representar valores decimales en sistemas informáticos binarios

### Sugerencias para Mejorar el código

1. **Definir una Constante para la Tolerancia:** Definir la tolerancia como una constante puede mejorar la legibilidad y mantener el código más claro. Por ejemplo:

   ```java
   // Se define una tolerancia epsilon para comparar los valores
   private static final double TOLERANCE = 0.0001;

   if (Math.abs(cantidad1 - cantidad2) > TOLERANCE) {
       return false;
   }
   ```

   > El valor `0.0001` en la expresión se considera un número mágico, por lo que es recomendable definirlo como una constante para mejorar la legibilidad del código.

2. **Explicación de la Tolerancia:** Documentar la razón de esta tolerancia puede ayudar a futuros mantenedores del código. Puedes añadir un comentario explicativo para que otros entiendan que estás mitigando los problemas de precisión con números `Double`.

   ```java
   private static final double TOLERANCE = 0.0001;

   if (Math.abs(cantidad1 - cantidad2) > TOLERANCE) {
       return false;
   }
   ```

3. **Validación del `null`:** Si existe alguna posibilidad de que alguno de los valores sea `null`, asegúrate de verificarlo antes, para evitar excepciones de puntero nulo:

   ```java
   Double amount1 = account.getCantidad1();
   Double amount2 = account.getCantidad2();

   if (amount1 == null || amount2 == null) {
       return false; // o una lógica que maneje el caso de nulos
   }

   if (Math.abs(amount1 - amount2) > TOLERANCE) {
       return false;
   }
   ```

## ¿Porque sucede esto con `double`?

En Java, y en casi todos los lenguajes de programación, los números de tipo `double` (*punto flotante*) pueden almacenar valores muy grandes o muy pequeños, pero tienen una limitación: no siempre pueden representar los números de forma exacta. Esto se debe a cómo se almacenan internamente en binario. Los decimales (*especialmente los que resultan de operaciones matemáticas*) pueden presentar pequeños errores, por lo que los valores que a simple vista parecen iguales, en realidad pueden tener ligeras diferencias.

Imagina esto:

1. **Errores por la representación de `double`:** Cuando haces cálculos con números de punto flotante, puede que acabes con resultados que se ven iguales en papel, pero que tienen diferencias mínimas al nivel de los decimales. Por ejemplo:
   - Tienes dos valores: `112264.3501` y `112264.35010000001`. Visualmente parecen iguales, pero si los comparas con `!=`, el programa los ve como diferentes debido a la mínima diferencia.

2. **La idea de la Tolerancia:** Para solucionar esto, en lugar de comparar ambos números de forma directa (lo cual lleva a problemas por esos errores minúsculos de representación), les damos una "zona de tolerancia". Esta tolerancia es un pequeño número (en este caso `0.0001`) que indica cuánto estamos dispuestos a aceptar que los números sean diferentes sin que se consideren distintos.

3. **Cómo funciona:** Al comparar con una tolerancia, verificamos si la diferencia entre los dos números es menor que esta tolerancia. Si es así, asumimos que los números son "suficientemente iguales" para nuestros fines, incluso si no son idénticos hasta el último decimal.

## Usando Math.ulp() para la Tolerancia

Otra forma de definir la tolerancia es usando `Math.ulp()`, que devuelve la distancia entre el número de punto flotante y el siguiente número más grande. Esto es útil para establecer una tolerancia que sea significativa en el contexto de los números que estás comparando.

Por ejemplo, si quieres comparar dos números `double` con una tolerancia relativa al tamaño de los números, puedes hacer algo como esto:

```java
double cantidad1 = 112264.3501;
double cantidad2 = 112264.35010000001;

double tolerancia = Math.ulp(cantidad1);

if (Math.abs(cantidad1 - cantidad2) <= tolerancia) {
    System.out.println("Las cantidades son iguales");
}
```

### ¿Qué es Math.ulp()?

ULP significa "Unidad en el Último Lugar" (Unit in the Last Place). En términos simples, Math.ulp() te dice cuál es el siguiente número representable más cercano a un número de punto flotante dado, en su representación binaria. Es una medida de la precisión que podemos esperar de un número de punto flotante en una computadora.

#### ¿Por qué se utiliza Math.ulp()?

Como lo se ha comentado en el artículo, la aritmética de punto flotante en computadoras no es exacta debido a las limitaciones de la representación binaria de números reales. Pequeñas diferencias en los últimos dígitos de dos números pueden hacer que sean considerados diferentes, incluso si son prácticamente iguales para la mayoría de los propósitos.

Math.ulp() nos permite establecer un umbral de comparación más realista. En lugar de comparar si dos números son exactamente iguales (*lo cual es poco probable debido a los errores de redondeo*), podemos comparar si la diferencia entre ellos es menor que la precisión que podemos esperar.

### ¿Por qué se recomienda usar Math.ulp()?

- **Mayor precisión en comparaciones**: Evita falsos negativos al comparar números de punto flotante que son prácticamente iguales pero no idénticos en su representación binaria.
- **Evita problemas de redondeo**: Al considerar el ULP, se tiene en cuenta la naturaleza aproximada de la aritmética de punto flotante.
- **Mejora la robustez de los cálculos*: Hace que los cálculos numéricos sean más tolerantes a pequeños errores de redondeo.

Math.ulp() ofrece una forma más rigurosa y adaptable de comparar números de punto flotante, y es generalmente preferible a la tolerancia epsilon en la mayoría de los casos. Sin embargo, la tolerancia epsilon puede ser útil en situaciones donde se requiere un control más granular sobre el nivel de precisión.

Imagina que estás comparando dos medidas de temperatura: 25.001°C y 25.002°C. Si estableces una tolerancia epsilon de 0.001, considerarías que ambas medidas son iguales. Sin embargo, si utilizas Math.ulp(), obtendrás un umbral de comparación más preciso, que podría revelar que las medidas son ligeramente diferentes.

## Ejemplo con BigDecimal

Imagina que quieres saber si dos personas tienen el mismo peso, pero tu báscula solo tiene precisión hasta el tercer decimal. Si tienes un peso de `70.123` y otro de `70.1234`, probablemente puedas decir que ambos pesos son iguales en una comparación práctica, aunque haya una mínima diferencia. La tolerancia permite definir cuánto de esta diferencia es aceptable antes de considerarlos distintos. En programación, la tolerancia ayuda a tratar estos casos sin que los errores de precisión te causen problemas inesperados.

Sin embargo, para cantidades monetarias, **usar `BigDecimal` es definitivamente la mejor práctica** en Java, porque:

1. **Precisión Exacta:** `BigDecimal` permite una precisión exacta, ya que no usa la representación binaria de los números de punto flotante como `double`. Esto significa que puedes representar cantidades decimales sin los errores de precisión que causan los problemas en `double`.

2. **Control de Redondeo:** Con `BigDecimal`, puedes controlar de manera precisa cómo redondear los números. Esto es muy importante en contextos financieros, donde incluso un pequeño error de redondeo puede tener consecuencias. Por ejemplo, puedes decidir si redondear al centavo más cercano o si aplicar otros modos de redondeo, dependiendo de las reglas contables que necesitas seguir.

3. **Comparaciones Directas:** Con `BigDecimal`, puedes realizar comparaciones directas sin tolerancia. La clase `BigDecimal` tiene métodos como `compareTo()` que comparan valores de manera precisa y sin necesidad de una "zona de tolerancia":

   ```java
   BigDecimal valor1 = new BigDecimal("112264.3501");
   BigDecimal valor2 = new BigDecimal("112264.35010000001");

   if (valor1.compareTo(valor2) == 0) {
       // Los valores son exactamente iguales, sin necesidad de tolerancia.
   }
   ```

   En este ejemplo, `compareTo()` devuelve `0` si ambos valores son equivalentes, lo cual es ideal para comparaciones exactas sin la complejidad de manejar diferencias mínimas.

4. **Escala y Precisión:** Con `BigDecimal`, puedes definir cuántos decimales quieres manejar y con qué precisión, lo cual es ideal para aplicaciones financieras donde, por ejemplo, siempre necesitas dos decimales para centavos.

## Comparación con `double`

Mientras que `double` es rápido y eficiente en términos de rendimiento y es útil para cálculos científicos donde se toleran pequeñas imprecisiones, no es ideal para dinero. La precisión exacta de `BigDecimal` asegura que los cálculos sean correctos hasta el último centavo, lo que es crucial en cualquier contexto financiero.

En resumen, para aplicaciones financieras o cuando necesitas una precisión estricta, `BigDecimal` es la opción correcta. Te permite evitar tolerancias y trabajar con comparaciones exactas, lo que lo hace ideal para evitar errores en validaciones de cantidades monetarias.

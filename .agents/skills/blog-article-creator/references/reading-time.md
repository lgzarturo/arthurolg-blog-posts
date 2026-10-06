# Arquetipos y Presupuesto de Longitud

La longitud de un artículo la decide el **contexto del tema**, no una plantilla. Este documento define cómo elegirla, cómo justificarla en la Ficha y cómo auditarla.

---

## 1. Regla de Oro

* Si el usuario indica una duración o un arquetipo, ese es el objetivo.
* Si no, la skill **propone un arquetipo en la Ficha de Definición** y lo justifica en una línea. La longitud solo queda fijada cuando el usuario aprueba la Ficha.
* **Nunca se alarga para llegar a un número.** Si el tema se agota antes del rango, se baja de arquetipo. Si el tema pide más, se sube y se dice por qué.
* No existe un tamaño "por defecto". Si varios artículos seguidos caen en el mismo rango, revisa si de verdad el contexto lo pedía.

---

## 2. Los Cuatro Arquetipos

| Arquetipo (`--archetype`) | Palabras de prosa | Secciones `##` del cuerpo | Citas `>` | Fuentes externas (mín.) | Enlaces internos (mín.) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Nota / destello** (`nota`) | 500 – 900 | 1 – 2 | 0 – 1 | 1 | 1 |
| **Guía / reflexión** (`guia`) | 1,000 – 1,800 | 3 – 4 | 1 – 3 | 3 | 2 |
| **Análisis profundo** (`analisis`) | 2,000 – 3,200 | 4 – 6 | 2 – 4 | 5 | 3 |
| **Tutorial / investigación** (`tutorial`) | 3,500 – 5,000+ | 5 o más | 2 – 4 | 8 | 3 |

Las secciones no cuentan `## Conclusión` ni `## Referencias`, que son obligatorias en todos. Los mínimos se auditan como avisos; el validador usa estos mismos números (`ARCHETYPES` en `validate_article.py`).

En Reflexión (`label: Reflexión` o `General`), las fuentes externas solo son obligatorias si el texto cita datos, estudios o autores. Los enlaces internos siguen aplicando, pero nunca se fuerzan.

### Señales para elegir el arquetipo

Evalúa estas señales con el tema concreto y elige el arquetipo que más se ajuste:

| Señal | Empuja hacia |
| :--- | :--- |
| Una sola idea o anécdota, sin necesidad de evidencia | nota |
| Un concepto con un ejemplo, pocas afirmaciones verificables | guía |
| Varias afirmaciones que necesitan fuente, trade-offs, alternativas descartadas | análisis |
| Pasos reproducibles, código obligatorio, comparativas, varias fuentes primarias | tutorial |
| El tema ya está cubierto en el blog (ver `index_articles.py`) | bajar un nivel y enlazar al artículo existente |
| Audiencia nueva en el tema, requiere definir conceptos | subir un nivel |
| El gancho es una escena breve y el aprendizaje cabe en un párrafo | nota |

La Ficha debe incluir: arquetipo, rango de palabras y **una línea de justificación** basada en estas señales.

---

## 3. Velocidad de Lectura y Tiempo Estimado

Velocidad base para prosa técnica reflexiva en español: **200 palabras por minuto**.

$$\text{Tiempo Real (min)} = \left(\frac{\text{palabras\_prosa}}{200}\right) + (\text{bloques\_código} \times 0.33) + ((\text{imágenes} + \text{diagramas Mermaid}) \times 0.20)$$

El tiempo estimado es una métrica informativa de la Hoja de Aprobación. **No determina la longitud**; la determina el arquetipo.

---

## 4. Distribución Orientativa

Para evitar una introducción enorme con un cuerpo raquítico:

| Bloque | Proporción aproximada |
| :--- | :--- |
| Gancho / introducción | 8 – 12% |
| Cuerpo | 75 – 80% |
| Conclusión | 8 – 12% (en una nota puede ser de 2 o 3 líneas) |

---

## 5. Cómo Ganar Profundidad sin Paja

Si falta contenido para el rango del arquetipo, no repitas ni adjetives. Haz una de estas cosas:

1. Añade una **anécdota real** o un caso de producción.
2. Explica los **trade-offs** o las alternativas descartadas.
3. Incorpora un **dato verificable** con su fuente (ver `references/research.md`).
4. Incluye un **bloque de código o diagrama Mermaid** que muestre el mecanismo.
5. Desarrolla un **caso borde** y la lección que dejó.

Si ninguna aplica, el artículo ya tiene la longitud correcta: baja de arquetipo.

---

## 6. Validación

```bash
python3 .agents/skills/blog-article-creator/scripts/validate_article.py \
  --file "<ruta-al-articulo.md>" --archetype <nota|guia|analisis|tutorial> --ignore-date-today
```

* Con `--archetype`, el rango de palabras, las secciones, las citas y los mínimos de fuentes y enlaces internos se miden contra la tabla de arriba.
* Sin `--archetype`, `--reading-time N` conserva el modo legado (±25% / +30% del objetivo). `--reading-time auto` solo es diagnóstico: infiere el objetivo del propio texto y no emite avisos de longitud.

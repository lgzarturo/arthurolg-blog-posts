# Presupuesto de Longitud: Tipo, Objetivo y Partes

La longitud no se elige como bloque ni se decide a ojo: se **calcula** a partir de las secciones que el tema necesita. El arquetipo da el rango; el cálculo por secciones da la cifra. Las tablas de este documento son las constantes de `scripts/plan_length.py` (una prueba verifica que coincidan).

---

## 1. Regla de Oro

* Si el usuario indica una duración o un arquetipo, ese es el objetivo.
* Si no, se clasifica el artículo en tres ejes cerrados y se ejecuta `plan_length.py`. Su salida se pega **literal** en la Ficha.
* **Nunca se rellena ni se comprime.** Si la cifra excede lo que permite el objetivo, se sube de arquetipo (`escalated`); si queda por debajo, se baja (`descended`). En ambos casos la Ficha lleva una línea de justificación.
* La SERP ajusta la profundidad de forma cualitativa (`--serp-adjust`); nunca se copia su conteo de palabras.

---

## 2. Tres Ejes de Clasificación

* **Tipo (`--type`):** la forma del texto. Fija las palabras por parte.
* **Objetivo (`--objective`):** lo que busca el lector. Acota los arquetipos permitidos y el registro.
* **Partes (`--parts`):** entero ≥ 1, obligatorio, contado del esquema propuesto (secciones `##` del cuerpo). No tiene valor por defecto.

### Palabras por parte según tipo

| Tipo | Unidad | Rango por parte |
| :--- | :--- | :--- |
| `lista` | ítem | 100 – 220 |
| `novedades` | novedad | 120 – 250 |
| `ensayo` | movimiento | 250 – 400 |
| `perfil` | etapa | 300 – 500 |
| `comparativa` | criterio | 250 – 400 |
| `analisis` | sección | 350 – 550 |
| `postmortem` | fase | 300 – 450 |
| `tutorial` | paso | 300 – 500 (el código no cuenta) |

### Objetivo → arquetipos permitidos

| Objetivo | Permitidos | Registro |
| :--- | :--- | :--- |
| `reflexionar` | nota, guia | íntimo y narrativo |
| `estar-al-dia` | nota, guia | periodístico |
| `entender` | guia, analisis | explicativo |
| `decidir` | analisis | evaluativo, con criterios |
| `hacer` | analisis, tutorial | directo e imperativo |

---

## 3. Los Cuatro Arquetipos (rangos continuos)

| Arquetipo | Palabras de prosa | Tope intro | Conclusión | Citas `>` (máx.) | Fuentes externas (mín.) | Enlaces internos (mín.) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `nota` | 400 – 900 | 100 | 40 – 100 | 1 | 1 | 1 |
| `guia` | 900 – 1,800 | 180 | 100 – 200 | 2 | 3 | 2 |
| `analisis` | 1,800 – 3,200 | 250 | 100 – 200 | 3 | 5 | 3 |
| `tutorial` | 3,000 – sin tope | 250 | 100 – 200 | 3 | 8 | 3 |

* Las citas en bloque no tienen mínimo: un artículo sin ninguna es válido.
* La cantidad de secciones `##` no es fija: la determinan las partes. `## Conclusión` y `## Referencias` son obligatorias en todos y no cuentan como partes.
* En Reflexión (`label: Reflexión` o `General`), las fuentes externas solo son obligatorias si el texto cita datos, estudios o autores. Los enlaces internos siguen aplicando, pero nunca se fuerzan.

---

## 4. Algoritmo de `plan_length.py`

1. **Punto por parte** según `--serp-adjust`: `-1` → mínimo del rango del tipo, `0` → punto medio, `+1` → máximo.
2. `cuerpo = partes × punto`.
3. Para cada arquetipo en orden ascendente: `total = cuerpo + tope_intro + punto_medio_conclusión`; se elige el primero cuyo rango contiene su propio total. Si el total queda por debajo de 400, se asigna `nota` y la salida avisa: no se rellena, se revisa si el tema da para un artículo.
4. Se compara con los arquetipos que permite el objetivo: dentro → `status ok`; por encima → `status escalated`; por debajo → `status descended`. Los dos últimos exigen una línea de justificación en la Ficha.

```bash
python3 .agents/skills/blog-article-creator/scripts/plan_length.py \
  --type analisis --objective decidir --parts 5 --serp-adjust 0
```

Ejemplos: `lista · reflexionar · 20` → 3,600 → `tutorial` (`escalated`); `tutorial · hacer · 3` → 1,530 → `guia` (`descended`); `analisis · decidir · 4` → 2,200 → `analisis` (`ok`).

---

## 5. Velocidad de Lectura y Tiempo Estimado

Velocidad base para prosa técnica reflexiva en español: **200 palabras por minuto**.

$$\text{Tiempo Real (min)} = \left(\frac{\text{palabras\_prosa}}{200}\right) + (\text{bloques\_código} \times 0.33) + ((\text{imágenes} + \text{diagramas Mermaid}) \times 0.20)$$

El tiempo estimado es una métrica informativa de la Hoja de Aprobación. **No determina la longitud.**

---

## 6. Cómo Ganar Profundidad sin Paja

Si una sección queda corta frente a su presupuesto, no repitas ni adjetives. Haz una de estas cosas:

1. Añade una **anécdota real** o un caso de producción.
2. Explica los **trade-offs** o las alternativas descartadas.
3. Incorpora un **dato verificable** con su fuente (ver `references/research.md`).
4. Desarrolla un **caso borde** y la lección que dejó.

Si ninguna aplica, la sección ya tiene la longitud correcta: quita una parte o baja de arquetipo.

---

## 7. Validación

```bash
python3 .agents/skills/blog-article-creator/scripts/validate_article.py \
  --file "<ruta-al-articulo.md>" --type <tipo> --objective <objetivo> --visuals <N> --ignore-date-today
```

* Con `--type/--objective`, el arquetipo se deriva de las secciones `##` reales y tiene precedencia sobre `--archetype`. Avisos (nunca errores): intro por encima del tope, conclusión fuera de rango (sin contar la línea de contacto), cada `##` fuera de su rango por parte ±25% (un `##` con `###` multiplica el rango por el número de `###`), Mermaid + tablas por encima de `--visuals`, citas por encima del máximo, `tutorial` sin código y transiciones vetadas al inicio de párrafo.
* `--archetype` sin `--type` es para artículos legados: mide el rango de palabras, el máximo de citas, el código en `tutorial` y los mínimos de fuentes y enlaces.
* Sin ninguno de los dos, `--reading-time N` conserva el modo legado (±25% / +30% del objetivo). `--reading-time auto` solo es diagnóstico.

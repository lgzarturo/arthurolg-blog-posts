# Enlaces Internos y Originalidad

Cada artículo debe dialogar con el resto del blog y aportar un ángulo que el blog aún no tiene. Para ambas cosas se usa el índice local `scripts/index_articles.py`.

---

## 1. Buscar en el Índice (fase Definir)

```bash
python3 .agents/skills/blog-article-creator/scripts/index_articles.py --query "<tema y palabras clave>" --top 8
python3 .agents/skills/blog-article-creator/scripts/index_articles.py --recent 5
```

Usa el índice para dos decisiones:

1. **Guardia de originalidad.** Si un artículo existente tiene puntaje alto (> 2.0) en título o descripción, hay solapamiento. En la Ficha, propone un ángulo distinto (otra audiencia, otro problema, otra profundidad) o enlaza al existente en lugar de repetirlo. Dilo explícitamente en la Ficha.
2. **Candidatos a enlazar.** Elige de 2 a 5 artículos relacionados y anótalos en la Ficha con el motivo del enlace.

---

## 2. Patrón de URL Pública

| Ubicación del archivo | URL pública |
| :--- | :--- |
| `articles/<slug>.md` | `https://www.arthurolg.com/article/<slug>` |
| `articles/<carpeta>/<slug>.md` | `https://www.arthurolg.com/article/<carpeta>_<slug>` |

Las carpetas válidas son `programming`, `springboot-course`, `technology`, `videogames` y `marketing`. Ejemplo:
`articles/springboot-course/kotlin-springboot-4-java-25-concurrencia-postgresql.md` →
`https://www.arthurolg.com/article/springboot-course_kotlin-springboot-4-java-25-concurrencia-postgresql`.

Copia la URL desde la salida del índice; no la construyas a mano.

---

## 3. Cómo Enlazar

* **Dentro de la prosa**, con enlace contextual: la frase debe tener sentido por sí sola y el texto del enlace debe describir el destino.
  * Bien: "Ya hablé de cómo [medir el costo real por tarea](URL) antes de elegir un modelo."
  * Mal: "Lee más [aquí](URL)." o una lista de "Artículos relacionados" al final.
* **Nunca fuerces un enlace.** Si ningún artículo encaja de forma natural, enlaza menos y no inventes la conexión; el aviso del validador es solo eso, un aviso.
* **No enlaces dos veces** el mismo artículo salvo que haya una razón clara.
* **Mínimos orientativos:** `nota` 1 · `guia` 2 · `analisis` 3 · `tutorial` 3.
* Los enlaces externos y las fuentes se tratan en `references/research.md`.

---

## 4. Validación

El validador comprueba que cada enlace `https://www.arthurolg.com/article/...` apunta a un archivo existente. Un enlace interno roto es un **error** que impide `[SUCCESS]`. La cantidad mínima de enlaces es un aviso.

---

## 5. Checklist

- [ ] ¿Consulté el índice antes de proponer el ángulo?
- [ ] ¿La Ficha indica si hay solapamiento y cómo se diferencia este artículo?
- [ ] ¿Los enlaces internos están en la prosa y vienen del índice?
- [ ] ¿Cada enlace aporta algo al lector, sin forzarse?

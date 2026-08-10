---
name: blog-article-creator
description: >-
  Crea, refina y valida artículos para el blog de Arturo López con voz humana natural, tono auténtico (desarrollador, líder técnico y pensador pragmático) y control preciso del tiempo de lectura en minutos (por defecto 10 min por estándar, ~200 WPM).
metadata:
  version: 2.0.0
---

# Blog Article Creator (bac)

## Overview
Esta skill permite redactar nuevos artículos de blog o refinar borradores existentes de tecnología, programación, Spring Boot, videojuegos, marketing y reflexión personal.

El contenido generado adopta fielmente la **voz auténtica de Arturo López** (primera persona cercana, reflexiva y técnica, inspirada en los artículos reales del repositorio) y ajusta la extensión al **tiempo de lectura objetivo en minutos** definido por el usuario (**estándar por defecto: 10 minutos de lectura**, equivalente a ~2,000 palabras de prosa con alto valor técnico, ejemplos prácticos y reflexiones profundas).

## Quick Start
Cuando el usuario pida crear o refinar un artículo (ejemplo: *"escribe un artículo sobre flujos agénticos"*, *"redacta un post de 5 minutos sobre Spring Boot"* o *"crea un borrador de 10 min sobre resiliencia"*):

1. **Determina el Tiempo de Lectura Objetivo:**
   * Si el usuario especifica los minutos (ej. 5, 10, 15 min), usa esa cantidad.
   * **Si el usuario no especifica el tiempo, usa el Estándar Por Defecto: 10 minutos de lectura (~2,000 palabras de prosa).**
2. **Determina el `label` y el Directorio de Destino:** Selecciona la categoría correcta y resuelve la carpeta según la tabla de clasificación.
3. **Diseña el Presupuesto de Palabras y Esquema:** Reparte el número de palabras en introducción, cuerpo (secciones `##`) y conclusión siguiendo el manual de tiempo de lectura.
4. **Redacta con Voz Humana Natural:** Aplica el tono de Arturo López (primera persona, anécdotas, analogías del software/vida/videojuegos, citas en `>` y cero clichés de IA).
5. **Guarda el Archivo `.md`:** Escribe el contenido en la ruta adecuada dentro de `articles/`.
6. **Ejecuta la Validación Local:** Ejecuta el script de validación `validate_article.py` e itera hasta que no queden errores.

---

## 1. Control del Tiempo de Lectura (Standard: 10 min Default)

El tiempo de lectura se calcula a una velocidad base de **200 palabras por minuto (WPM)** para prosa en español reflexiva y técnica.

$$\text{palabras\_prosa\_objetivo} = \text{minutos\_lectura} \times 200$$

### Tabla de Presupuesto:
| Tiempo Solicitado | Objetivo Prosa | Rango Aceptable | Secciones (`##`) | Bloques de Código / Imágenes |
| :--- | :--- | :--- | :--- | :--- |
| 3 min | ~600 palabras | 500 – 700 págs | 2 – 3 | 1 bloque (~20s extra) |
| 5 min | ~1,000 palabras | 800 – 1,200 págs | 3 – 4 | 1–2 bloques |
| **10 min (DEFAULT)** | **~2,000 palabras** | **1,600 – 2,400 págs** | **5 – 6** | **2–4 bloques** |
| 15 min | ~3,000 palabras | 2,400 – 3,500 págs | 6 – 8 | 3–5 bloques |
| 20 min | ~4,000 palabras | 3,200 – 4,500 págs | 8 – 10 | 4–6 bloques |

*Cada bloque de código suma ~0.33 min (~20s / ~65 palabras equivalentes). Cada imagen o diagrama ASCII suma ~0.20 min (~12s).*
*Consulta la guía completa en [references/reading-time.md](references/reading-time.md).*

---

## 2. Voz, Tono y Estilo de Redacción de Arturo López

El texto debe reflejar la personalidad y visión de Arturo López (desarrollador, líder técnico, artesano del código y pensador estoico).

### Pilares del Tono:
* **Voz en Primera Persona:** Habla directamente ("Yo", "en mi día a día", "en mi experiencia", "me gusta pensar que").
* **Pragmático y Técnico pero Humano:** No es un manual universitario seco; es la reflexión de un ingeniero que ha vivido deploys a las 3 a.m., refactorizaciones difíciles y proyectos escalables.
* **Metáforas Memorables:** Emplea analogías de videojuegos (Pokémon, Age of Mythology), artes marciales o estoicismo (Marco Aurelio, dicotomía del control) para explicar conceptos de arquitectura de software o vida profesional.
* **Ritmo Respiratorio Variado:** Mezcla frases analíticas profundas con frases cortas de impacto directo. Varía el tamaño de los párrafos. Usa entre 2 y 4 citas en bloque (`>`) destacadas por artículo.

### Lista Negra de Clichés de IA (Prohibidos):
❌ *"En el vertiginoso mundo de..."* / *"En la era digital..."*
❌ *"Cabe destacar..."* / *"Cabe mencionar..."* / *"Es importante señalar..."*
❌ *"En conclusión,"* / *"En resumen,"* al inicio de la conclusión.
❌ *"Sin lugar a dudas..."*
❌ Tríologos artificiales repetidos (*"rápido, eficiente y escalable"*).
❌ Cierres genéricos tipo *"el viaje apenas comienza"*.

*Consulta la guía detallada de estilo en [references/natural-writing.md](references/natural-writing.md).*

---

## 3. Clasificación del Tema y Estructura del Archivo

### A. Frontmatter YAML Requerido
```markdown
---
title: "Título Atractivo y Directo Sin Punto Final"
image: https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/<slug-de-la-imagen>.webp
description: "Resumen SEO en 1 o 2 frases atractivas y honestas (máximo 160 caracteres)."
author: Arturo López
date: YYYY-MM-DD
label: Programación
---
```

### B. Mapeo de Categorías y Carpetas
| Label Permitido | Carpeta Destino | Temas |
| :--- | :--- | :--- |
| `Programación` | `articles/programming/` | Lenguajes, algoritmos, SQL, TDD, Clean Code, patrones. |
| `Spring Boot` o `SpringBoot` | `articles/springboot-course/` | Framework Spring Boot, Java/Kotlin, APIs escalables, JPA. |
| `Tecnología` | `articles/technology/` | Tendencias tecnológicas, IA agéntica, hardware, arquitectura. |
| `Videojuegos` | `articles/videogames/` | Reseñas, análisis de mecánicas, reflexiones sobre gaming. |
| `Marketing` | `articles/marketing/` | Estrategias de canal directo, marca personal, SEO. |
| `Reflexión` o `General` | `articles/` (Raíz) | Crecimiento personal, estoicismo, mindfulness, bienestar. |

---

## 4. Cierre Oficial del Artículo (CTA)

Todos los artículos deben incluir la firma oficial de Arturo antes de la sección de referencias:

```markdown
## Conclusión

<Reflexión final profunda que conecte con la tesis inicial sin usar "En conclusión">

¿Ya estás implementando este enfoque en tu entorno de desarrollo? Me encantaría conocer tu experiencia y los desafíos que has enfrentado. ¡Hasta la próxima línea de código! 🚀

Deja tus comentarios en el [repositorio](https://github.com/lgzarturo/arthurolg-blog-posts/issues) o en mi perfil de [X@arturolgdev](https://x.com/arturolgdev). Si te es de utilidad, una estrella en [GitHub](https://github.com/lgzarturo) es de gran ayuda o no dudes en compartir este artículo con tus colegas y amigos. ¡Gracias por leer!

## Referencias

- [Documentación / Repositorio Relevante](https://github.com/lgzarturo)
```

---

## 5. Script de Validación y Autocorrección

Tras escribir o editar el archivo markdown, ejecuta siempre la validación local:

```bash
python3 /home/alg/.gemini/config/plugins/blog-article-creator/skills/blog-article-creator/scripts/validate_article.py --file "/home/alg/GitHub/arthurolg-blog-posts/articles/<ruta_relativa>/<slug>.md" --reading-time 10
```

Si el script reporta errores o advertencias, lee los detalles en `stderr`, corrige el archivo Markdown y vuelve a validar hasta obtener `[SUCCESS]`.

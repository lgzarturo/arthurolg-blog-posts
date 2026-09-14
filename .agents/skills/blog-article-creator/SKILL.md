---
name: blog-article-creator
description: >-
  Crea, refina y valida artículos para el blog de Arturo López en español neutro
  (tuteo estándar, sin voseo ni regionalismos), con voz humana natural, tono auténtico
  (desarrollador, líder técnico y pensador pragmático), generación automatizada de
  imágenes WebP responsivas, duración dinámica, edición SEO y diagramas Mermaid
  en un flujo reproducible en tres fases: Definir, Concretar y Aprobar.
metadata:
  version: 4.0.0
---

# Blog Article Creator (bac)

## Visión General

Esta skill gobierna la creación y refinamiento de artículos para el blog de
**Arturo López** (`lgzarturo`), abarcando tecnología, programación, Spring Boot,
arquitectura de software, videojuegos, marketing y reflexión
personal/estoicismo.

Todos los artículos se redactan obligatoriamente en **español neutro** (tuteo
estándar internacional / mexicano culto: *tú*, *tienes*, *observas*, *revisa*,
*lee*). Queda **estrictamente prohibido el uso de voseo** (*tenés*, *mirá*, *vos*)
y regionalismos marcados (chilenos, rioplatenses o ibéricos), garantizando una
lectura cercana, profesional y de alcance global.

El proceso sigue un **flujo reproducible y óptimo en tres fases deterministas**:

1. **Definir:** Acordar el enfoque, duración objetivo (o calcularla desde el
   contexto), categoría, tesis, intención de búsqueda, gancho y esquema antes
   de redactar.
2. **Concretar:** Redactar con la voz auténtica de Arturo López, pasar el texto
   por una edición SEO experta, representar diagramas técnicos con Mermaid,
   generar una portada basada en el artículo y procesar las 3 versiones WebP
   responsivas (`desktop`, `tablet`, `mobile`).
3. **Aprobar:** Ejecutar la suite de validación local y presentar la Hoja de
   Aprobación con métricas, previsualización de imagen y comando de commit listo
   para publicación.

---

## Flujo de Trabajo en Tres Fases

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   1. DEFINIR    │ ───>  │  2. CONCRETAR   │ ───>  │   3. APROBAR    │
│  Ficha y Visto  │       │ Prosa + WebPs   │       │ Validación +    │
│      Bueno      │       │   Responsivos   │       │     Handoff     │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

### FASE 1: DEFINIR (Ideación y Estructura)

1. **Recepción de la Idea:**
   - Si la petición es genérica o el usuario pide ideas, consultar opcionalmente
     `ideas_to_write.md`.
   - Si la idea es abierta, proponer **2 o 3 ángulos temáticos con enfoques
     contrastados**.
2. **Ficha de Definición:** Una vez acordado el ángulo (o si el usuario ya dio
   una idea precisa), presentar la **Ficha de Definición** y detenerse a esperar
   el visto bueno del usuario:

```markdown
### 📋 Ficha de Definición del Artículo

- **Título Propuesto:** <Título atractivo y directo, sin punto final>
- **Slug:** `<slug-del-articulo>`
- **Categoría (`label`):** `Programación` | `Spring Boot` | `Tecnología` |
  `Videojuegos` | `Marketing` | `Reflexión`
- **Ruta Destino:** `articles/<categoria-path>/<slug>.md`
- **Tiempo de Lectura:** `<N> minutos` (duración indicada por el usuario o
  estimada desde la profundidad, audiencia y complejidad del tema). Incluir el
  rango de palabras objetivo; no asumir 10 minutos si no se especifica.
- **Tesis Central:** <Una oración que resuma la idea fuerza>
- **Intención de Búsqueda:** <informacional, comparativa, transaccional o navegación>
- **Keyword Principal:** <consulta natural que el lector buscaría>
- **Keywords Secundarias:** <3–6 términos semánticamente relacionados>
- **Gancho Inicial:** <Anécdota real, dilema técnico o pregunta provocadora>
- **Concepto Visual de Portada:** <escena concreta derivada de la tesis,
  audiencia, ejemplos y metáforas del artículo; no solo la categoría>
- **Esquema de Secciones:**
  - `## <Sección 1: Planteamiento del problema / Contexto>`
  - `## <Sección 2: Concepto técnico o metodológico>`
  - `## <Sección 3: Caso práctico / Código / Implementación>`
  - `<Diagrama Mermaid si mejora la comprensión de una relación, flujo o arquitectura>`
  - `## <Sección 4: Trade-offs, lecciones o aplicación>`
  - `## Conclusión` (Reflexión + CTA oficial)
  - `## Referencias`
```

> ⚠️ **Punto de Control:** No comenzar la redacción de la prosa ni la generación
> de imágenes hasta que el usuario confirme la Ficha de Definición.

---

### FASE 2: CONCRETAR (Redacción y Arte WebP Responsivo)

Una vez aprobada la Ficha de Definición:

#### A. Redacción en Prosa Auténtica

- **Editor SEO experto:** aplicar antes de aprobar el artículo un pase editorial
  sobre intención de búsqueda, título, slug, descripción de hasta 160 caracteres,
  jerarquía de encabezados, keyword principal, términos relacionados, enlaces
  internos y referencias. Optimizar sin repetir keywords artificialmente ni
  prometer algo que el artículo no explica. Seguir
  [references/seo-editor.md](references/seo-editor.md).

- **Idioma Obligatorio (Español Neutro):** Redactar **siempre en español neutro**
  con tuteo estándar (*tú*, *tienes*, *puedes*, *observas*, *revisa*, *deja*).
  Está **estrictamente prohibido el voseo** (*tenés*, *podés*, *mirá*, *hacés*,
  *para vos*, etc.) y modismos regionales (chilenos, rioplatenses, peninsulares).
  El tono es el de Arturo López (México): cercano, técnico, reflexivo y universal.
- **Voz de Arturo López:** Primera persona directa, artesano de software, líder
  técnico humilde y reflexivo. Metáforas de videojuegos (Pokémon, Age of
  Mythology), cultura pop (Spider-Man) y estoicismo (Marco Aurelio, dicotomía
  del control, actuar sin depender del resultado).
- **Ritmo y Variedad:** Alternar frases largas con sentencias breves. Incluir
  entre **2 y 4 citas en bloque (`>`)**.
- **Cero Clichés de IA:** Aplicar estrictamente la lista negra (prohibido _"en
  el vertiginoso mundo"_, _"cabe destacar"_, _"en conclusión,"_ al inicio de
  conclusión, etc.).
- **Bloques Prácticos:** Código comentado, tablas y diagramas Mermaid cuando
  aplique. Si se representa un flujo, secuencia, arquitectura, relación o ciclo,
  usar un bloque fenced `mermaid`; no usar ASCII como formato principal para
  diagramas técnicos. No añadir diagramas por decoración.
- **Cierre Oficial (CTA):**

  ```markdown
  ## Conclusión

  <Reflexión final que cierre el arco sin usar "En conclusión">

  ¿Ya estás implementando este enfoque en tu entorno de desarrollo? Me
  encantaría conocer tu experiencia y los desafíos que has enfrentado. ¡Hasta la
  próxima línea de código! 🚀

  Deja tus comentarios en el
  [repositorio](https://github.com/lgzarturo/arthurolg-blog-posts/issues) o en
  mi perfil de [X@algforge](https://x.com/algforge). Si te es de utilidad, una
  estrella en [GitHub](https://github.com/lgzarturo) es de gran ayuda o no dudes
  en compartir este artículo con tus colegas y amigos. ¡Gracias por leer!

  ## Referencias

  - [Documentación / Repositorio Relevante](https://...)
  ```

#### B. Generación y Procesamiento de la Imagen de Portada

1. Generar la imagen con la herramienta nativa `generate_image`:
   - `AspectRatio`: `"16:9"`
   - `Prompt`: Prompt en inglés construido desde la tesis, problema, audiencia,
     ejemplos y metáforas del artículo, siguiendo las pautas de
     [references/cover-images.md](references/cover-images.md). La categoría solo
     define el lenguaje visual; nunca sustituye el contexto semántico del texto.
   - `ImageName`: `<slug_resumido>`
2. Procesar a las 3 variantes WebP responsivas ejecutando el script local:
   ```bash
   python3 .agents/skills/blog-article-creator/scripts/process_article_images.py \
     --input-image "<ruta_del_png_generado>" \
     --slug "<slug-del-articulo>"
   ```
   Esto generará automáticamente:
   - `articles/images/<slug>.webp` (1920x1080)
   - `articles/images/<slug>-tablet.webp` (1024x576)
   - `articles/images/<slug>-mobile.webp` (600x338)

#### C. Creación del Archivo Markdown

Escribir el artículo en la ruta correspondiente con el frontmatter YAML
estándar:

```markdown
---
title: 'Título Atractivo Sin Punto Final'
image: 'https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/<slug>.webp'
description:
  'Descripción concisa para SEO y redes sociales (máximo 160 caracteres).'
author: 'Arturo López'
date: 'YYYY-MM-DD'
label: 'Programación'
---
```

---

### FASE 3: APROBAR (Validación Local y Handoff)

1. **Ejecución de la Suite de Validación:** Ejecutar el script de auditoría:

   ```bash
   python3 .agents/skills/blog-article-creator/scripts/validate_article.py \
     --file "articles/<categoria>/<slug>.md" \
     --reading-time <minutos-o-auto>
   ```

   _Si el script reporta errores, corregir el archivo Markdown o las imágenes
   hasta obtener `[SUCCESS]`._

2. **Presentación de la Hoja de Aprobación:** Presentar al usuario el resumen
   final con la imagen embebida y el relevo para publicación:

````markdown
### 🎯 Hoja de Aprobación del Artículo

- **Artículo:** [`<nombre-archivo.md>`](file:///<ruta_absoluta>)
- **Métricas:** ~X,XXX palabras de prosa | X.X min de lectura estimada | X
  bloques de código | X citas `>`
- **Validación:** ✅ Frontmatter, Estructura, Cero Clichés de IA y 3 WebPs
  Responsivos Verificados.

#### Portada Generada

![Portada: <slug>](ruta_al_arte_generado_o_webp)

---

#### Relevo para Publicación (Git Commit)

Puedes revisar el borrador y cuando estés listo, comitear y publicar con el
siguiente comando (según `.agents/rules/commit-style.md`):

```bash
git add articles/images/<slug>*.webp articles/<categoria>/<slug>.md
git commit -m "feat(blog): publicar articulo sobre <tema en español neutro>

- agregar articulo sobre <resumen punto 1>
- incluir imagenes responsivas en formato WebP (desktop, tablet, mobile)
- reflexionar sobre <resumen punto 2>"
```
````

```

3. **Actualización de Ideas (si aplica):**
   Si el tema provino de `ideas_to_write.md`, sugerir actualizar o tachar el tema correspondiente en dicho archivo.

---

## Mapeo de Categorías y Rutas

| Label Frontmatter | Directorio en Repositorio | Descripción / Temas |
| :--- | :--- | :--- |
| `Programación` | `articles/programming/` | Algoritmos, patrones, Clean Code, SQL, TDD, testing. |
| `Spring Boot` o `SpringBoot` | `articles/springboot-course/` | Framework Spring Boot, Java, Kotlin, microservicios, JPA. |
| `Tecnología` | `articles/technology/` | IA agéntica, herramientas de desarrollo, arquitectura moderna. |
| `Videojuegos` | `articles/videogames/` | Análisis de mecánicas, retrospectivas, narrativa gamer. |
| `Marketing` | `articles/marketing/` | Canal directo, hospitality tech, planes de lealtad. |
| `Reflexión` o `General` | `articles/` (Raíz) | Estoicismo, mentalidad, crecimiento personal, bienestar. |

---

## Documentación de Referencia

- [references/natural-writing.md](references/natural-writing.md): Manual de estilo, voz y lista negra de clichés de IA.
- [references/reading-time.md](references/reading-time.md): Presupuesto de palabras y fórmula de cálculo a 200 WPM.
- [references/cover-images.md](references/cover-images.md): Guía estética y especificaciones técnicas de portadas WebP.
- [references/seo-editor.md](references/seo-editor.md): Pase editorial experto para SEO, legibilidad e intención de búsqueda.
```

---
name: blog-article-creator
description: >-
  Crea, refina y valida artículos para el blog de Arturo López en español neutro
  (tuteo estándar, sin voseo ni regionalismos), con voz humana natural, longitud
  decidida por el contexto del tema (arquetipos), investigación con fuentes
  primarias, enlaces a otros artículos del blog, cierres propios de cada tema,
  imágenes WebP responsivas, edición SEO y diagramas Mermaid en un flujo
  reproducible: Definir, Investigar, Concretar y Aprobar.
metadata:
  version: 5.0.0
---

# Blog Article Creator (bac)

## Visión General

Esta skill gobierna la creación y refinamiento de artículos para el blog de
**Arturo López** (`lgzarturo`), abarcando tecnología, programación, Spring Boot,
arquitectura de software, videojuegos, marketing y reflexión personal.

Todos los artículos se redactan obligatoriamente en **español neutro** (tuteo
estándar internacional / mexicano culto: *tú*, *tienes*, *observas*, *revisa*,
*lee*). Queda **estrictamente prohibido el uso de voseo** (*tenés*, *mirá*, *vos*)
y regionalismos marcados (chilenos, rioplatenses o ibéricos), garantizando una
lectura cercana, profesional y de alcance global.

Principios que gobiernan todo el flujo:

- **La longitud la decide el contexto.** Cada artículo tiene un arquetipo (nota,
  guía, análisis, tutorial) elegido según el tema. Nunca se alarga para llegar a
  un número ni se parte de un tamaño por defecto.
- **Lo verificable se investiga.** Los datos se ligan a fuentes primarias y se
  citan en la prosa. Lo que no se pudo verificar se elimina o se presenta como
  opinión propia.
- **El blog dialoga consigo mismo.** Cada artículo enlaza a otros del blog cuando
  encaja, y aporta un ángulo que el blog aún no tiene.
- **El tema manda sobre la fórmula.** El tono, la cadencia y la narrativa de
  Arturo se mantienen; las analogías salen del tema y no se fuerzan (ni el
  estoicismo, ni los videojuegos).
- **Cada cierre es propio.** La conclusión termina con una idea del tema y una
  única línea constante de contacto; no hay despedida repetida.

El proceso sigue **cuatro fases con un solo punto de aprobación (la Ficha)**:

1. **Definir:** revisar el índice del blog, hacer una investigación ligera, elegir
   el arquetipo y presentar la Ficha.
2. **Investigar:** un sub-agente construye el dossier completo de fuentes.
3. **Concretar:** redactar sobre el dossier con la voz de Arturo, editar para SEO,
   representar diagramas con Mermaid, generar la portada y los 3 WebP.
4. **Aprobar:** validar con el script y presentar la Hoja de Aprobación.

---

## Flujo de Trabajo

```
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  1. DEFINIR   │ → │ 2. INVESTIGAR │ → │ 3. CONCRETAR  │ → │  4. APROBAR   │
│ Índice, tesis │   │ Sub-agente:   │   │ Prosa, enlaces│   │ Validación y  │
│ y Ficha ✋    │   │ dossier       │   │ y WebPs       │   │ Hoja          │
└───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘
        ✋ = único punto de aprobación del usuario
```

### FASE 1: DEFINIR (Contexto, Ángulo y Ficha)

1. **Recepción de la idea:**
   - Si la petición es genérica o el usuario pide ideas, consultar
     `ideas_to_write.md`.
   - Si la idea es abierta, proponer **2 o 3 ángulos con enfoques contrastados**.
2. **Revisar el blog** con el índice (ver
   [references/internal-linking.md](references/internal-linking.md)):

   ```bash
   python3 .agents/skills/blog-article-creator/scripts/index_articles.py \
     --query "<tema y palabras clave>" --top 8
   ```

   - **Guardia de originalidad:** si hay solapamiento, proponer un ángulo
     distinto o enlazar al artículo existente en vez de repetirlo.
   - **Candidatos a enlazar:** elegir de 2 a 5 artículos relacionados.
3. **Investigación ligera** (la hace la propia skill; ver
   [references/research.md](references/research.md)): pocas búsquedas con
   `WebSearch`, `WebFetch` y `Context7` para confirmar que la tesis se sostiene,
   conocer la versión o el estado actual del tema y armar el plan de fuentes.
4. **Elegir el arquetipo** con las señales de
   [references/reading-time.md](references/reading-time.md). Justificarlo en una línea.
5. **Presentar la Ficha de Definición** y detenerse a esperar el visto bueno:

```markdown
### 📋 Ficha de Definición del Artículo

- **Título Propuesto:** <Título atractivo y directo, sin punto final>
- **Slug:** `<slug-del-articulo>`
- **Categoría (`label`):** `Programación` | `Spring Boot` | `Tecnología` |
  `Videojuegos` | `Marketing` | `Reflexión`
- **Ruta Destino:** `articles/<categoria-path>/<slug>.md`
- **Arquetipo y longitud:** `nota` | `guia` | `analisis` | `tutorial` — <rango de
  palabras>. **Justificación:** <una línea basada en las señales del tema>
- **Tesis Central:** <Una oración que resuma la idea fuerza>
- **Originalidad:** <artículos del blog con ángulo cercano y cómo se diferencia
  este; o "sin solapamiento">
- **Intención de Búsqueda:** <informacional, comparativa, transaccional o navegación>
- **Keyword Principal:** <consulta natural que el lector buscaría>
- **Keywords Secundarias:** <3–6 términos semánticamente relacionados>
- **Gancho Inicial:** <Anécdota real, dilema técnico o pregunta provocadora>
- **Analogía (opcional):** <idea que salga del propio tema, o "ninguna">
- **Plan de Fuentes:** <fuentes primarias a consultar, afirmaciones que respaldan
  y mínimo del arquetipo>
- **Enlaces Internos Candidatos:** <2–5 artículos del índice, con URL y motivo>
- **Concepto Visual de Portada:** <escena concreta derivada de la tesis,
  audiencia, ejemplos y metáforas del artículo; no solo la categoría>
- **Esquema de Secciones:** <secciones `##` acordes al arquetipo, diagramas
  Mermaid si mejoran la comprensión>, `## Conclusión`, `## Referencias`
```

> ⚠️ **Punto de Control:** No lanzar la investigación completa, redactar la prosa
> ni generar imágenes hasta que el usuario apruebe la Ficha. Al aprobar, el
> usuario puede ajustar el arquetipo, los enlaces o el plan de fuentes.

---

### FASE 2: INVESTIGAR (Dossier de Fuentes)

Tras la aprobación de la Ficha, **siempre** (en todos los arquetipos) lanzar un
**sub-agente en segundo plano** con la herramienta `Agent`, usando el contrato de
[references/research.md](references/research.md). El sub-agente abre y lee las
fuentes primarias y devuelve una tabla afirmación → fuente → URL → confianza,
más lo que no pudo verificar.

- El dossier **vive solo en la conversación**; no se guarda en el repositorio.
- No redactar sobre afirmaciones que el dossier marque como no verificadas:
  eliminarlas o presentarlas como opinión propia.
- Si el dossier contradice la tesis o revela un ángulo mejor, decirlo al usuario
  antes de continuar.

---

### FASE 3: CONCRETAR (Redacción y Arte WebP Responsivo)

#### A. Redacción en Prosa Auténtica

- **Longitud:** respetar el arquetipo aprobado. Nunca rellenar; si falta
  contenido, profundizar con anécdotas, trade-offs, datos con fuente o código
  (ver `reading-time.md`, sección 5), o bajar de arquetipo.
- **Fuentes y enlaces:** citar las fuentes del dossier con enlace contextual en la
  frase que afirma el dato, y enlazar los artículos internos elegidos dentro de la
  prosa. No forzar enlaces.
- **Editor SEO experto:** aplicar antes de aprobar un pase editorial sobre
  intención de búsqueda, título, slug, descripción de hasta 160 caracteres,
  jerarquía de encabezados, keyword principal, términos relacionados, enlaces
  internos y referencias. Optimizar sin repetir keywords artificialmente ni
  prometer algo que el artículo no explica. Seguir
  [references/seo-editor.md](references/seo-editor.md).
- **Idioma Obligatorio (Español Neutro):** redactar **siempre en español neutro**
  con tuteo estándar (*tú*, *tienes*, *puedes*, *observas*, *revisa*, *deja*).
  Está **estrictamente prohibido el voseo** (*tenés*, *podés*, *mirá*, *hacés*,
  *para vos*, etc.) y los modismos regionales.
- **Voz de Arturo López:** primera persona directa, artesano de software, líder
  técnico humilde y reflexivo. El tono, el ritmo y la narrativa son los de
  siempre. Las analogías salen del tema; Pokémon, Age of Mythology, Spider-Man y
  el estoicismo son una **paleta opcional**, no un requisito (ver
  [references/natural-writing.md](references/natural-writing.md)).
- **Ritmo y Variedad:** alternar frases largas con sentencias breves. Citas en
  bloque (`>`) según el arquetipo (nota 0–1, guía 1–3, análisis y tutorial 2–4).
- **Cero Clichés de IA:** aplicar estrictamente la lista negra (prohibido _"en
  el vertiginoso mundo"_, _"cabe destacar"_, _"en conclusión,"_ al inicio de
  conclusión, etc.).
- **Bloques Prácticos:** código comentado, tablas y diagramas Mermaid cuando
  aplique. Si se representa un flujo, secuencia, arquitectura, relación o ciclo,
  usar un bloque fenced `mermaid`; no usar ASCII como formato principal para
  diagramas técnicos. No añadir diagramas por decoración.
- **Cierre:** la conclusión cierra el arco con una reflexión y termina con una
  idea o pregunta **propia del tema**, distinta a la de los últimos artículos. No
  hay despedida fija. Lo último antes de `## Referencias` es la **línea
  constante** de contacto:

  ```markdown
  ## Conclusión

  <Reflexión final propia del tema, sin "En conclusión", con una idea, reto o
  pregunta específica del artículo. En una nota puede ser de 2 o 3 líneas.>

  Si quieres comentar o compartir tu experiencia, escríbeme en [X (@algforge)](https://x.com/algforge) o abre un issue en el [repositorio](https://github.com/lgzarturo/arthurolg-blog-posts/issues). Una estrella en [GitHub](https://github.com/lgzarturo) también ayuda.

  ## Referencias

  - [Título de la fuente, Organización](https://...)
  ```

#### B. Generación y Procesamiento de la Imagen de Portada

1. Generar la imagen con la herramienta nativa `generate_image`:
   - `AspectRatio`: `"16:9"`
   - `Prompt`: prompt en inglés construido desde la tesis, problema, audiencia,
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

### FASE 4: APROBAR (Validación Local y Handoff)

1. **Ejecutar la suite de validación** con el arquetipo aprobado:

   ```bash
   python3 .agents/skills/blog-article-creator/scripts/validate_article.py \
     --file "articles/<categoria>/<slug>.md" \
     --archetype <nota|guia|analisis|tutorial> \
     --check-links
   ```

   - Los **errores** impiden `[SUCCESS]` y deben corregirse: frontmatter, clichés,
     voseo, falta de `## Conclusión` o `## Referencias`, imágenes faltantes y
     **enlaces internos rotos**.
   - Los **avisos** nunca bloquean, pero deben revisarse y justificarse o
     corregirse: longitud fuera del arquetipo, pocas fuentes o enlaces internos,
     enlace externo que no responde, fuentes solo en `## Referencias`, referencias
     genéricas propias, cierre repetido y referencias recurrentes.
   - `--check-links` hace peticiones HTTP; si un sitio bloquea bots, confirmar a
     mano.

2. **Presentar la Hoja de Aprobación** con la imagen embebida, el dossier resumido
   y el relevo para publicación:

````markdown
### 🎯 Hoja de Aprobación del Artículo

- **Artículo:** [`<nombre-archivo.md>`](file:///<ruta_absoluta>)
- **Arquetipo:** <arquetipo> | ~X,XXX palabras de prosa | X.X min de lectura
  estimada | X bloques de código | X citas `>`
- **Enlaces:** X internos, X fuentes externas
- **Validación:** ✅ Sin errores | ⚠️ <avisos pendientes y por qué se aceptan>

#### Dossier de Fuentes (resumen)

| # | Afirmación | Fuente | URL | Confianza |
|---|------------|--------|-----|-----------|
| 1 | ...        | ...    | ... | alta      |

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

3. **Actualización de Ideas (si aplica):** si el tema provino de
   `ideas_to_write.md`, sugerir actualizar o tachar el tema correspondiente.

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

- [references/reading-time.md](references/reading-time.md): Arquetipos de longitud, señales para elegirlos y mínimos por arquetipo.
- [references/research.md](references/research.md): Política de investigación, jerarquía de fuentes y contrato del sub-agente.
- [references/internal-linking.md](references/internal-linking.md): Índice del blog, patrón de URL, enlaces internos y guardia de originalidad.
- [references/natural-writing.md](references/natural-writing.md): Manual de estilo, voz, cierre y lista negra de clichés de IA.
- [references/seo-editor.md](references/seo-editor.md): Pase editorial experto para SEO, legibilidad e intención de búsqueda.
- [references/cover-images.md](references/cover-images.md): Guía estética y especificaciones técnicas de portadas WebP.
- [scripts/index_articles.py](scripts/index_articles.py): Índice y búsqueda de artículos del blog.
- [scripts/validate_article.py](scripts/validate_article.py): Suite de validación (`--archetype`, `--check-links`).

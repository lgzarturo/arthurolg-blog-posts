---
description: Flujo en 4 fases (Definir, Investigar, Concretar y Aprobar) para crear y validar un nuevo artículo para el blog de Arturo López con longitud por arquetipo, investigación con fuentes primarias, enlaces internos, edición SEO, diagramas Mermaid e imágenes WebP responsivas.
---

// turbo-all

## Flujo de Creación de Artículo

Sigue rigurosamente las 4 fases definidas en la skill `blog-article-creator`:

### Fase 1: Definir
1. Consultar el tema con el usuario (revisar `ideas_to_write.md` si se pide inspiración).
2. Si la idea es abierta, proponer 2-3 ángulos con diferentes enfoques.
3. Consultar el índice del blog para detectar solapamientos y elegir artículos relacionados:
   ```bash
   python3 .agents/skills/blog-article-creator/scripts/index_articles.py --query "<tema y palabras clave>" --top 8
   ```
4. Hacer una investigación ligera (`WebSearch`, `WebFetch`, `Context7`) para validar la tesis y armar el plan de fuentes.
5. Elegir el arquetipo de longitud (`nota`, `guia`, `analisis`, `tutorial`) según las señales del tema (ver `references/reading-time.md`) y justificarlo en una línea.
6. Presentar la **Ficha de Definición** (Título, Slug, Categoría, Arquetipo y longitud, Tesis, Originalidad, Gancho, Analogía opcional, Plan de fuentes, Enlaces internos candidatos, Concepto visual y Esquema de secciones). **Detenerse** y esperar la aprobación explícita del usuario antes de continuar.

### Fase 2: Investigar
1. Tras la aprobación, lanzar **siempre** un sub-agente en segundo plano con el contrato de `references/research.md` para construir el dossier (afirmación → fuente → URL → confianza).
2. El dossier vive solo en la conversación. Eliminar o presentar como opinión lo que no se pueda verificar.

### Fase 3: Concretar
1. Redactar el artículo completo en `articles/<categoria>/<slug>.md` con la voz auténtica de Arturo López en **español neutro obligatorio** (tuteo estándar, sin voseo ni modismos regionales, primera persona, cero clichés de IA). Respetar el arquetipo aprobado, citar las fuentes en la prosa, enlazar artículos internos del blog dentro del texto, y cerrar la conclusión con una idea propia del tema seguida de la línea constante de contacto y `## Referencias`. Aplicar además el pase editorial SEO y usar Mermaid para cualquier diagrama técnico.
2. Generar el arte visual en relación 16:9 a partir del contexto específico del artículo, siguiendo las directrices estéticas de la categoría (ver `references/cover-images.md`).
3. Ejecutar el script de procesamiento de imágenes para generar las 3 variantes WebP responsivas:
   ```bash
   python3 .agents/skills/blog-article-creator/scripts/process_article_images.py --input-image "<ruta_imagen_generada>" --slug "<slug>"
   ```

### Fase 4: Aprobar
1. Ejecutar la suite de validación:
   ```bash
   python3 .agents/skills/blog-article-creator/scripts/validate_article.py --file "articles/<categoria>/<slug>.md" --archetype <nota|guia|analisis|tutorial> --check-links
   ```
   Corregir cualquier error hasta obtener `[SUCCESS]`; revisar y justificar los avisos.
2. Presentar la **Hoja de Aprobación** al usuario con:
   - Arquetipo y métricas (palabras, tiempo de lectura, citas, enlaces internos y fuentes).
   - Tabla resumida del dossier de fuentes.
   - Previsualización del arte generado.
   - Enlace al archivo markdown listo para inspección.
   - Comando de git commit sugerido (en español neutro y formato Conventional Commits según `.agents/rules/commit-style.md`), listo para que Arturo comitee y publique por su cuenta.
3. Si el artículo provino de `ideas_to_write.md`, sugerir la actualización correspondiente.

---
description: Flujo estructurado en 3 fases (Definir, Concretar y Aprobar) para crear y validar un nuevo artículo para el blog de Arturo López con imágenes WebP responsivas.
---

// turbo-all

## Flujo de Creación de Artículo

Sigue rigurosamente las 3 fases definidas en la skill `blog-article-creator`:

### Fase 1: Definir
1. Consultar el tema con el usuario (revisar `ideas_to_write.md` si se pide inspiración).
2. Si la idea es abierta, proponer 2-3 ángulos con diferentes enfoques.
3. Presentar la **Ficha de Definición** (Título, Slug, Categoría, Duración de lectura, Tesis central, Gancho narrativo, Concepto visual y Esquema de secciones).
4. **Detenerse** y esperar la confirmación explícita del usuario antes de continuar.

### Fase 2: Concretar
1. Redactar el artículo completo en el archivo `articles/<categoria>/<slug>.md` adoptando la voz auténtica de Arturo López (primera persona, artesano del software, citas `>`, cero clichés de IA, CTA oficial en la conclusión y `## Referencias`).
2. Generar el arte visual en relación 16:9 con la herramienta `generate_image` siguiendo las directrices estéticas de la categoría (ver `references/cover-images.md`).
3. Ejecutar el script de procesamiento de imágenes para generar las 3 variantes WebP responsivas:
   ```bash
   python3 .agents/skills/blog-article-creator/scripts/process_article_images.py --input-image "<ruta_imagen_generada>" --slug "<slug>"
   ```

### Fase 3: Aprobar
1. Ejecutar la suite de validación:
   ```bash
   python3 .agents/skills/blog-article-creator/scripts/validate_article.py --file "articles/<categoria>/<slug>.md" --reading-time <minutos>
   ```
   Corregir cualquier error reportado hasta obtener `[SUCCESS]`.
2. Presentar la **Hoja de Aprobación** al usuario con:
   - Resumen de métricas (palabras, tiempo de lectura, citas).
   - Previsualización del arte generado.
   - Enlace al archivo markdown listo para inspección.
   - Comando de git commit sugerido (en español neutro y formato Conventional Commits según `.agents/rules/commit-style.md`), listo para que Arturo comitee y publique por su cuenta.
3. Si el artículo provino de `ideas_to_write.md`, sugerir la actualización correspondiente.

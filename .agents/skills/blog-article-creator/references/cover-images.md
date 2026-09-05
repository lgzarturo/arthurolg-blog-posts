# Guía Visual y Especificación de Imágenes de Portada

Este documento define los estándares artísticos, técnicos y de formato para las imágenes de portada de los artículos del blog de **Arturo López**.

---

## 1. Especificaciones Técnicas y Responsividad

Cada artículo requiere **3 versiones WebP con relación de aspecto 16:9** optimizadas para la web:

| Versión | Sufijo de Archivo | Dimensiones Exactas | Calidad WebP | Destino en Repositorio |
| :--- | :--- | :--- | :--- | :--- |
| **Desktop / Principal** | `<slug>.webp` | **1920 x 1080 px** | 88% | `articles/images/<slug>.webp` |
| **Tablet** | `<slug>-tablet.webp` | **1024 x 576 px** | 85% | `articles/images/<slug>-tablet.webp` |
| **Mobile** | `<slug>-mobile.webp` | **600 x 338 px** | 82% | `articles/images/<slug>-mobile.webp` |

### Referencia en el Frontmatter YAML
El archivo Markdown únicamente referencia la versión de escritorio en su frontmatter:
```yaml
image: "https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/<slug>.webp"
```
El motor del blog frontend resuelve automáticamente las variantes `-tablet.webp` y `-mobile.webp` según el viewport del dispositivo.

---

## 2. Pautas Estéticas por Categoría

Las portadas del blog de Arturo destacan por su elegancia visual, evitando a toda costa imágenes genéricas de banco de fotos corporativas o humanos con sonrisas falsas frente a laptops.

### A. Programación y Tecnología (`Programación`, `Tecnología`, `Spring Boot`)
* **Estilo Visual:** Render 3D conceptual isométrico o semi-cenital sobre fondo oscuro (*dark mode aesthetic*, negro mate / grafito profundo).
* **Elementos Clave:** Estructuras de vidrio translúcido brillante (*glowing glass blocks*), tuberías de datos o circuitos luminiscentes con neón (azul cian, zafiro, verde esmeralda y toques de ámbar cálido).
* **Concepto:** Representar la abstracción del tema (ej. orquestación de agentes como módulos conectados por haces de luz, microservicios como bloques hexagonales flotantes, arquitecturas resilientes).
* **Prohibido:** Texto superpuesto tipo banner ("HOW TO CODE"), personas genéricas de oficina, marcas de agua.

### B. Videojuegos (`Videojuegos`)
* **Estilo Visual:** Ilustración digital estilizada (estilo anime/manga moderno o concept art épico).
* **Elementos Clave:** Iluminación atmosférica, partículas dinámicas, composiciones inspiradas en universos narrativos (Pokémon, Age of Mythology, consolas clásicas, etc.).
* **Concepto:** Conectar la emoción gamer con la ingeniería o el aprendizaje.

### C. Reflexión y Crecimiento Personal (`Reflexión`, `General`)
* **Estilo Visual:** Fotografía artística minimalista o bodegón cálido (*fine-art still life*).
* **Elementos Clave:** Elementos naturales y contemplativos (bonsáis, piedras de río pulidas, bandejas de madera rústica, tazas de té/café humeante, cuadernos de notas antiguos, luz suave de ventana al amanecer o lámpara de papel de arroz cálida).
* **Concepto:** Serenidad, pausa consciente, resiliencia y filosofía estoica.

### D. Marketing y Estrategia (`Marketing`)
* **Estilo Visual:** Visualización 3D conceptual sofisticada (lujo minimalista, hospitalidad moderna, rutas de conversión y datos fluidos).
* **Elementos Clave:** Luces de hotel boutique, esquemas tridimensionales limpios, contrastes dorados y tonos oscuros sobrios.

---

## 3. Generación y Procesamiento Automatizado

### Paso 1: Generar la Imagen Base con `generate_image`
Usar la herramienta `generate_image` con:
- `AspectRatio`: `"16:9"`
- `ImageName`: 2-3 palabras en minúsculas con guiones bajos (ej. `isometric_agent_pipeline`)
- `Prompt`: Descripción en inglés detallada que aplique las directrices estéticas de arriba.

*Ejemplo de Prompt (Tecnología):*
> "Stunning 3D isometric render on a sleek dark metallic background. Futuristic glowing glass blocks and luminous translucent pipes pulsing with cyan and emerald neon light, representing a structured agentic workflow pipeline. Soft ambient volumetric lighting, clean tech illustration, no text, no watermark, 8k resolution concept art."

### Paso 2: Procesar a WebP Responsivo con el Script Oficial
Ejecutar el script automatizado que recorta a 16:9 exacto y exporta las 3 variantes WebP a `articles/images/`:

```bash
python3 .agents/skills/blog-article-creator/scripts/process_article_images.py \
  --input-image "<ruta_del_png_generado>" \
  --slug "<slug-del-articulo>"
```

### Paso 3: Validación Visual
El asistente debe mostrar la imagen al usuario para su aprobación dentro de la Hoja de Aprobación.

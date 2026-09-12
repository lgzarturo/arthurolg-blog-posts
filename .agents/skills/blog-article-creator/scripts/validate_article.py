#!/usr/bin/env python3
"""
Script de validación para artículos del blog de Arturo López.
Audita:
  1. Metadatos YAML del Frontmatter (campos requeridos, límites de caracteres, concordancia de ruta).
  2. Presupuesto de palabras y tiempo de lectura objetivo (WPM = 200 base).
  3. Detección estricta de clichés y muletillas de IA (Lista negra).
  4. Estructura narrativa (gancho inicial, citas '>', conclusión con CTA oficial, referencias).
  5. Existencia y dimensiones de las 3 imágenes WebP responsivas (desktop, tablet, mobile).

Uso:
  python3 validate_article.py --file articles/programming/mi-articulo.md --reading-time 10
"""

import argparse
import datetime
import os
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Mapeo oficial de categorías a directorios
CATEGORY_FOLDER_MAP = {
    "Programación": "articles/programming",
    "Spring Boot": "articles/springboot-course",
    "SpringBoot": "articles/springboot-course",
    "Tecnología": "articles/technology",
    "Videojuegos": "articles/videogames",
    "Marketing": "articles/marketing",
    "Reflexión": "articles",
    "General": "articles",
}

# Lista negra de clichés de IA
AI_CLICHES = [
    (r"\ben el vertiginoso mundo\b", "Cliché de IA: 'En el vertiginoso mundo'"),
    (r"\ben la era digital\b", "Cliché de IA: 'En la era digital'"),
    (r"\ben el mundo del desarrollo moderno\b", "Cliché de IA: 'En el mundo del desarrollo moderno'"),
    (r"\bcabe (destacar|mencionar|resaltar|señalar)\b", "Muletilla burocrática: 'Cabe destacar/mencionar/...'"),
    (r"\bes (importante|fundamental|vital|crucial) (destacar|mencionar|resaltar|señalar|notar|recordar)\b", "Muletilla de relleno: 'Es importante/fundamental destacar...'"),
    (r"^\s*(?:[-*]\s*)?(?:En conclusión|En resumen|En definitiva|Para concluir)[,:]", "Apertura genérica de conclusión. Arranca directamente con la idea."),
    (r"\bsin lugar a dudas\b", "Frase trillada: 'Sin lugar a dudas'"),
    (r"\bsin duda alguna\b", "Frase trillada: 'Sin duda alguna'"),
    (r"\bun papel fundamental\b", "Cliché de IA: 'Un papel fundamental'"),
    (r"\bpieza clave en el rompecabezas\b", "Metáfora trillada de IA"),
    (r"\bel viaje apenas comienza\b", "Cierre cliché de IA"),
    (r"\bno es una excepción\b", "Muletilla común de IA"),
    (r"\bun sinfín de\b", "Imprecisión de relleno"),
    (r"\ben última instancia\b", "Traducción mecánica de 'ultimately'"),
    (r"\btestimonio de\b", "Traducción mecánica de 'testament to'"),
    (r"\bactores clave\b", "Jerga genérica corporativa de IA"),
]

# Lista de voseo y regionalismos no permitidos (el blog exige español neutro con tuteo estándar)
VOSEO_AND_REGIONALISMS = [
    (r"\bvos\b", "Voseo no permitido: 'vos'. El blog se redacta en español neutro con tuteo estándar ('tú')."),
    (r"\bte decís a vos\b", "Voseo no permitido: 'te decís a vos' -> usar 'te dices a ti mismo'."),
    (r"\bpara vos\b", "Voseo no permitido: 'para vos' -> usar 'para ti'."),
    (r"\b(acabás|definís|pulsás|sabés|saltás|abrís|mirás|regresás|sentís|recordás|tenés|ejecutás|lanzás|cambiás|podés|intentás|descuidás|dispersás|inspeccionás|utilizás|transformás|abordás|convertís|hacés|pensás|creés)\b", "Conjugación de voseo no permitida. Usar tuteo en español neutro."),
    (r"\b(leé|utilizá|dejá|revisá|limpiá|apartá|mirá|estirá|tomá|respirá|poné|agregá|agrupá|cambiame)\b", "Imperativo de voseo no permitido. Usar imperativo en español neutro (lee, utiliza, deja, revisa, limpia, aparta, mira, estira, toma, respira, pon, agrega, agrupa, cámbiame)."),
    (r"\b(cachai|al tiro|altiro|weón|wn)\b", "Modismo chileno no permitido. El blog se redacta en español neutro."),
    (r"\b(vosotros|habéis|tenéis|hacéis|sois)\b", "Peninsularismo no permitido. Usar segunda persona neutra latinoamericana."),
]


def mask_code_blocks(text: str) -> str:
    """Reemplaza el interior de bloques de código por espacios para no alterar líneas ni posiciones."""
    def replacer(match):
        return re.sub(r"[^\n]", " ", match.group(0))

    masked = re.sub(r"```[\s\S]*?```", replacer, text)
    masked = re.sub(r"`[^`\n]+`", replacer, masked)
    return masked


def resolve_repo_root():
    curr = Path(__file__).resolve().parent
    while curr != curr.parent:
        if (curr / ".git").exists():
            return curr
        curr = curr.parent
    return Path.cwd()


def parse_frontmatter(content: str):
    """Extrae el frontmatter YAML y el cuerpo del archivo Markdown."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content

    yaml_text = match.group(1)
    body = match.group(2)

    metadata = {}
    for line in yaml_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            metadata[key] = val

    return metadata, body


def count_prose_words(body: str):
    """Cuenta palabras de prosa excluyendo bloques de código y frontmatter."""
    # Eliminar bloques de código cercados
    cleaned = re.sub(r"```[\s\S]*?```", "", body)
    # Eliminar código inline
    cleaned = re.sub(r"`[^`]+`", "", cleaned)
    # Eliminar URLs de enlaces markdown pero conservar texto del enlace
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    # Eliminar imágenes markdown
    cleaned = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", cleaned)
    # Eliminar encabezados
    cleaned = re.sub(r"^#{1,6}\s+.*$", "", cleaned, flags=re.MULTILINE)
    # Eliminar sintaxis de citas y viñetas
    cleaned = re.sub(r"^[>\-*+]\s+", "", cleaned, flags=re.MULTILINE)

    words = re.findall(r"\b[\w\u00C0-\u017F'-]+\b", cleaned)
    return len(words)


def validate_article(file_path: Path, target_reading_time: int, wpm: int = 200, ignore_date_today: bool = False):
    errors = []
    warnings = []
    info = []

    repo_root = resolve_repo_root()

    if not file_path.exists():
        return False, [f"El archivo no existe: {file_path}"], [], []

    content = file_path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content)

    if metadata is None:
        errors.append("No se encontró Frontmatter YAML válido delimitado por '---'.")
        return False, errors, warnings, info

    # 1. Validación de Frontmatter
    req_fields = ["title", "image", "description", "author", "date", "label"]
    for f in req_fields:
        if f not in metadata or not metadata[f]:
            errors.append(f"Falta el campo obligatorio en el frontmatter: '{f}'.")

    # Título
    title = metadata.get("title", "")
    if title.endswith("."):
        errors.append(f"El título '{title}' no debe terminar con punto final.")

    # Autor
    author = metadata.get("author", "")
    if "Arturo" not in author:
        warnings.append(f"El autor suele ser 'Arturo López' (actual: '{author}').")

    # Descripción (SEO)
    desc = metadata.get("description", "")
    if len(desc) > 160:
        errors.append(f"La descripción excede 160 caracteres ({len(desc)} caracteres).")
    elif len(desc) < 30 and desc:
        warnings.append(f"La descripción es muy corta ({len(desc)} caracteres).")

    # Fecha
    date_str = metadata.get("date", "")
    try:
        art_date = datetime.date.fromisoformat(date_str)
        today = datetime.date.today()
        if not ignore_date_today and art_date != today:
            warnings.append(f"La fecha del artículo ({art_date}) no coincide con la fecha de hoy ({today}). Usa --ignore-date-today si es intencional.")
    except Exception:
        errors.append(f"Formato de fecha inválido en el frontmatter: '{date_str}' (debe ser YYYY-MM-DD).")

    # Categoría y Ruta
    label = metadata.get("label", "")
    if label not in CATEGORY_FOLDER_MAP:
        errors.append(f"Categoría ('label') no reconocida: '{label}'. Valores válidos: {list(CATEGORY_FOLDER_MAP.keys())}")
    else:
        expected_folder = CATEGORY_FOLDER_MAP[label]
        # Resolver ruta relativa respecto al repo
        try:
            rel_path = file_path.resolve().relative_to(repo_root)
            parent_dir = str(rel_path.parent).replace("\\", "/")
            if expected_folder == "articles":
                if parent_dir != "articles":
                    warnings.append(f"Para el label '{label}', se esperaba guardar en 'articles/', pero está en '{parent_dir}'.")
            else:
                if not parent_dir.endswith(expected_folder):
                    warnings.append(f"Para el label '{label}', se esperaba guardar en '{expected_folder}/', pero está en '{parent_dir}'.")
        except ValueError:
            pass

    # 2. Análisis de Palabras y Tiempo de Lectura
    prose_words = count_prose_words(body)
    code_blocks = len(re.findall(r"```[\w]*\r?\n[\s\S]*?```", body))
    images_count = len(re.findall(r"!\[[^\]]*\]\([^)]+\)", body))

    calculated_reading_time = (prose_words / wpm) + (code_blocks * 0.33) + (images_count * 0.20)
    target_words = target_reading_time * wpm

    info.append(f"Palabras de prosa: {prose_words:,} | Bloques de código: {code_blocks} | Imágenes en cuerpo: {images_count}")
    info.append(f"Tiempo de lectura estimado: {calculated_reading_time:.1f} min (Objetivo: {target_reading_time} min @ {wpm} WPM)")

    min_words = int(target_words * 0.75)
    max_words = int(target_words * 1.30)
    if prose_words < min_words:
        warnings.append(f"Recuento de palabras bajo: {prose_words} palabras (recomendado mínimo {min_words} para {target_reading_time} min). Profundiza con casos reales o ejemplos técnicos sin añadir paja.")
    elif prose_words > max_words:
        warnings.append(f"Recuento de palabras elevado: {prose_words} palabras (máximo recomendado {max_words} para {target_reading_time} min).")

    # 3. Detección de Clichés de IA
    masked_body = mask_code_blocks(body)

    for pattern, msg in AI_CLICHES:
        matches = re.finditer(pattern, masked_body, flags=re.IGNORECASE | re.MULTILINE)
        for m in matches:
            line_num = body[:m.start()].count("\n") + 1
            errors.append(f"Línea {line_num}: {msg} -> encontrado '{m.group(0).strip()}'")

    # 4. Detección de Voseo y Regionalismos (Español Neutro Obligatorio)
    for pattern, msg in VOSEO_AND_REGIONALISMS:
        matches = re.finditer(pattern, masked_body, flags=re.IGNORECASE | re.MULTILINE)
        for m in matches:
            line_num = body[:m.start()].count("\n") + 1
            errors.append(f"Línea {line_num}: {msg} -> encontrado '{m.group(0).strip()}'")

    # 5. Estructura Narrativa y Formato
    # Citas en bloque (>)
    blockquotes = len(re.findall(r"^>\s+.*$", body, flags=re.MULTILINE))
    if blockquotes < 2:
        warnings.append(f"Solo se encontraron {blockquotes} citas destacadas ('>'). Se recomiendan entre 2 y 4 citas memorables.")
    else:
        info.append(f"Citas destacadas en bloque ('>'): {blockquotes}")

    # Conclusión
    if not re.search(r"^##\s+Conclusi[oó]n", body, flags=re.MULTILINE | re.IGNORECASE):
        errors.append("No se encontró la sección '## Conclusión'.")
    else:
        # Verificar firma / CTA oficial
        if "github.com/lgzarturo" not in body and "x.com/algforge" not in body:
            warnings.append("No se encontró el enlace oficial al repositorio o a X@algforge en la conclusión.")
        if "¡Hasta la próxima línea de código!" not in body and "¡Gracias por leer!" not in body:
            warnings.append("Se sugiere incluir la despedida característica de Arturo en el cierre.")

    # Referencias
    if not re.search(r"^##\s+Referencias", body, flags=re.MULTILINE | re.IGNORECASE):
        errors.append("No se encontró la sección obligatoria '## Referencias'.")

    # 5. Validación de Imágenes WebP Responsivas
    image_val = metadata.get("image", "")
    slug_match = re.search(r"([^/]+?)(?:-tablet|-mobile)?\.webp$", image_val)
    if not slug_match:
        errors.append(f"La URL de imagen en frontmatter no apunta a un archivo .webp válido: '{image_val}'")
    else:
        slug = slug_match.group(1)
        images_dir = repo_root / "articles" / "images"

        desktop_file = images_dir / f"{slug}.webp"
        tablet_file = images_dir / f"{slug}-tablet.webp"
        mobile_file = images_dir / f"{slug}-mobile.webp"

        for variant_name, img_path, min_w in [
            ("Desktop", desktop_file, 1200),
            ("Tablet", tablet_file, 800),
            ("Mobile", mobile_file, 500),
        ]:
            if not img_path.exists():
                errors.append(f"Falta la imagen {variant_name} requerida: {img_path.relative_to(repo_root)}")
            elif HAS_PIL:
                try:
                    with Image.open(img_path) as im:
                        w, h = im.size
                        ratio = w / h
                        info.append(f"Imagen {variant_name}: {img_path.name} ({w}x{h}, {ratio:.2f}:1, {img_path.stat().st_size / 1024:.1f} KB)")
                        if w < min_w:
                            warnings.append(f"La imagen {variant_name} ({img_path.name}) tiene ancho menor al recomendado ({w}px < {min_w}px).")
                except Exception as ex:
                    warnings.append(f"No se pudo leer dimensiones de {img_path.name}: {ex}")

    success = (len(errors) == 0)
    return success, errors, warnings, info


def main():
    parser = argparse.ArgumentParser(description="Validar artículos del blog de Arturo López.")
    parser.add_argument("--file", required=True, help="Ruta al archivo Markdown del artículo")
    parser.add_argument("--reading-time", type=int, default=10, help="Tiempo de lectura objetivo en minutos (por defecto: 10)")
    parser.add_argument("--wpm", type=int, default=200, help="Palabras por minuto para cálculo de prosa (por defecto: 200)")
    parser.add_argument("--ignore-date-today", action="store_true", help="No emitir advertencia si la fecha no es hoy")

    args = parser.parse_args()
    file_path = Path(args.file)

    print(f"\n🔍 Auditando artículo: {file_path.name}")
    print("=" * 60)

    success, errors, warnings, info = validate_article(
        file_path=file_path,
        target_reading_time=args.reading_time,
        wpm=args.wpm,
        ignore_date_today=args.ignore_date_today,
    )

    if info:
        print("\n📊 Métricas del Artículo:")
        for item in info:
            print(f"   ℹ️  {item}")

    if warnings:
        print("\n⚠️  Advertencias:")
        for warn in warnings:
            print(f"   🟡 {warn}")

    if errors:
        print("\n❌ Errores Críticos:")
        for err in errors:
            print(f"   🔴 {err}")
        print("\n[FAILED] El artículo contiene fallos que deben corregirse antes de aprobar.\n")
        sys.exit(1)
    else:
        print("\n🎉 [SUCCESS] ¡El artículo cumple al 100% con los estándares y lineamientos del blog!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()

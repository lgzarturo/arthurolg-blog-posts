#!/usr/bin/env python3
"""
Script para procesar imágenes de portada para el blog de Arturo López.
Toma una imagen fuente (ej. PNG generado por IA) y produce las 3 versiones
WebP responsivas con relación de aspecto 16:9 requeridas por el blog:
  - <slug>.webp        (1920x1080)
  - <slug>-tablet.webp (1024x576)
  - <slug>-mobile.webp (600x338)

Uso:
  python3 process_article_images.py --input-image /ruta/imagen.png --slug mi-articulo
"""

import argparse
import os
import sys
from pathlib import Path
from PIL import Image

TARGET_ASPECT_RATIO = 16.0 / 9.0

# Configuraciones de salida responsiva: (ancho, alto, sufijo, calidad)
SIZES = [
    (1920, 1080, "", 88),         # Desktop / Principal
    (1024, 576, "-tablet", 85),   # Tablet
    (600, 338, "-mobile", 82),    # Mobile
]


def resolve_repo_root():
    """Encuentra la raíz del repositorio buscando la carpeta .git."""
    curr = Path(__file__).resolve().parent
    while curr != curr.parent:
        if (curr / ".git").exists():
            return curr
        curr = curr.parent
    return Path.cwd()


def crop_to_aspect_ratio(img: Image.Image, aspect: float) -> Image.Image:
    """Recorta la imagen desde el centro para coincidir exactamente con el aspect ratio."""
    width, height = img.size
    current_aspect = width / height

    if abs(current_aspect - aspect) < 0.01:
        return img

    if current_aspect > aspect:
        # La imagen es más ancha de lo necesario: recortar laterales
        new_width = int(height * aspect)
        offset = (width - new_width) // 2
        return img.crop((offset, 0, offset + new_width, height))
    else:
        # La imagen es más alta de lo necesario: recortar arriba/abajo
        new_height = int(width / aspect)
        offset = (height - new_height) // 2
        return img.crop((0, offset, width, offset + new_height))


def process_images(input_path: Path, slug: str, output_dir: Path):
    if not input_path.exists():
        print(f"❌ Error: La imagen de entrada no existe: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(input_path) as orig_img:
            # Convertir a RGB si tiene canal alpha o formato indexado
            if orig_img.mode in ("RGBA", "LA", "P"):
                # Fondo oscuro elegante para preservar contraste
                rgb_img = Image.new("RGB", orig_img.size, (15, 17, 23))
                rgb_img.paste(orig_img, mask=orig_img.split()[-1] if orig_img.mode == "RGBA" else None)
            else:
                rgb_img = orig_img.convert("RGB")

            # Asegurar relación 16:9
            cropped = crop_to_aspect_ratio(rgb_img, TARGET_ASPECT_RATIO)

            created_files = []

            for width, height, suffix, quality in SIZES:
                resized = cropped.resize((width, height), Image.Resampling.LANCZOS)
                out_filename = f"{slug}{suffix}.webp"
                out_path = output_dir / out_filename

                resized.save(out_path, "WEBP", quality=quality, method=6)
                file_size_kb = out_path.stat().st_size / 1024
                created_files.append((out_filename, out_path, f"{width}x{height}", f"{file_size_kb:.1f} KB"))

            print("\n✅ Imágenes WebP generadas exitosamente:")
            for name, path, dims, size in created_files:
                print(f"   • {name:45} [{dims:9}] {size:>8} -> {path}")

            raw_url = f"https://raw.githubusercontent.com/lgzarturo/arthurolg-blog-posts/refs/heads/main/articles/images/{slug}.webp"
            print(f"\n🔗 URL para Frontmatter YAML:\nimage: \"{raw_url}\"\n")
            return created_files

    except Exception as e:
        print(f"❌ Error al procesar imagen: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Procesar imágenes WebP responsivas para el blog.")
    parser.add_argument("--input-image", required=True, help="Ruta de la imagen de entrada (PNG, JPG, etc.)")
    parser.add_argument("--slug", required=True, help="Slug del artículo (nombre base del archivo sin extensión)")
    parser.add_argument("--output-dir", default=None, help="Directorio de destino (por defecto: articles/images en la raíz del repo)")

    args = parser.parse_args()

    repo_root = resolve_repo_root()
    output_dir = Path(args.output_dir) if args.output_dir else (repo_root / "articles" / "images")

    process_images(Path(args.input_image), args.slug, output_dir)


if __name__ == "__main__":
    main()

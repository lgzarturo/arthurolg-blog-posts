#!/usr/bin/env python3
"""
Script de validación para artículos del blog de Arturo López.
Audita:
  1. Metadatos YAML del Frontmatter (campos requeridos, límites de caracteres, concordancia de ruta).
  2. Presupuesto de palabras y tiempo de lectura objetivo (WPM = 200 base).
  3. Detección estricta de clichés y muletillas de IA (Lista negra).
  4. Estructura narrativa escalada por arquetipo (secciones, citas '>', conclusión, referencias).
  5. Existencia y dimensiones de las 3 imágenes WebP responsivas (desktop, tablet, mobile).
  6. Investigación y enlaces: fuentes externas, enlaces internos que existan, referencias genéricas.
  7. Originalidad frente a los últimos artículos: cierres repetidos y referencias recurrentes.

Uso:
  python3 validate_article.py --file articles/programming/mi-articulo.md --archetype analisis
  python3 validate_article.py --file articles/programming/mi-articulo.md --archetype guia --check-links
  python3 validate_article.py --file articles/programming/mi-articulo.md --reading-time 7   # modo legado
"""

import argparse
import datetime
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import index_articles  # noqa: E402  (índice compartido: URLs públicas y resolución de enlaces internos)

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


# Arquetipos: rango de palabras de prosa, estructura esperada y mínimos de investigación.
# max_words=None significa sin límite superior.
ARCHETYPES = {
    "nota": {
        "name": "Nota / destello", "min_words": 500, "max_words": 900,
        "sections": (1, 2), "quotes": (0, 1), "sources": 1, "internal": 1, "needs_code": False,
    },
    "guia": {
        "name": "Guía / reflexión", "min_words": 1000, "max_words": 1800,
        "sections": (3, 4), "quotes": (1, 3), "sources": 3, "internal": 2, "needs_code": False,
    },
    "analisis": {
        "name": "Análisis profundo", "min_words": 2000, "max_words": 3200,
        "sections": (4, 6), "quotes": (2, 4), "sources": 5, "internal": 3, "needs_code": False,
    },
    "tutorial": {
        "name": "Tutorial / investigación", "min_words": 3500, "max_words": None,
        "sections": (5, None), "quotes": (2, 4), "sources": 8, "internal": 3, "needs_code": True,
    },
}

# Labels en los que las fuentes externas solo son obligatorias si el texto cita datos, estudios o autores.
REFLECTIVE_LABELS = {"Reflexión", "General"}

# Referencias recurrentes (paleta opcional): se avisa si dominan los últimos artículos.
RECURRING_REFERENCES = {
    "Pokémon": r"\bpok[eé]mon\b|\bpok[eé]dex\b",
    "Age of Mythology": r"\bage of mythology\b",
    "Spider-Man": r"\bspider-?man\b",
    "Estoicismo": r"\bestoic\w*|\bmarco aurelio\b|\bepicteto\b|\bs[eé]neca\b",
    "Dark Souls": r"\bdark souls\b",
}
RECURRING_WINDOW = 5      # últimos N artículos (incluido el actual)
RECURRING_THRESHOLD = 3   # apariciones dentro de esa ventana para avisar
CLOSING_WINDOW = 3        # cierres de los últimos N artículos contra los que se compara
CLOSING_MIN_WORDS = 6     # una oración repetida debe tener al menos estas palabras

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((https?://[^)\s]+)\)")
SOCIAL_SIGNATURE = ("x.com/algforge", "github.com/lgzarturo", "raw.githubusercontent.com/lgzarturo")
GENERIC_OWN_REFS = ("github.com/lgzarturo", "lgzarturo.com", "arthurolg.com")


def split_sections(body: str) -> dict:
    """Devuelve {'conclusion': str, 'referencias': str, 'cuerpo': str} usando los encabezados ##."""
    conc = re.search(r"^##\s+Conclusi[oó]n[^\n]*\n", body, flags=re.MULTILINE | re.IGNORECASE)
    refs = re.search(r"^##\s+Referencias[^\n]*\n", body, flags=re.MULTILINE | re.IGNORECASE)
    cuerpo_end = min([m.start() for m in (conc, refs) if m] or [len(body)])
    conclusion = ""
    if conc:
        end = refs.start() if refs and refs.start() > conc.end() else len(body)
        conclusion = body[conc.end():end]
    referencias = body[refs.end():] if refs else ""
    return {"conclusion": conclusion, "referencias": referencias, "cuerpo": body[:cuerpo_end]}


def closing_sentences(conclusion: str) -> set:
    """Oraciones del cierre sin la línea constante de enlaces; normalizadas para comparar."""
    sentences = set()
    for paragraph in re.split(r"\n\s*\n", conclusion):
        if any(sig in paragraph for sig in SOCIAL_SIGNATURE):
            continue
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", paragraph)
        for sentence in re.split(r"(?<=[.!?¡¿])\s+", text):
            norm = " ".join(index_articles.tokenize_all(sentence))
            if len(norm.split()) >= CLOSING_MIN_WORDS:
                sentences.add(norm)
    return sentences


def previous_articles(repo_root: Path, current: Path, current_date: str, limit: int) -> list:
    """Artículos más recientes (por fecha) anteriores o iguales al actual, excluyendo el propio archivo."""
    entries = index_articles.load_index(repo_root)
    cur_rel = None
    try:
        cur_rel = str(current.resolve().relative_to(repo_root)).replace("\\", "/")
    except ValueError:
        pass
    candidates = [e for e in entries if e["path"] != cur_rel and e["date"]]
    if current_date:
        candidates = [e for e in candidates if e["date"] <= current_date]
    candidates.sort(key=lambda e: e["date"], reverse=True)
    return candidates[:limit]


def check_external_link(url: str, timeout: int = 8):
    """Devuelve (ok, detalle). Intenta HEAD y cae a GET; algunos sitios bloquean bots, por eso solo avisa."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; blog-article-validator/5.0)"}
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status < 400:
                    return True, str(resp.status)
        except urllib.error.HTTPError as ex:
            if method == "GET" or ex.code not in (403, 405, 429, 501):
                return False, f"HTTP {ex.code}"
        except Exception as ex:  # DNS, timeout, SSL...
            if method == "GET":
                return False, type(ex).__name__
    return False, "sin respuesta"


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


def validate_article(file_path: Path, target_reading_time, wpm: int = 200, ignore_date_today: bool = False,
                     archetype: str = None, check_links: bool = False):
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
    all_code_blocks = len(re.findall(r"```[\w]*\r?\n[\s\S]*?```", body))
    mermaid_blocks = len(re.findall(r"```mermaid\r?\n[\s\S]*?```", body, flags=re.IGNORECASE))
    code_blocks = all_code_blocks - mermaid_blocks
    images_count = len(re.findall(r"!\[[^\]]*\]\([^)]+\)", body))

    calculated_reading_time = (prose_words / wpm) + (code_blocks * 0.33) + ((images_count + mermaid_blocks) * 0.20)
    reading_time_was_auto = target_reading_time == "auto"
    if target_reading_time == "auto":
        # Auto sirve para artículos cuya duración fue calculada desde el contenido.
        # Se redondea a una cifra útil, sin reintroducir un valor fijo de 10 minutos.
        target_reading_time = max(1, round(calculated_reading_time))
        if not archetype:
            info.append(f"Objetivo dinámico inferido desde el contenido: {target_reading_time} min")
    target_words = target_reading_time * wpm

    info.append(f"Palabras de prosa: {prose_words:,} | Bloques de código: {code_blocks} | Diagramas Mermaid: {mermaid_blocks} | Imágenes en cuerpo: {images_count}")
    arch = ARCHETYPES.get(archetype) if archetype else None
    if arch:
        upper = f"{arch['max_words']:,}" if arch["max_words"] else "sin límite"
        info.append(f"Arquetipo: {arch['name']} (rango {arch['min_words']:,}–{upper} palabras) | Tiempo de lectura estimado: {calculated_reading_time:.1f} min")
        if prose_words < arch["min_words"]:
            warnings.append(f"Recuento de palabras bajo para '{arch['name']}': {prose_words:,} (mínimo {arch['min_words']:,}). Profundiza con casos reales, trade-offs o ejemplos; si el tema no da más, considera un arquetipo menor.")
        elif arch["max_words"] and prose_words > arch["max_words"]:
            warnings.append(f"Recuento de palabras alto para '{arch['name']}': {prose_words:,} (máximo {arch['max_words']:,}). Recorta o considera un arquetipo mayor.")
    else:
        info.append(f"Tiempo de lectura estimado: {calculated_reading_time:.1f} min (Objetivo: {target_reading_time} min @ {wpm} WPM)")
        if reading_time_was_auto:
            info.append("Sin --archetype: el objetivo 'auto' se infiere del propio texto y no emite avisos de longitud. Usa --archetype para validar el rango.")
        else:
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

    # 5. Estructura Narrativa y Formato (escalada por arquetipo)
    sections = split_sections(body)

    # Secciones ## del cuerpo (sin Conclusión ni Referencias)
    body_sections = len(re.findall(r"^##\s+", mask_code_blocks(sections["cuerpo"]), flags=re.MULTILINE))
    # Citas en bloque: cuenta bloques contiguos, no líneas
    blockquotes = len(re.findall(r"(?:^>[^\n]*\n?)+", mask_code_blocks(body), flags=re.MULTILINE))
    if arch:
        lo, hi = arch["sections"]
        if body_sections < lo or (hi is not None and body_sections > hi):
            rng = f"{lo}+" if hi is None else f"{lo}–{hi}"
            warnings.append(f"Secciones '##' del cuerpo: {body_sections} (esperado {rng} para '{arch['name']}', sin contar Conclusión ni Referencias).")
        qlo, qhi = arch["quotes"]
        if blockquotes < qlo or blockquotes > qhi:
            warnings.append(f"Citas en bloque ('>'): {blockquotes} (esperado {qlo}–{qhi} para '{arch['name']}').")
        else:
            info.append(f"Citas destacadas en bloque ('>'): {blockquotes} | Secciones '##' del cuerpo: {body_sections}")
        if arch["needs_code"] and code_blocks == 0:
            warnings.append(f"'{arch['name']}' espera al menos un bloque de código; no se encontró ninguno.")
    else:
        info.append(f"Citas destacadas en bloque ('>'): {blockquotes} | Secciones '##' del cuerpo: {body_sections}")

    # Conclusión
    if not re.search(r"^##\s+Conclusi[oó]n", body, flags=re.MULTILINE | re.IGNORECASE):
        errors.append("No se encontró la sección '## Conclusión'.")
    else:
        # Línea constante: enlaces a X y GitHub dentro de la conclusión (no se exige ninguna frase de despedida)
        conclusion = sections["conclusion"]
        if "x.com/algforge" not in conclusion or "github.com/lgzarturo" not in conclusion:
            warnings.append("La conclusión debe cerrar con la línea constante con enlaces a x.com/algforge y github.com/lgzarturo.")

    # Referencias
    if not re.search(r"^##\s+Referencias", body, flags=re.MULTILINE | re.IGNORECASE):
        errors.append("No se encontró la sección obligatoria '## Referencias'.")

    # 6. Investigación y enlaces
    all_links = list(dict.fromkeys(LINK_RE.findall(mask_code_blocks(body))))
    internal_links = [u for u in all_links if u.startswith(index_articles.SITE_BASE)]
    external_links = [
        u for u in all_links
        if not u.startswith(index_articles.SITE_BASE) and not any(sig in u for sig in SOCIAL_SIGNATURE)
        and u.rstrip("/") not in ("https://www.arthurolg.com", "https://arthurolg.com")
    ]
    sources = [u for u in external_links if not any(g in u for g in GENERIC_OWN_REFS)]

    self_rel = None
    try:
        self_rel = file_path.resolve().relative_to(repo_root)
    except ValueError:
        pass
    for url in internal_links:
        target = index_articles.url_to_path(url, repo_root)
        if target is None:
            errors.append(f"Enlace interno roto: {url} no corresponde a ningún artículo (patrón: /article/<slug> o /article/<carpeta>_<slug>).")
        elif self_rel is not None and target.resolve() == file_path.resolve():
            warnings.append(f"El artículo se enlaza a sí mismo: {url}")

    is_reflective = label in REFLECTIVE_LABELS
    info.append(f"Enlaces internos: {len(internal_links)} | Fuentes externas: {len(sources)}")
    if arch:
        if len(internal_links) < arch["internal"]:
            warnings.append(f"Enlaces internos: {len(internal_links)} (mínimo {arch['internal']} para '{arch['name']}'). Usa index_articles.py --query para encontrar candidatos; no fuerces uno que no encaje.")
        if len(sources) < arch["sources"]:
            if is_reflective and len(sources) == 0:
                info.append("Reflexión sin fuentes externas: válido solo si el texto no cita datos, estudios ni autores.")
            else:
                warnings.append(f"Fuentes externas: {len(sources)} (mínimo {arch['sources']} para '{arch['name']}'). Prefiere fuentes primarias.")

    refs_links = [u for u in LINK_RE.findall(sections["referencias"])]
    if refs_links and all(any(g in u for g in GENERIC_OWN_REFS) for u in refs_links):
        warnings.append("Las referencias son solo enlaces genéricos propios (github.com/lgzarturo, arthurolg.com). Cita fuentes que respalden el contenido.")
    body_external = [u for u in LINK_RE.findall(mask_code_blocks(sections["cuerpo"])) if u in sources]
    if sources and not body_external and archetype != "nota":
        warnings.append("Las fuentes aparecen solo en '## Referencias'. Cítalas también dentro de la prosa con enlace contextual.")

    if check_links:
        for url in sources:
            ok, detail = check_external_link(url)
            if not ok:
                warnings.append(f"Enlace externo no verificable ({detail}): {url} (algunos sitios bloquean bots; confirma a mano).")
        info.append(f"Enlaces externos comprobados por HTTP: {len(sources)}")

    # 7. Originalidad frente a los últimos artículos
    previous = previous_articles(repo_root, file_path, metadata.get("date", ""), max(CLOSING_WINDOW, RECURRING_WINDOW - 1))
    if previous:
        mine = closing_sentences(sections["conclusion"])
        for prev in previous[:CLOSING_WINDOW]:
            prev_closing = closing_sentences(split_sections(prev["body"])["conclusion"])
            shared = mine & prev_closing
            if shared:
                warnings.append(f"Cierre repetido: una oración de la conclusión coincide con la de '{prev['title']}' -> '{sorted(shared)[0][:80]}...'. Escribe un cierre propio del tema.")
        recent = previous[:RECURRING_WINDOW - 1]
        for ref_name, pattern in RECURRING_REFERENCES.items():
            if not re.search(pattern, mask_code_blocks(body), flags=re.IGNORECASE):
                continue
            count = 1 + sum(1 for prev in recent if re.search(pattern, prev["body"], flags=re.IGNORECASE))
            if count >= RECURRING_THRESHOLD:
                warnings.append(f"Referencia recurrente: '{ref_name}' aparece en {count} de los últimos {len(recent) + 1} artículos. Busca una analogía que salga del propio tema.")

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
    parser.add_argument("--archetype", choices=sorted(ARCHETYPES), help="Arquetipo aprobado en la Ficha: nota | guia | analisis | tutorial (define rangos y mínimos)")
    parser.add_argument("--check-links", action="store_true", help="Comprobar por HTTP las fuentes externas (avisa, no bloquea)")
    parser.add_argument("--reading-time", default="auto", help="Modo legado: minutos objetivo, o 'auto' (solo diagnóstico). Con --archetype se ignora para longitud")
    parser.add_argument("--wpm", type=int, default=200, help="Palabras por minuto para cálculo de prosa (por defecto: 200)")
    parser.add_argument("--ignore-date-today", action="store_true", help="No emitir advertencia si la fecha no es hoy")

    args = parser.parse_args()
    if args.reading_time != "auto":
        try:
            args.reading_time = int(args.reading_time)
            if args.reading_time <= 0:
                raise ValueError
        except ValueError:
            parser.error("--reading-time debe ser un entero positivo o 'auto'")
    file_path = Path(args.file)

    print(f"\n🔍 Auditando artículo: {file_path.name}")
    print("=" * 60)

    success, errors, warnings, info = validate_article(
        file_path=file_path,
        target_reading_time=args.reading_time,
        wpm=args.wpm,
        ignore_date_today=args.ignore_date_today,
        archetype=args.archetype,
        check_links=args.check_links,
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

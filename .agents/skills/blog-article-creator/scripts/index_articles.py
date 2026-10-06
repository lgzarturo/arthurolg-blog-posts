#!/usr/bin/env python3
"""
Índice de artículos del blog de Arturo López.

Sirve para dos cosas en la fase Definir:
  1. Detectar solapamiento de ángulo con artículos ya publicados.
  2. Elegir de 2 a 5 artículos relacionados para enlazar dentro de la prosa.

También expone utilidades que reutiliza validate_article.py (URL pública,
resolución de enlaces internos, últimos artículos por fecha).

Uso:
  python3 index_articles.py --query "java concurrencia virtual threads"
  python3 index_articles.py --query "liderazgo técnico" --top 8 --label Programación
  python3 index_articles.py --recent 5
  python3 index_articles.py --list --json
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SITE_BASE = "https://www.arthurolg.com/article/"
EXCLUDED_DIRS = {"images", "resources"}
EXCLUDED_FILES = {"hello-world.md"}

STOPWORDS = {
    "a", "al", "algo", "como", "con", "cual", "cuando", "de", "del", "desde", "donde", "el", "ella",
    "en", "entre", "era", "es", "esa", "ese", "eso", "esta", "este", "esto", "la", "las", "le", "lo",
    "los", "mas", "me", "mi", "muy", "no", "nos", "o", "para", "pero", "por", "que", "se", "si", "sin",
    "sobre", "su", "sus", "te", "tu", "tus", "un", "una", "uno", "unos", "unas", "y", "ya", "hay",
    "son", "ser", "mis", "has", "han", "he", "tiene", "tienes", "puedes", "puede", "hacer", "cada",
}


def resolve_repo_root() -> Path:
    curr = Path(__file__).resolve().parent
    while curr != curr.parent:
        if (curr / ".git").exists():
            return curr
        curr = curr.parent
    return Path.cwd()


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def tokenize(text: str) -> list:
    words = re.findall(r"[a-z0-9]+", normalize(text))
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]


def tokenize_all(text: str) -> list:
    """Tokeniza sin filtrar stopwords; sirve para comparar oraciones textualmente."""
    return re.findall(r"[a-z0-9]+", normalize(text))


def parse_frontmatter(content: str):
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    metadata = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip().strip('"').strip("'")
    return metadata, match.group(2)


def public_url(rel_path: Path) -> str:
    """articles/<slug>.md -> /article/<slug> ; articles/<carpeta>/<slug>.md -> /article/<carpeta>_<slug>"""
    parts = rel_path.with_suffix("").parts[1:]  # quitar 'articles'
    return SITE_BASE + "_".join(parts)


def url_to_path(url: str, repo_root: Path):
    """Resuelve una URL pública del blog al archivo Markdown correspondiente, o None si no existe."""
    if not url.startswith(SITE_BASE):
        return None
    ident = url[len(SITE_BASE):].split("#")[0].split("?")[0].rstrip("/")
    if not ident:
        return None
    articles_dir = repo_root / "articles"
    root_candidate = articles_dir / f"{ident}.md"
    if root_candidate.exists():
        return root_candidate
    if "_" in ident:
        folder, slug = ident.split("_", 1)
        candidate = articles_dir / folder / f"{slug}.md"
        if candidate.exists():
            return candidate
    return None


def load_index(repo_root: Path) -> list:
    articles_dir = repo_root / "articles"
    entries = []
    for path in sorted(articles_dir.rglob("*.md")):
        rel = path.relative_to(repo_root)
        if any(part in EXCLUDED_DIRS for part in rel.parts) or path.name in EXCLUDED_FILES:
            continue
        content = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        if not meta.get("title"):
            continue
        no_code = re.sub(r"```[\s\S]*?```", "", body)
        headings = re.findall(r"^#{2,3}\s+(.+)$", no_code, flags=re.MULTILINE)
        entries.append({
            "path": str(rel).replace("\\", "/"),
            "url": public_url(rel),
            "title": meta.get("title", ""),
            "description": meta.get("description", ""),
            "label": meta.get("label", ""),
            "date": meta.get("date", ""),
            "headings": headings,
            "body": no_code,
        })
    return entries


def score(entry: dict, query_tokens: list) -> float:
    if not query_tokens:
        return 0.0
    title_t = set(tokenize(entry["title"] + " " + Path(entry["path"]).stem.replace("-", " ")))
    desc_t = set(tokenize(entry["description"]))
    head_t = set(tokenize(" ".join(entry["headings"])))
    body_t = tokenize(entry["body"])
    body_set = set(body_t)
    total = 0.0
    for tok in set(query_tokens):
        if tok in title_t:
            total += 3.0
        if tok in desc_t:
            total += 2.0
        if tok in head_t:
            total += 1.5
        if tok in body_set:
            total += 0.5 + min(body_t.count(tok), 10) * 0.05
    return total / max(len(set(query_tokens)), 1)


def search(entries: list, query: str, top: int, label: str = None) -> list:
    tokens = tokenize(query)
    ranked = []
    for entry in entries:
        if label and entry["label"] != label:
            continue
        s = score(entry, tokens)
        if s > 0:
            ranked.append((s, entry))
    ranked.sort(key=lambda x: -x[0])
    return ranked[:top]


def recent(entries: list, n: int) -> list:
    dated = [e for e in entries if e["date"]]
    dated.sort(key=lambda e: e["date"], reverse=True)
    return dated[:n]


def strip_body(entry: dict) -> dict:
    return {k: v for k, v in entry.items() if k != "body"}


def main():
    parser = argparse.ArgumentParser(description="Índice y búsqueda de artículos del blog.")
    parser.add_argument("--query", help="Tema o palabras clave para buscar artículos relacionados o solapados")
    parser.add_argument("--top", type=int, default=6, help="Cantidad de resultados (por defecto: 6)")
    parser.add_argument("--label", help="Filtrar por label (Programación, Tecnología, ...)")
    parser.add_argument("--recent", type=int, help="Mostrar los N artículos más recientes por fecha")
    parser.add_argument("--list", action="store_true", help="Listar todo el índice")
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    args = parser.parse_args()

    entries = load_index(resolve_repo_root())

    if args.query:
        results = [(round(s, 2), strip_body(e)) for s, e in search(entries, args.query, args.top, args.label)]
        if args.json:
            print(json.dumps([{"score": s, **e} for s, e in results], ensure_ascii=False, indent=2))
            return
        if not results:
            print("Sin coincidencias: no hay solapamiento ni enlaces internos obvios.")
            return
        print(f"Coincidencias para: {args.query!r}\n")
        for s, e in results:
            print(f"[{s:.2f}] {e['title']}  ({e['label']}, {e['date']})")
            print(f"        {e['url']}")
            print(f"        {e['description'][:140]}")
        print("\nPuntaje alto (>2.0) en título o descripción: posible solapamiento; replantea el ángulo o enlaza.")
        return

    selected = recent(entries, args.recent) if args.recent else entries
    if args.json:
        print(json.dumps([strip_body(e) for e in selected], ensure_ascii=False, indent=2))
        return
    for e in selected:
        print(f"{e['date']}  [{e['label']}]  {e['title']}\n            {e['url']}")
    print(f"\nTotal: {len(selected)} artículo(s)")


if __name__ == "__main__":
    main()

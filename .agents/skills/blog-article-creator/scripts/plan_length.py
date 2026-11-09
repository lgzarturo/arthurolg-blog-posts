#!/usr/bin/env python3
"""
Presupuesto de longitud de un artículo del blog de Arturo López.

Calcula la cifra de palabras de prosa a partir de tres ejes cerrados:
  - tipo (qué forma tiene el texto) -> palabras por parte,
  - objetivo (qué busca el lector) -> arquetipos permitidos y registro,
  - partes (cuántas secciones '##' tiene el esquema).

El arquetipo se elige por la cifra, no por la intuición. Si la cifra no cabe en lo
que permite el objetivo, se conserva y el estado lo dice (escalated / descended):
la Ficha exige justificarlo en una línea. Nunca se rellena ni se comprime.

Uso:
  python3 plan_length.py --type analisis --objective decidir --parts 5
  python3 plan_length.py --type lista --objective reflexionar --parts 7 --serp-adjust -1
"""

import argparse
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Arquetipos en orden ascendente. max_words=None significa sin tope.
ARCHETYPES = {
    "nota": {"min_words": 400, "max_words": 900, "intro_max": 100, "conclusion": (40, 100), "quotes_max": 1},
    "guia": {"min_words": 900, "max_words": 1800, "intro_max": 180, "conclusion": (100, 200), "quotes_max": 2},
    "analisis": {"min_words": 1800, "max_words": 3200, "intro_max": 250, "conclusion": (100, 200), "quotes_max": 3},
    "tutorial": {"min_words": 3000, "max_words": None, "intro_max": 250, "conclusion": (100, 200), "quotes_max": 3},
}
ORDER = list(ARCHETYPES)

# Objetivo -> (arquetipos permitidos, registro)
OBJECTIVES = {
    "reflexionar": (("nota", "guia"), "íntimo y narrativo"),
    "estar-al-dia": (("nota", "guia"), "periodístico"),
    "entender": (("guia", "analisis"), "explicativo"),
    "decidir": (("analisis",), "evaluativo, con criterios"),
    "hacer": (("analisis", "tutorial"), "directo e imperativo"),
}

# Tipo -> (unidad, palabras mínimas por parte, palabras máximas por parte)
PARTS = {
    "lista": ("ítem", 100, 220),
    "novedades": ("novedad", 120, 250),
    "ensayo": ("movimiento", 250, 400),
    "perfil": ("etapa", 300, 500),
    "comparativa": ("criterio", 250, 400),
    "analisis": ("sección", 350, 550),
    "postmortem": ("fase", 300, 450),
    "tutorial": ("paso", 300, 500),
}


def _midpoint(lo: int, hi: int) -> int:
    return (lo + hi) // 2


def section_range(type_: str, subsections: int) -> tuple:
    """Rango de palabras de un '##' del cuerpo; un '##' con N '###' vale N partes."""
    _, lo, hi = PARTS[type_]
    factor = max(1, subsections)
    return lo * factor, hi * factor


def plan(type_: str, objective: str, parts: int, serp_adjust: int = 0) -> dict:
    if parts < 1:
        raise ValueError("parts debe ser un entero >= 1")
    unit, lo, hi = PARTS[type_]
    per_part = {-1: lo, 0: _midpoint(lo, hi), 1: hi}[serp_adjust]
    body = parts * per_part

    archetype, total = None, None
    for name in ORDER:
        arch = ARCHETYPES[name]
        candidate = body + arch["intro_max"] + _midpoint(*arch["conclusion"])
        if candidate >= arch["min_words"] and (arch["max_words"] is None or candidate <= arch["max_words"]):
            archetype, total = name, candidate
            break
    below_minimum = archetype is None  # solo ocurre por debajo del mínimo de 'nota'
    if below_minimum:
        archetype = ORDER[0]
        arch = ARCHETYPES[archetype]
        total = body + arch["intro_max"] + _midpoint(*arch["conclusion"])

    allowed, register = OBJECTIVES[objective]
    position = ORDER.index(archetype)
    if archetype in allowed:
        status = "ok"
    elif position > max(ORDER.index(a) for a in allowed):
        status = "escalated"
    else:
        status = "descended"

    arch = ARCHETYPES[archetype]
    return {
        "type": type_, "objective": objective, "parts": parts, "register": register,
        "unit": unit, "per_part": per_part, "per_part_range": (lo, hi),
        "intro_max": arch["intro_max"], "conclusion": arch["conclusion"],
        "total": total, "archetype": archetype, "range": (arch["min_words"], arch["max_words"]),
        "status": status, "allowed": allowed, "below_minimum": below_minimum,
    }


def format_ficha(result: dict) -> str:
    lo, hi = result["range"]
    rng = f"{lo:,}–{hi:,}" if hi else f"{lo:,}+"
    p_lo, p_hi = result["per_part_range"]
    c_lo, c_hi = result["conclusion"]
    lines = [
        f"- Tipo / Objetivo / Partes: {result['type']} · {result['objective']} · {result['parts']}",
        f"- Registro: {result['register']}",
        f"- Presupuesto: {result['total']:,} palabras → {result['archetype']} ({rng}) · status {result['status']}",
    ]
    if result["status"] != "ok":
        allowed = ", ".join(result["allowed"])
        lines.append(f"  Justificación (obligatoria; el objetivo permite {allowed}): <una línea>")
    if result["below_minimum"]:
        lines.append(f"  Aviso: el total queda por debajo del mínimo de 'nota' ({lo:,}); no rellenes, revisa si el tema da para un artículo.")
    lines += [
        f"- Intro: ≤ {result['intro_max']} palabras",
        f"- Por {result['unit']}: {result['per_part']} palabras (rango {p_lo}–{p_hi}) × {result['parts']}",
        f"- Conclusión: {c_lo}–{c_hi} palabras",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Calcula el presupuesto de longitud y el arquetipo de un artículo.")
    parser.add_argument("--type", required=True, choices=list(PARTS), help="Forma del texto")
    parser.add_argument("--objective", required=True, choices=list(OBJECTIVES), help="Qué busca el lector")
    parser.add_argument("--parts", required=True, type=int, help="Número de partes del esquema (secciones '##' del cuerpo)")
    parser.add_argument("--serp-adjust", type=int, choices=(-1, 0, 1), default=0,
                        help="-1 usa el mínimo por parte, 0 el punto medio, +1 el máximo (según la profundidad de la SERP)")
    args = parser.parse_args()
    if args.parts < 1:
        parser.error("--parts debe ser un entero >= 1")
    print(format_ficha(plan(args.type, args.objective, args.parts, args.serp_adjust)))


if __name__ == "__main__":
    main()

import re
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
SKILL_DIR = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
import plan_length  # noqa: E402

DOCS = [SKILL_DIR / "SKILL.md", *sorted((SKILL_DIR / "references").glob("*.md"))]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(path: Path) -> str:
    return re.sub(r"\s+", " ", read(path)).lower()


def table_rows(text: str, key: str) -> list:
    """Filas de tabla Markdown cuya primera celda contiene `key` (un nombre puede ser tipo y arquetipo)."""
    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and f"`{key}`" in cells[0]:
            rows.append(line)
    return rows


def has_row_with(text: str, key: str, *expected: str) -> bool:
    return any(all(e in row for e in expected) for row in table_rows(text, key))


class ReadingTimeTablesMatchCodeTest(unittest.TestCase):
    text = read(SKILL_DIR / "references" / "reading-time.md")

    def test_archetype_rows_match_constants(self):
        for name, a in plan_length.ARCHETYPES.items():
            with self.subTest(archetype=name):
                upper = f"{a['max_words']:,}" if a["max_words"] else "sin tope"
                c_lo, c_hi = a["conclusion"]
                self.assertTrue(has_row_with(self.text, name, f"{a['min_words']:,} – {upper} | {a['intro_max']} | "
                                             f"{c_lo} – {c_hi} | {a['quotes_max']} |"))

    def test_parts_rows_match_constants(self):
        for type_, (unit, lo, hi) in plan_length.PARTS.items():
            with self.subTest(type=type_):
                self.assertTrue(has_row_with(self.text, type_, f"| {unit} | {lo} – {hi}"))

    def test_objective_rows_match_constants(self):
        for objective, (allowed, register) in plan_length.OBJECTIVES.items():
            with self.subTest(objective=objective):
                self.assertTrue(has_row_with(self.text, objective, f"| {', '.join(allowed)} | {register} |"))


class ForbiddenContentTest(unittest.TestCase):
    def test_no_doc_mentions_quote_minimums_or_mermaid_by_default(self):
        for path in DOCS:
            text = normalized(path)
            for phrase in ("mermaid cuando aplique", "nota 0–1", "guía 1–3", "2–4", "2 – 4"):
                with self.subTest(doc=path.name, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_natural_writing_has_no_copyable_example_phrases(self):
        text = normalized(SKILL_DIR / "references" / "natural-writing.md")
        for phrase in ("hoy quiero reflexionar contigo", "en mi día a día", "de novato a maestro",
                       "lecciones aprendidas en el camino"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)


class SkillMetadataTest(unittest.TestCase):
    text = read(SKILL_DIR / "SKILL.md")

    def test_version_is_6(self):
        self.assertRegex(self.text, r"(?m)^\s+version: 6\.0\.0$")

    def test_flow_uses_plan_length_openings_and_typed_validator(self):
        for expected in ("plan_length.py", "--openings", "--type", "--objective", "--visuals"):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.text)


if __name__ == "__main__":
    unittest.main()

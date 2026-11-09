import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))
import index_articles  # noqa: E402

SCRIPT = SCRIPTS / "index_articles.py"


def run_cli(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")


class FirstParagraphTest(unittest.TestCase):
    def test_skips_headings_images_and_rules(self):
        body = "# Título\n\n![Portada](img.webp)\n\n---\n\n## Sección\n\nLa guardia empezó a las tres.\nNadie dormía.\n\nSegundo párrafo."
        self.assertEqual(index_articles.first_paragraph(body), "La guardia empezó a las tres. Nadie dormía.")

    def test_skips_code_blocks(self):
        body = "```bash\necho hola\n```\n\nPrimera prosa."
        self.assertEqual(index_articles.first_paragraph(body), "Primera prosa.")

    def test_keeps_blockquote_opening(self):
        self.assertEqual(index_articles.first_paragraph("> Una cita que abre.\n\nDespués."), "> Una cita que abre.")

    def test_body_without_prose_returns_empty(self):
        self.assertEqual(index_articles.first_paragraph("## Solo encabezado\n"), "")


class OpeningsCliTest(unittest.TestCase):
    def test_openings_prints_date_title_and_paragraph_for_recent(self):
        proc = run_cli("--recent", "2", "--openings")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        entries = index_articles.recent(index_articles.load_index(index_articles.resolve_repo_root()), 2)
        for entry in entries:
            self.assertIn(entry["date"], proc.stdout)
            self.assertIn(entry["title"], proc.stdout)
            self.assertIn(index_articles.first_paragraph(entry["body"])[:60], proc.stdout)

    def test_openings_requires_recent(self):
        self.assertEqual(run_cli("--openings").returncode, 2)


if __name__ == "__main__":
    unittest.main()

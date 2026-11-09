import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))
import validate_article  # noqa: E402

REPO = validate_article.resolve_repo_root()
CONTACT = ("Si quieres comentar, escríbeme en [X (@algforge)](https://x.com/algforge) o en "
           "[GitHub](https://github.com/lgzarturo).")
NEW_WARNING_PREFIXES = ("Intro:", "Conclusión:", "Sección '", "Visuales:", "Transición")


def words(n: int) -> str:
    return " ".join(["texto"] * n) + "."


def article(intro=150, sections=(450, 450), conclusion=150, extra_body="", extra_intro=""):
    parts = [words(intro), extra_intro]
    for i, size in enumerate(sections, 1):
        parts += [f"## Sección {i}", words(size)]
    parts += [extra_body, "## Conclusión", words(conclusion), CONTACT,
              "## Referencias", "- [Fuente](https://example.com)"]
    return "\n\n".join(p for p in parts if p) + "\n"


def warnings_for(body, archetype="analisis", type_="analisis", visuals=0):
    return validate_article.structure_warnings(body, archetype, type_, visuals)


def new_warnings(warnings):
    return [w for w in warnings if w.startswith(NEW_WARNING_PREFIXES)]


class CleanArticleTest(unittest.TestCase):
    def test_clean_article_has_no_warnings(self):
        self.assertEqual(warnings_for(article()), [])


class IntroTest(unittest.TestCase):
    def test_inflated_intro_warns(self):
        self.assertTrue(any(w.startswith("Intro:") for w in warnings_for(article(intro=400))))


class ConclusionTest(unittest.TestCase):
    def test_short_conclusion_warns(self):
        self.assertTrue(any(w.startswith("Conclusión:") for w in warnings_for(article(conclusion=30))))

    def test_long_conclusion_warns(self):
        self.assertTrue(any(w.startswith("Conclusión:") for w in warnings_for(article(conclusion=300))))

    def test_contact_line_does_not_count_toward_conclusion(self):
        # 190 de prosa + ~20 de la línea de contacto superaría 200 si se contara.
        self.assertEqual(warnings_for(article(conclusion=190)), [])


class SectionTest(unittest.TestCase):
    def test_thin_section_warns(self):
        self.assertTrue(any(w.startswith("Sección '") for w in warnings_for(article(sections=(450, 100)))))

    def test_bloated_section_warns(self):
        self.assertTrue(any(w.startswith("Sección '") for w in warnings_for(article(sections=(450, 900)))))

    def test_subsections_multiply_the_range(self):
        body = article(sections=(450,), extra_body="## Larga\n\n### A\n\n" + words(450) + "\n\n### B\n\n" + words(450))
        self.assertEqual(warnings_for(body), [])

    def test_tolerance_of_25_percent_is_accepted(self):
        self.assertEqual(warnings_for(article(sections=(270, 680))), [])


class VisualsTest(unittest.TestCase):
    MERMAID = "```mermaid\ngraph TD\n  A --> B\n```"
    TABLE = "| a | b |\n|---|---|\n| 1 | 2 |"

    def test_undeclared_mermaid_warns(self):
        self.assertTrue(any(w.startswith("Visuales:") for w in warnings_for(article(extra_body=self.MERMAID))))

    def test_undeclared_table_warns(self):
        self.assertTrue(any(w.startswith("Visuales:") for w in warnings_for(article(extra_body=self.TABLE))))

    def test_declared_visuals_do_not_warn(self):
        body = article(extra_body=self.MERMAID + "\n\n" + self.TABLE)
        self.assertEqual(warnings_for(body, visuals=2), [])


class TransitionTest(unittest.TestCase):
    def test_blacklisted_transition_at_paragraph_start_warns(self):
        body = article(extra_body="Dicho esto, " + words(20))
        self.assertTrue(any(w.startswith("Transición") for w in warnings_for(body)))

    def test_blacklisted_phrase_mid_paragraph_does_not_warn(self):
        body = article(extra_body="Lo medí y, dicho esto, " + words(20))
        self.assertEqual(warnings_for(body), [])

    def test_every_blacklist_entry_is_detected(self):
        for phrase in validate_article.TRANSITION_BLACKLIST:
            with self.subTest(phrase=phrase):
                body = article(extra_body=f"{phrase} {words(20)}")
                self.assertTrue(any(w.startswith("Transición") for w in warnings_for(body)))


class QuotesAndCodeTest(unittest.TestCase):
    def test_too_many_quotes_warns(self):
        quotes = "\n\n".join(f"> cita {i}" for i in range(4))
        self.assertTrue(any("Citas en bloque" in w for w in warnings_for(article(extra_body=quotes))))

    def test_zero_quotes_does_not_warn(self):
        self.assertFalse(any("Citas en bloque" in w for w in warnings_for(article())))

    def test_tutorial_without_code_warns(self):
        body = article(sections=(400, 400))
        self.assertTrue(any("bloque de código" in w for w in warnings_for(body, "tutorial", "tutorial")))

    def test_tutorial_with_code_does_not_warn(self):
        body = article(sections=(400, 400), extra_body="```bash\necho hola\n```")
        self.assertFalse(any("bloque de código" in w for w in warnings_for(body, "tutorial", "tutorial")))


class ArchetypeOnlyModeTest(unittest.TestCase):
    def test_without_type_only_quotes_and_code_are_checked(self):
        body = article(intro=400, sections=(100,), conclusion=30, extra_body="Dicho esto, " + words(5))
        self.assertEqual(new_warnings(validate_article.structure_warnings(body, "analisis")), [])


class RegressionTest(unittest.TestCase):
    CASES = [
        ("articles/technology/antes-de-elegir-modelo-define-que-significa-terminar.md", "analisis", "entender"),
        ("articles/20-cosas-que-me-ha-ensenado-la-vida-a-los-43.md", "lista", "reflexionar"),
        ("articles/springboot-course/kotlin-springboot-4-java-25-concurrencia-postgresql.md", "tutorial", "hacer"),
    ]

    def test_published_articles_gain_no_errors_with_type(self):
        for rel, type_, objective in self.CASES:
            with self.subTest(article=rel):
                _, errors, _, info = validate_article.validate_article(
                    REPO / rel, "auto", ignore_date_today=True, type_=type_, objective=objective)
                self.assertEqual(errors, [])
                self.assertTrue(any("status" in i for i in info))

    def test_archetype_only_mode_adds_no_new_warnings(self):
        rel = self.CASES[0][0]
        _, errors, warnings, _ = validate_article.validate_article(REPO / rel, "auto", ignore_date_today=True,
                                                                   archetype="analisis")
        self.assertEqual(errors, [])
        self.assertEqual(new_warnings(warnings), [])


if __name__ == "__main__":
    unittest.main()

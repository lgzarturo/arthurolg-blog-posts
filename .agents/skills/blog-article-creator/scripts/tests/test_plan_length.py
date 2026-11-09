import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))
import plan_length  # noqa: E402

SCRIPT = SCRIPTS / "plan_length.py"


def run_cli(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, encoding="utf-8")


class PlanExamplesTest(unittest.TestCase):
    def test_lista_reflexionar_20_parts_escalates_to_tutorial(self):
        result = plan_length.plan("lista", "reflexionar", 20)
        self.assertEqual((result["archetype"], result["status"], result["total"]), ("tutorial", "escalated", 3600))

    def test_tutorial_hacer_3_parts_descends_to_guia(self):
        result = plan_length.plan("tutorial", "hacer", 3)
        self.assertEqual((result["archetype"], result["status"], result["total"]), ("guia", "descended", 1530))

    def test_analisis_decidir_4_parts_is_ok(self):
        result = plan_length.plan("analisis", "decidir", 4)
        self.assertEqual((result["archetype"], result["status"], result["total"]), ("analisis", "ok", 2200))


class PlanEdgeCasesTest(unittest.TestCase):
    def test_single_part_below_400_falls_back_to_nota_with_flag(self):
        result = plan_length.plan("lista", "reflexionar", 1, serp_adjust=-1)
        self.assertEqual((result["archetype"], result["total"], result["below_minimum"]), ("nota", 270, True))

    def test_total_inside_a_range_is_not_flagged_below_minimum(self):
        self.assertFalse(plan_length.plan("analisis", "decidir", 4)["below_minimum"])

    def test_serp_adjust_plus_one_uses_part_maximum(self):
        result = plan_length.plan("analisis", "decidir", 4, serp_adjust=1)
        self.assertEqual((result["per_part"], result["total"], result["archetype"]), (550, 2600, "analisis"))

    def test_serp_adjust_minus_one_uses_part_minimum_and_can_descend(self):
        result = plan_length.plan("analisis", "decidir", 4, serp_adjust=-1)
        self.assertEqual((result["per_part"], result["archetype"], result["status"]), (350, "guia", "descended"))

    def test_register_comes_from_objective(self):
        self.assertEqual(plan_length.plan("perfil", "decidir", 5)["register"], "evaluativo, con criterios")

    def test_parts_below_one_raises(self):
        with self.assertRaises(ValueError):
            plan_length.plan("lista", "reflexionar", 0)


class SectionRangeTest(unittest.TestCase):
    def test_section_without_subsections_uses_one_part(self):
        self.assertEqual(plan_length.section_range("lista", 0), (100, 220))

    def test_subsections_multiply_the_range(self):
        self.assertEqual(plan_length.section_range("lista", 3), (300, 660))


class CliTest(unittest.TestCase):
    def test_valid_call_prints_ficha_block(self):
        proc = run_cli("--type", "lista", "--objective", "reflexionar", "--parts", "20")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("lista · reflexionar · 20", proc.stdout)
        self.assertIn("3,600 palabras → tutorial", proc.stdout)
        self.assertIn("status escalated", proc.stdout)
        self.assertIn("Justificación", proc.stdout)

    def test_ok_status_does_not_ask_for_justification(self):
        proc = run_cli("--type", "analisis", "--objective", "decidir", "--parts", "4")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("Justificación", proc.stdout)

    def test_below_minimum_prints_warning(self):
        proc = run_cli("--type", "lista", "--objective", "reflexionar", "--parts", "1", "--serp-adjust", "-1")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("por debajo", proc.stdout)

    def test_missing_parts_is_rejected(self):
        self.assertEqual(run_cli("--type", "lista", "--objective", "reflexionar").returncode, 2)

    def test_parts_zero_is_rejected(self):
        self.assertEqual(run_cli("--type", "lista", "--objective", "reflexionar", "--parts", "0").returncode, 2)

    def test_unknown_type_is_rejected(self):
        self.assertEqual(run_cli("--type", "receta", "--objective", "hacer", "--parts", "3").returncode, 2)

    def test_unknown_objective_is_rejected(self):
        self.assertEqual(run_cli("--type", "lista", "--objective", "vender", "--parts", "3").returncode, 2)

    def test_serp_adjust_out_of_range_is_rejected(self):
        self.assertEqual(run_cli("--type", "lista", "--objective", "hacer", "--parts", "3", "--serp-adjust", "2").returncode, 2)


if __name__ == "__main__":
    unittest.main()

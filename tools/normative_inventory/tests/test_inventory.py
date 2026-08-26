import json
import tempfile
import unittest
from pathlib import Path

from tools.normative_inventory.core import build_inventory, build_norm_matrix, compare_inventories, extract_metadata, normalize_name


class InventoryTests(unittest.TestCase):
    def test_metadata_supports_accents_and_non_vigente_proposal(self):
        metadata = extract_metadata("Emenda Constituição — V1.0.md", "Código: UDF-001\nEstado: APROVADO_NAO_PROMULGADO\nAutoridade: Reitoria")
        self.assertEqual(metadata["state"], "APROVADO_NAO_PROMULGADO")
        self.assertEqual(metadata["authority"], "Reitoria")
        self.assertEqual(normalize_name("Emenda Constituição — V1.0.md"), "emenda constituicao v1 0")

    def test_duplicate_and_incremental_report_are_deterministic(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "a.md").write_text("Código: UDF-001\nEstado: HISTORICO", encoding="utf-8")
            (root / "b.md").write_bytes((root / "a.md").read_bytes())
            first = build_inventory([root], generated_at="2026-08-26T00:00:00+00:00")
            self.assertEqual(first["summary"]["files"], 2)
            self.assertEqual(len(first["duplicate_groups"]["exact"]), 1)
            (root / "c.txt").write_text("novo", encoding="utf-8")
            second = build_inventory([root], generated_at="2026-08-26T00:01:00+00:00")
            self.assertEqual(len(compare_inventories(second, first)["added"]), 1)
            self.assertEqual(len(build_norm_matrix(second)), 3)
            json.dumps(second, ensure_ascii=False, sort_keys=True)


if __name__ == "__main__":
    unittest.main()

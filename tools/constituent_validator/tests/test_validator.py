import hashlib
import unittest

from tools.constituent_validator.validator import safe_zip_members, validate_manifest, validate_transition, validate_votes


class ValidatorTests(unittest.TestCase):
    def test_valid_invalid_and_extra_manifest(self):
        data = b"juramento"
        digest = hashlib.sha256(data).hexdigest()
        manifest = {"files": [{"name": "raiz.md", "sha256": digest, "code": "UDF-1", "version": "1"}]}
        self.assertTrue(validate_manifest(manifest, {"raiz.md": data})["valid"])
        self.assertFalse(validate_manifest(manifest, {"raiz.md": b"alterado"})["valid"])
        self.assertFalse(validate_manifest(manifest, {"raiz.md": data, "extra.md": b"x"})["valid"])

    def test_votes_and_transitions_are_not_counts_or_promulgation(self):
        result = validate_votes({"denominator": 2, "votes": [{"identity": "A", "declaration": "SIM"}, {"identity": "A", "declaration": "SIM"}]})
        self.assertFalse(result["valid"])
        self.assertIsNone(result["vote_count"])
        self.assertFalse(validate_transition("PARA_VISTAS", "VIGENTE")["valid"])
        self.assertFalse(validate_transition("PARA_VISTAS", "APROVADO_NAO_PROMULGADO")["valid"] is False)

    def test_zip_slip_and_human_gate_are_safe(self):
        self.assertFalse(safe_zip_members(["ok/file.md", "../escape.md"])["safe"])
        self.assertFalse(validate_transition("PARA_VISTAS", "APROVADO_NAO_PROMULGADO", human_gate=True)["valid"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = ROOT.parent / "backend_academico"
sys.path.insert(0, str(BACKEND_ROOT))

from jus9_backend.api import AcademicBackend  # noqa: E402
from jus9_backend.ghr import sha256_payload  # noqa: E402
from dictionary_pipeline import validate_corpus  # noqa: E402


class BackendIntegrationTests(unittest.TestCase):
    def test_dictionary_snapshot_registers_in_existing_genealogy_backend(self) -> None:
        corpus = json.loads((ROOT / "data" / "lote_500_sementes.json").read_text(encoding="utf-8"))
        report = validate_corpus(corpus)
        payload = {
            "artifact_type": "DICTIONARY_SEED_CORPUS",
            "expected_total": report["expected_total"],
            "total": report["total"],
            "state_counts": report["state_counts"],
            "source_snapshot": corpus["source_snapshot"],
        }
        backend = AcademicBackend()
        artifact = backend.register_artifact(
            artifact_id="dictionary-500-seed-corpus",
            version="v3.0.0",
            payload=payload,
            source=corpus["source_snapshot"]["source_document_id"],
            actor="codex-dicionarios",
            classification="INTERNAL",
            epistemic_state="DOCUMENTED",
        )
        self.assertEqual(artifact.payload["total"], 500)
        self.assertEqual(len(backend.ghr.records("dictionary-500-seed-corpus")), 1)
        self.assertEqual(artifact.sha256, sha256_payload(payload))


if __name__ == "__main__":
    unittest.main()

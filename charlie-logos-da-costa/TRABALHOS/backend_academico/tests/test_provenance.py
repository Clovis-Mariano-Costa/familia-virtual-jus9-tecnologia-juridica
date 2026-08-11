from __future__ import annotations

import unittest
import tempfile
from pathlib import Path

from jus9_backend.ghr import HashConflictError
from jus9_backend.api import AcademicBackend
from jus9_backend.provenance import EpistemicState, Nature, ProvenanceError, ProvenanceRegistry, reproducible_demo
from jus9_backend.store import JsonStore


def create_root(registry: ProvenanceRegistry, *, record_id: str = "root"):
    return registry.create(record_id=record_id, artifact_id="artifact", version="v1", payload={"value": 1},
        source="DRIVE/CASA_LAR", evidence=("drive:file-1",), agent="codex", activity="INGESTAO",
        classification="INTERNAL", permission="READ_ONLY", epistemic_state=EpistemicState.HYPOTHESIS.value,
        confidence=0.5, nature=Nature.HYPOTHESIS.value, timestamp="2026-08-10T12:00:00.00000Z")


class ProvenanceRegistryTests(unittest.TestCase):
    def test_hash_index_and_reproducible_chain(self) -> None:
        registry, destination_id = reproducible_demo()
        self.assertEqual([record.record_id for record in registry.chain(destination_id)],
                         ["origin-001", "transform-001", "version-001", "destination-001"])
        self.assertTrue(registry.verify("origin-001", {"text": "fonte inicial"}))
        self.assertIn("INGESTAO_CONTROLADA", registry.render_chain(destination_id))
        self.assertEqual(len(registry.events), 4)

    def test_missing_parent_and_hash_conflict_are_blocked(self) -> None:
        registry = ProvenanceRegistry()
        with self.assertRaises(ProvenanceError):
            registry.derive(record_id="child", artifact_id="a", version="v1", payload={"x": 1},
                parent_ids=("missing",), source="s", activity="a", destination="d", evidence=("e",),
                agent="codex", classification="INTERNAL", permission="READ_ONLY")
        create_root(registry)
        with self.assertRaises(HashConflictError):
            registry.create(record_id="conflict", artifact_id="artifact", version="v1", payload={"value": 2},
                source="DRIVE/CASA_LAR", evidence=("drive:file-1",), agent="codex", activity="INGESTAO",
                classification="INTERNAL", permission="READ_ONLY", timestamp="2026-08-10T12:00:00.00000Z")

    def test_hypothesis_cannot_be_promoted_without_explicit_approval(self) -> None:
        registry = ProvenanceRegistry()
        root = create_root(registry)
        with self.assertRaises(ProvenanceError):
            registry.transition_epistemic(root.record_id, EpistemicState.DOCUMENTED.value, actor="codex",
                authority="REVIEWER", reason="promotion attempt")
        registry.transition_epistemic(root.record_id, EpistemicState.DOCUMENTED.value, actor="reviewer",
            authority="HUMAN_REVIEW", reason="explicit review", approval_reference="approval-1")
        self.assertEqual(root.epistemic_state, EpistemicState.DOCUMENTED.value)

    def test_revocation_creates_tombstone_and_preserves_history(self) -> None:
        registry = ProvenanceRegistry()
        root = create_root(registry)
        tombstone = registry.revoke(root.record_id, actor="reviewer", reason="source revoked")
        self.assertTrue(registry.is_revoked(root.record_id))
        self.assertEqual(tombstone.artifact_state, "REVOGADO")
        self.assertIn(root.record_id, tombstone.parent_ids)
        self.assertEqual(len(registry.records), 2)
        with self.assertRaises(ProvenanceError):
            registry.derive(record_id="child", artifact_id="artifact", version="v2", payload={"value": 2},
                parent_ids=(root.record_id,), source="BACKEND", activity="REVISAO", destination="INDEX",
                evidence=("review-1",), agent="codex", classification="INTERNAL", permission="READ_ONLY")

    def test_export_is_auditable(self) -> None:
        registry = ProvenanceRegistry()
        root = create_root(registry)
        exported = registry.export()
        self.assertEqual(exported["records"][0]["record_id"], root.record_id)
        self.assertIn("index", exported)
        self.assertEqual(exported["events"][0]["event_type"], "RECORD_CREATED")
        self.assertNotIn("password", str(exported).lower())

    def test_backend_api_exposes_chain_and_persists_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            backend = AcademicBackend(JsonStore(Path(directory) / "backend.json"))
            root = backend.register_provenance(
                record_id="api-root", artifact_id="api-artifact", version="v1", payload={"safe": True},
                source="DRIVE/CASA_LAR", evidence=("source:api",), agent="codex", activity="INGESTAO",
                classification="INTERNAL", permission="READ_ONLY", timestamp="2026-08-10T12:00:00.00000Z",
            )
            child = backend.derive_provenance(
                record_id="api-child", artifact_id="api-artifact", version="v2", payload={"safe": "revised"},
                parent_ids=(root.record_id,), source="BACKEND", activity="REVISAO", destination="INDEX_MESTRE",
                evidence=("review:api",), agent="codex", classification="INTERNAL", permission="READ_ONLY",
                timestamp="2026-08-10T12:01:00.00000Z",
            )
            self.assertEqual([item.record_id for item in backend.provenance_chain(child.record_id)],
                             ["api-root", "api-child"])
            persisted = (Path(directory) / "backend.json").read_text(encoding="utf-8")
            self.assertIn('"provenance"', persisted)


if __name__ == "__main__":
    unittest.main()

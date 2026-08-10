from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from jus9_backend.api import AcademicBackend
from jus9_backend.asm import AcademicState, AcademicStateMachine, TransitionError
from jus9_backend.gates import GateContext, GateValidator
from jus9_backend.ghr import GenealogyLedger, HashConflictError
from jus9_backend.models import TransitionRequest
from jus9_backend.store import JsonStore


def request(role: str = "AUTOR_FUNCIONAL", evidence: tuple[str, ...] = ("evidence-1",)) -> TransitionRequest:
    return TransitionRequest(
        actor="codex-reviewer",
        role=role,
        evidence=evidence,
        version="v1.0.0",
        timestamp="2026-08-10T12:00:00.00000Z",
        classification="INTERNAL",
        risk="LOW",
        justification="explicit test transition",
    )


class AcademicStateMachineTests(unittest.TestCase):
    def test_valid_transition_and_event(self) -> None:
        machine = AcademicStateMachine()
        event = machine.transition("a-1", AcademicState.M01, request())
        self.assertEqual(event.result, "ACCEPTED")
        self.assertEqual(machine.current_state("a-1"), AcademicState.M01)

    def test_invalid_transition_is_blocked(self) -> None:
        with self.assertRaises(TransitionError):
            AcademicStateMachine().transition("a-1", AcademicState.M08, request("REITORIA"))

    def test_rollback_preserves_history(self) -> None:
        machine = AcademicStateMachine()
        event = machine.transition("a-1", AcademicState.M01, request())
        rolled = machine.rollback("evt-000001", request("CODEX_TECNICO"))
        self.assertEqual(rolled.result, "ROLLED_BACK")
        self.assertEqual(machine.current_state("a-1"), AcademicState.M00)
        self.assertEqual(len(machine.events("a-1")), 2)


class GenealogyTests(unittest.TestCase):
    def test_hash_and_parent_chain(self) -> None:
        ledger = GenealogyLedger()
        root = ledger.append(
            artifact_id="a-1", version="v1", payload={"x": 1}, source="drive",
            transformation="ingest", destination="backend", actor="codex",
            classification="INTERNAL", epistemic_state="DOCUMENTED",
        )
        child = ledger.append(
            artifact_id="a-1", version="v2", payload={"x": 2}, source="backend",
            transformation="revise", destination="backend", actor="codex",
            classification="INTERNAL", epistemic_state="DOCUMENTED", parent_ids=(root.record_id,),
        )
        self.assertTrue(ledger.verify({"x": 2}, child.sha256))
        self.assertEqual(child.parent_ids, (root.record_id,))

    def test_hash_divergence_is_blocked(self) -> None:
        ledger = GenealogyLedger()
        ledger.append(
            artifact_id="a-1", version="v1", payload={"x": 1}, source="drive",
            transformation="ingest", destination="backend", actor="codex",
            classification="INTERNAL", epistemic_state="DOCUMENTED",
        )
        with self.assertRaises(HashConflictError):
            ledger.append(
                artifact_id="a-1", version="v1", payload={"x": 2}, source="drive",
                transformation="conflict", destination="backend", actor="codex",
                classification="INTERNAL", epistemic_state="DOCUMENTED",
            )


class GateTests(unittest.TestCase):
    def test_publication_is_fail_closed(self) -> None:
        decision = GateValidator().validate(GateContext(
            artifact_id="a-1", target_state="M22_PUBLICADO_NA_BIBLIOTECA",
            actor="codex", role="CODEX_TECNICO", evidence=("e1",),
        ))
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason_code, "PROMOTION_BLOCKED_PENDING_EVIDENCE")
        self.assertIn("gate de segurança não aprovado", decision.reasons)

    def test_valid_intermediate_transition_allows(self) -> None:
        decision = GateValidator().validate(GateContext(
            artifact_id="a-1", target_state="M01_RASCUNHO_CLASSIFICADO",
            actor="codex", role="AUTOR_FUNCIONAL", evidence=("e1",),
        ))
        self.assertTrue(decision.allowed)


class PersistenceTests(unittest.TestCase):
    def test_backend_persists_sanitized_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "backend.json"
            backend = AcademicBackend(JsonStore(path))
            backend.register_artifact(
                artifact_id="a-1", version="v1", payload={"safe": True}, source="drive",
                actor="codex", classification="INTERNAL", epistemic_state="DOCUMENTED",
            )
            self.assertTrue(path.exists())
            self.assertIn("genealogy", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

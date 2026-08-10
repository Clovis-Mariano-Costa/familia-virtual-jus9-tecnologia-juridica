from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from .asm import AcademicState, AcademicStateMachine
from .gates import GateDecision, GateValidator
from .ghr import GenealogyLedger
from .models import ArtifactRecord, GateContext, TransitionRequest, utc_timestamp
from .store import JsonStore


class AcademicBackend:
    """Orchestrator API for the scoped ASM/GHR/GV package."""

    def __init__(self, store: JsonStore | None = None) -> None:
        self.asm = AcademicStateMachine()
        self.ghr = GenealogyLedger()
        self.gates = GateValidator()
        self.store = store
        self.artifacts: dict[str, ArtifactRecord] = {}

    def register_artifact(
        self,
        *,
        artifact_id: str,
        version: str,
        payload: Mapping[str, Any],
        source: str,
        actor: str,
        classification: str,
        epistemic_state: str,
    ) -> ArtifactRecord:
        record = self.ghr.append(
            artifact_id=artifact_id,
            version=version,
            payload=payload,
            source=source,
            transformation="REGISTER_CANONICAL_ARTIFACT",
            destination="ACADEMIC_BACKEND",
            actor=actor,
            classification=classification,
            epistemic_state=epistemic_state,
        )
        artifact = ArtifactRecord(
            artifact_id=artifact_id,
            version=version,
            payload=dict(payload),
            source=source,
            actor=actor,
            classification=classification,
            epistemic_state=epistemic_state,
            created_at=record.created_at,
            sha256=record.sha256,
        )
        self.artifacts[artifact_id] = artifact
        self._persist()
        return artifact

    def evaluate_gate(self, context: GateContext) -> GateDecision:
        return self.gates.validate(context)

    def transition(self, artifact_id: str, target: AcademicState, request: TransitionRequest):
        decision = self.evaluate_gate(
            GateContext(
                artifact_id=artifact_id,
                target_state=target.value,
                actor=request.actor,
                role=request.role,
                evidence=request.evidence,
            )
        )
        if not decision.allowed:
            raise PermissionError("; ".join(decision.reasons))
        event = self.asm.transition(artifact_id, target, request)
        self._persist()
        return event

    def _persist(self) -> None:
        if self.store is None:
            return
        self.store.write(
            {
                "artifacts": [asdict(value) for value in self.artifacts.values()],
                "events": [asdict(value) for value in self.asm.events()],
                "genealogy": [asdict(value) for value in self.ghr.records()],
            }
        )

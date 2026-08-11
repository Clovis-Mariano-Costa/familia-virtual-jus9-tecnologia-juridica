from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from .asm import AcademicState, AcademicStateMachine
from .gates import GateDecision, GateValidator
from .ghr import GenealogyLedger
from .models import ArtifactRecord, GateContext, TransitionRequest, utc_timestamp
from .provenance import ProvenanceRecord, ProvenanceRegistry
from .security import CyberSecurityContext, CyberSecurityGate, SecurityDecision
from .store import JsonStore


class AcademicBackend:
    """Orchestrator API for the scoped ASM/GHR/GV package."""

    def __init__(self, store: JsonStore | None = None) -> None:
        self.asm = AcademicStateMachine()
        self.ghr = GenealogyLedger()
        self.gates = GateValidator()
        self.security_gate = CyberSecurityGate()
        self.provenance = ProvenanceRegistry()
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

    def evaluate_cybersecurity(self, context: CyberSecurityContext) -> SecurityDecision:
        """Evaluate the independent fail-closed cybersecurity gate."""
        return self.security_gate.evaluate(context)

    def register_provenance(self, **kwargs: Any) -> ProvenanceRecord:
        record = self.provenance.create(**kwargs)
        self._persist()
        return record

    def derive_provenance(self, **kwargs: Any) -> ProvenanceRecord:
        record = self.provenance.derive(**kwargs)
        self._persist()
        return record

    def revoke_provenance(self, record_id: str, *, actor: str, reason: str) -> ProvenanceRecord:
        tombstone = self.provenance.revoke(record_id, actor=actor, reason=reason)
        self._persist()
        return tombstone

    def provenance_chain(self, record_id: str) -> tuple[ProvenanceRecord, ...]:
        return self.provenance.chain(record_id)

    def transition(
        self,
        artifact_id: str,
        target: AcademicState,
        request: TransitionRequest,
        *,
        security_context: CyberSecurityContext | None = None,
    ):
        security_decision = None
        if int(target.value[1:3]) >= 8:
            if security_context is None:
                raise PermissionError("cybersecurity context required for relevant promotion")
            security_decision = self.evaluate_cybersecurity(security_context)
            if not security_decision.allowed:
                raise PermissionError("; ".join(security_decision.reasons))
        decision = self.evaluate_gate(
            GateContext(
                artifact_id=artifact_id,
                target_state=target.value,
                actor=request.actor,
                role=request.role,
                evidence=request.evidence,
                security_passed=security_decision.allowed if security_decision else False,
                tenant_isolated=security_context.tenant_isolated if security_context else False,
                rollback_ready=security_context.rollback_ready if security_context else False,
                secrets_detected=security_context.secrets_detected if security_context else False,
                dependencies_known=security_context.dependencies_known if security_context else False,
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
                "provenance": self.provenance.export(),
            }
        )

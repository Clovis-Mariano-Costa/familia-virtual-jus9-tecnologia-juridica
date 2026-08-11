"""Proveniência verificável, auditoria append-only e índice de genealogia."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from itertools import count
from typing import Any, Iterable, Mapping
import re

from .ghr import HashConflictError, sha256_payload
from .models import utc_timestamp


class ProvenanceError(ValueError):
    """Erro de contrato ou de integridade da proveniência."""


class EpistemicState(str, Enum):
    DOCUMENTED = "DOCUMENTADO"
    RECONSTRUCTION = "RECONSTRUCAO"
    INFERENCE = "INFERENCIA"
    ASSOCIATION = "ASSOCIACAO"
    HYPOTHESIS = "HIPOTESE"
    SIMULATION = "SIMULACAO"
    UNKNOWN = "DESCONHECIDO"


class ArtifactState(str, Enum):
    ACTIVE = "ATIVO"
    HISTORICAL = "HISTORICO"
    SUPERSEDED = "SUBSTITUIDO"
    PENDING = "PENDENTE"
    CONFLICTING = "CONFLITANTE"
    REVOKED = "REVOGADO"


class Nature(str, Enum):
    SCIENTIFIC_PHYSICAL = "CIENTIFICO_FISICO"
    QUANTUM_COMPUTING = "COMPUTACAO_QUANTICA"
    PHILOSOPHICAL_OPERATIONAL = "FILOSOFICO_EPISTEMOLOGICO_OPERACIONAL"
    METAPHOR = "METAFORA"
    HYPOTHESIS = "HIPOTESE"
    NOT_DEMONSTRATED = "NAO_DEMONSTRADO"


_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{5}Z")


@dataclass
class ProvenanceRecord:
    record_id: str
    artifact_id: str
    version: str
    source: str
    evidence: tuple[str, ...]
    agent: str
    activity: str
    timestamp: str
    classification: str
    permission: str
    epistemic_state: str
    confidence: float
    dependencies: tuple[str, ...]
    parent_ids: tuple[str, ...]
    destination: str
    nature: str
    sha256: str
    artifact_state: str = ArtifactState.ACTIVE.value
    supersedes: str | None = None

    def __post_init__(self) -> None:
        required = (
            self.record_id, self.artifact_id, self.version, self.source,
            self.agent, self.activity, self.classification, self.permission,
            self.epistemic_state, self.destination, self.nature, self.sha256,
        )
        if any(not str(value).strip() for value in required):
            raise ProvenanceError("all identity, authority, state and integrity fields are required")
        if not self.evidence:
            raise ProvenanceError("at least one evidence reference is required")
        if not 0.0 <= float(self.confidence) <= 1.0:
            raise ProvenanceError("confidence must be between 0 and 1")
        if not _TIMESTAMP.fullmatch(self.timestamp):
            raise ProvenanceError("timestamp must be UTC with five fractional digits")
        if len(self.sha256) != 64 or any(char not in "0123456789abcdef" for char in self.sha256):
            raise ProvenanceError("sha256 must be a lowercase hexadecimal digest")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    event_type: str
    record_id: str
    actor: str
    timestamp: str
    reason: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


class ProvenanceRegistry:
    """Registry with deterministic hashes, genealogy and append-only events."""

    def __init__(self) -> None:
        self._records: dict[str, ProvenanceRecord] = {}
        self._events: list[AuditEvent] = []
        self._revoked: set[str] = set()
        self._ids = count(1)
        self._event_ids = count(1)

    @property
    def records(self) -> tuple[ProvenanceRecord, ...]:
        return tuple(self._records.values())

    @property
    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)

    def create(self, *, record_id: str, artifact_id: str, version: str,
               payload: Mapping[str, Any], source: str, evidence: Iterable[str],
               agent: str, activity: str, classification: str, permission: str,
               epistemic_state: str = EpistemicState.DOCUMENTED.value,
               confidence: float = 1.0, dependencies: Iterable[str] = (),
               parent_ids: Iterable[str] = (), destination: str = "BACKEND_ACADEMICO",
               nature: str = Nature.NOT_DEMONSTRATED.value, timestamp: str | None = None,
               supersedes: str | None = None, artifact_state: str = ArtifactState.ACTIVE.value) -> ProvenanceRecord:
        record = ProvenanceRecord(
            record_id=record_id, artifact_id=artifact_id, version=version,
            source=source, evidence=tuple(evidence), agent=agent, activity=activity,
            timestamp=timestamp or utc_timestamp(), classification=classification,
            permission=permission, epistemic_state=epistemic_state, confidence=confidence,
            dependencies=tuple(dependencies), parent_ids=tuple(parent_ids),
            destination=destination, nature=nature, sha256=sha256_payload(payload),
            artifact_state=artifact_state, supersedes=supersedes,
        )
        self.add(record)
        self._audit("RECORD_CREATED", record.record_id, agent, "record registered", {"sha256": record.sha256})
        return record

    def add(self, record: ProvenanceRecord) -> None:
        if record.record_id in self._records:
            raise ProvenanceError(f"duplicate record_id: {record.record_id}")
        unknown = [parent for parent in record.parent_ids if parent not in self._records]
        if unknown:
            raise ProvenanceError(f"unknown parent records: {unknown}")
        same_version = [item for item in self._records.values()
                        if item.artifact_id == record.artifact_id and item.version == record.version]
        if record.artifact_state != ArtifactState.REVOKED.value and any(item.sha256 != record.sha256 for item in same_version):
            raise HashConflictError(f"hash divergence for {record.artifact_id} version {record.version}")
        self._records[record.record_id] = record

    def derive(self, *, record_id: str, artifact_id: str, version: str,
               payload: Mapping[str, Any], parent_ids: Iterable[str], source: str,
               activity: str, destination: str, evidence: Iterable[str], agent: str,
               classification: str, permission: str,
               epistemic_state: str = EpistemicState.RECONSTRUCTION.value,
               confidence: float = 1.0, nature: str = Nature.NOT_DEMONSTRATED.value,
               timestamp: str | None = None) -> ProvenanceRecord:
        parents = tuple(parent_ids)
        for parent_id in parents:
            self._require(parent_id)
            if parent_id in self._revoked:
                raise ProvenanceError(f"revoked record cannot be used as a source: {parent_id}")
        return self.create(
            record_id=record_id, artifact_id=artifact_id, version=version, payload=payload,
            source=source, evidence=evidence, agent=agent, activity=activity,
            classification=classification, permission=permission, epistemic_state=epistemic_state,
            confidence=confidence, dependencies=parents, parent_ids=parents,
            destination=destination, nature=nature, timestamp=timestamp,
        )

    def transition_epistemic(self, record_id: str, target: str, *, actor: str,
                             authority: str, reason: str,
                             approval_reference: str | None = None) -> ProvenanceRecord:
        record = self._require(record_id)
        if not actor.strip() or not authority.strip() or not reason.strip():
            raise ProvenanceError("epistemic transition requires actor, authority and reason")
        if target == EpistemicState.DOCUMENTED.value and record.epistemic_state != target and not approval_reference:
            raise ProvenanceError("promotion to DOCUMENTADO requires explicit approval evidence")
        record.epistemic_state = target
        self._audit("EPISTEMIC_STATE_CHANGED", record_id, actor, reason,
                    {"authority": authority, "target": target, "approval_reference": approval_reference})
        return record

    def revoke(self, record_id: str, *, actor: str, reason: str) -> ProvenanceRecord:
        original = self._require(record_id)
        if not actor.strip() or not reason.strip():
            raise ProvenanceError("revocation requires actor and reason")
        self._revoked.add(record_id)
        tombstone = self.create(
            record_id=f"tombstone-{next(self._ids):06d}", artifact_id=original.artifact_id,
            version=original.version, payload={"revoked_record_id": record_id, "reason": reason},
            source=original.source, evidence=original.evidence, agent=actor,
            activity="TOMBSTONE_REVOGACAO", classification=original.classification,
            permission=original.permission, epistemic_state=original.epistemic_state,
            confidence=original.confidence, dependencies=(record_id,), parent_ids=(record_id,),
            destination="AUDIT_LOG", nature=original.nature,
            artifact_state=ArtifactState.REVOKED.value, supersedes=record_id,
        )
        self._audit("RECORD_REVOKED", record_id, actor, reason, {"tombstone": tombstone.record_id})
        return tombstone

    def verify(self, record_id: str, payload: Mapping[str, Any]) -> bool:
        return sha256_payload(payload) == self._require(record_id).sha256

    def is_revoked(self, record_id: str) -> bool:
        return record_id in self._revoked

    def chain(self, record_id: str) -> tuple[ProvenanceRecord, ...]:
        self._require(record_id)
        ordered: list[ProvenanceRecord] = []
        visited: set[str] = set()

        def visit(current_id: str) -> None:
            if current_id in visited:
                return
            visited.add(current_id)
            current = self._require(current_id)
            for parent_id in current.parent_ids:
                visit(parent_id)
            ordered.append(current)

        visit(record_id)
        return tuple(ordered)

    def render_chain(self, record_id: str) -> str:
        return "\n".join(
            f"{index:02d}. {record.record_id} | {record.source} --[{record.activity}]--> "
            f"{record.destination} | {record.version} | {record.epistemic_state}"
            for index, record in enumerate(self.chain(record_id), 1)
        )

    def index_report(self) -> dict[str, Any]:
        by_artifact: dict[str, list[str]] = {}
        by_state: dict[str, list[str]] = {}
        for record in self.records:
            by_artifact.setdefault(record.artifact_id, []).append(record.record_id)
            by_state.setdefault(record.artifact_state, []).append(record.record_id)
        return {"by_artifact": by_artifact, "by_state": by_state, "revoked": sorted(self._revoked)}

    def export(self) -> dict[str, Any]:
        return {"records": [record.to_dict() for record in self.records],
                "events": [asdict(event) for event in self.events], "index": self.index_report()}

    def _require(self, record_id: str) -> ProvenanceRecord:
        try:
            return self._records[record_id]
        except KeyError as error:
            raise ProvenanceError(f"unknown record: {record_id}") from error

    def _audit(self, event_type: str, record_id: str, actor: str, reason: str, metadata: Mapping[str, Any]) -> None:
        self._events.append(AuditEvent(
            event_id=f"audit-{next(self._event_ids):06d}", event_type=event_type,
            record_id=record_id, actor=actor, timestamp=utc_timestamp(), reason=reason,
            metadata=dict(metadata)))


def reproducible_demo() -> tuple[ProvenanceRegistry, str]:
    """Build origin -> transformation -> version -> destination."""
    registry = ProvenanceRegistry()
    root = registry.create(record_id="origin-001", artifact_id="demo-artifact", version="v1",
        payload={"text": "fonte inicial"}, source="DRIVE/CASA_LAR", evidence=("source:demo",),
        agent="codex", activity="INGESTAO_CONTROLADA", classification="INTERNAL", permission="READ_ONLY",
        epistemic_state=EpistemicState.DOCUMENTED.value, nature=Nature.NOT_DEMONSTRATED.value,
        timestamp="2026-08-10T12:00:00.00000Z")
    transformed = registry.derive(record_id="transform-001", artifact_id="demo-artifact", version="v2",
        payload={"text": "fonte normalizada"}, parent_ids=(root.record_id,), source="BACKEND",
        activity="NORMALIZACAO_DEMONSTRATIVA", destination="BACKEND", evidence=("transform:demo",),
        agent="codex", classification="INTERNAL", permission="READ_ONLY", timestamp="2026-08-10T12:01:00.00000Z")
    versioned = registry.derive(record_id="version-001", artifact_id="demo-artifact", version="v3",
        payload={"text": "versao revisada"}, parent_ids=(transformed.record_id,), source="BACKEND",
        activity="REVISAO_VERSIONADA", destination="INDEX_MESTRE", evidence=("review:demo",),
        agent="codex", classification="INTERNAL", permission="READ_ONLY", timestamp="2026-08-10T12:02:00.00000Z")
    destination = registry.derive(record_id="destination-001", artifact_id="demo-artifact", version="v4",
        payload={"text": "versao revisada entregue"}, parent_ids=(versioned.record_id,), source="INDEX_MESTRE",
        activity="ENTREGA_AUDITADA", destination="CASA_TRABALHO", evidence=("delivery:demo",),
        agent="codex", classification="INTERNAL", permission="READ_ONLY", timestamp="2026-08-10T12:03:00.00000Z")
    return registry, destination.record_id


__all__ = ["ArtifactState", "AuditEvent", "EpistemicState", "Nature", "ProvenanceError",
           "ProvenanceRecord", "ProvenanceRegistry", "reproducible_demo"]

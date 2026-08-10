from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
from typing import Any, Mapping


def utc_timestamp(value: datetime | None = None) -> str:
    """Return a real UTC timestamp with exactly five fractional digits."""
    value = value or datetime.now(timezone.utc)
    if value.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    value = value.astimezone(timezone.utc)
    return value.strftime("%Y-%m-%dT%H:%M:%S.") + f"{value.microsecond // 10:05d}Z"


@dataclass(frozen=True)
class TransitionRequest:
    actor: str
    role: str
    evidence: tuple[str, ...]
    version: str
    timestamp: str
    classification: str
    risk: str
    justification: str
    rollback: str | None = None

    def __post_init__(self) -> None:
        if not self.actor.strip() or self.actor.strip().lower() in {"system", "automatic", "automation"}:
            raise ValueError("actor must identify an accountable actor; automatic promotion is forbidden")
        if not self.role.strip():
            raise ValueError("role is required")
        if not self.evidence:
            raise ValueError("at least one evidence reference is required")
        if not self.version.strip() or not self.classification.strip() or not self.risk.strip():
            raise ValueError("version, classification and risk are required")
        if not self.justification.strip():
            raise ValueError("justification is required")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{5}Z", self.timestamp):
            raise ValueError("timestamp must be UTC with five fractional digits, e.g. 2026-01-01T00:00:00.00000Z")


@dataclass(frozen=True)
class AcademicEvent:
    event_id: str
    artifact_id: str
    from_state: str
    to_state: str
    actor: str
    role: str
    evidence: tuple[str, ...]
    version: str
    timestamp: str
    classification: str
    risk: str
    justification: str
    result: str
    rollback: str | None = None


@dataclass(frozen=True)
class GateContext:
    artifact_id: str
    target_state: str
    actor: str
    role: str
    evidence: tuple[str, ...] = ()
    approval_evidence: bool = False
    homologation_evidence: bool = False
    sanitized: bool = False
    genealogy_valid: bool = False
    same_hash: bool = False
    security_passed: bool = False
    tenant_isolated: bool = False
    rollback_ready: bool = False
    secrets_detected: bool = False
    dependencies_known: bool = False
    required_human_approval: bool = False


@dataclass(frozen=True)
class ArtifactRecord:
    artifact_id: str
    version: str
    payload: Mapping[str, Any]
    source: str
    actor: str
    classification: str
    epistemic_state: str
    created_at: str
    sha256: str
    parent_ids: tuple[str, ...] = ()
    status: str = "ACTIVE"
    supersedes: str | None = None


@dataclass(frozen=True)
class GenealogyRecord:
    record_id: str
    artifact_id: str
    version: str
    parent_ids: tuple[str, ...]
    source: str
    transformation: str
    destination: str
    actor: str
    classification: str
    epistemic_state: str
    sha256: str
    created_at: str
    status: str = "ACTIVE"
    supersedes: str | None = None

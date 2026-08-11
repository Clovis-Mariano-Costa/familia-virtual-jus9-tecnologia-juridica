"""Backend acadêmico mínimo: estados, genealogia/hash e gates fail-closed."""

from .api import AcademicBackend
from .asm import AcademicState, AcademicStateMachine, TransitionError
from .gates import GateContext, GateDecision, GateValidator
from .ghr import GenealogyLedger, HashConflictError
from .security import (
    ContentReview,
    CyberSecurityContext,
    CyberSecurityGate,
    KillSwitch,
    PromptInjectionGuard,
    RIBRecord,
    RIBValidator,
    SanitizedAuditLog,
    SecurityDecision,
)
from .provenance import (
    ArtifactState,
    EpistemicState,
    Nature,
    ProvenanceError,
    ProvenanceRecord,
    ProvenanceRegistry,
    reproducible_demo,
)

__all__ = [
    "AcademicBackend",
    "AcademicState",
    "AcademicStateMachine",
    "TransitionError",
    "GateContext",
    "GateDecision",
    "GateValidator",
    "GenealogyLedger",
    "HashConflictError",
    "ContentReview",
    "CyberSecurityContext",
    "CyberSecurityGate",
    "KillSwitch",
    "PromptInjectionGuard",
    "RIBRecord",
    "RIBValidator",
    "SanitizedAuditLog",
    "SecurityDecision",
    "ArtifactState",
    "EpistemicState",
    "Nature",
    "ProvenanceError",
    "ProvenanceRecord",
    "ProvenanceRegistry",
    "reproducible_demo",
]

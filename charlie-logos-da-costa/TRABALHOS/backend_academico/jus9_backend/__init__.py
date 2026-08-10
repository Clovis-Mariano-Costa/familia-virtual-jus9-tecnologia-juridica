"""Backend acadêmico mínimo: estados, genealogia/hash e gates fail-closed."""

from .api import AcademicBackend
from .asm import AcademicState, AcademicStateMachine, TransitionError
from .gates import GateContext, GateDecision, GateValidator
from .ghr import GenealogyLedger, HashConflictError

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
]

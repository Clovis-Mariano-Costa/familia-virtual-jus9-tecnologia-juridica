from __future__ import annotations

from dataclasses import replace
from enum import Enum
from itertools import count

from .models import AcademicEvent, TransitionRequest


class AcademicState(str, Enum):
    M00 = "M00_RASCUNHO_DIDATICO_INTERNO"
    M01 = "M01_RASCUNHO_CLASSIFICADO"
    M02 = "M02_MATERIAL_DE_AULA_INTERNO"
    M03 = "M03_MATERIAL_DE_ESTUDO_REFERENCIADO"
    M04 = "M04_MATERIAL_REVISADO"
    M05 = "M05_MATERIAL_COM_ANTITESE_E_CONTRAEXEMPLOS"
    M06 = "M06_PROJETO_ACADEMICO"
    M07 = "M07_PROJETO_ORIENTADO"
    M08 = "M08_PROJETO_APROVADO_PARA_EXECUCAO"
    M09 = "M09_PROTOCOLO_PRE_REGISTRADO"
    M10 = "M10_EXECUCAO_CONTROLADA"
    M11 = "M11_RESULTADOS_PRELIMINARES"
    M12 = "M12_RESULTADOS_REPRODUZIDOS_OU_REVISADOS"
    M13 = "M13_MANUSCRITO_PRE_BANCA"
    M14 = "M14_SUBMETIDO_A_BANCA"
    M15 = "M15_BANCA_COM_EXIGENCIAS"
    M16 = "M16_APROVADO_PELA_BANCA"
    M17 = "M17_CORRIGIDO_POS_BANCA"
    M18 = "M18_HOMOLOGADO_INTERNAMENTE"
    M19 = "M19_SANITIZADO_PARA_PUBLICACAO"
    M20 = "M20_DEPOSITO_BIBLIOTECARIO_PENDENTE"
    M21 = "M21_PUBLICACAO_BIBLIOTECA_AUTORIZADA"
    M22 = "M22_PUBLICADO_NA_BIBLIOTECA"
    M23 = "M23_REVISAO_POS_PUBLICACAO"


class TransitionError(ValueError):
    pass


_SEQUENCE = list(AcademicState)
_ALLOWED: dict[AcademicState, set[AcademicState]] = {
    state: {_SEQUENCE[index + 1]} for index, state in enumerate(_SEQUENCE[:-1])
}
_ALLOWED[AcademicState.M14] = {AcademicState.M15, AcademicState.M16}
_ALLOWED[AcademicState.M15] = {AcademicState.M17}
_ALLOWED[AcademicState.M16] = {AcademicState.M17}


def _required_roles(target: AcademicState) -> set[str]:
    if target in {AcademicState.M08, AcademicState.M09, AcademicState.M10, AcademicState.M11, AcademicState.M12}:
        return {"REITORIA", "DIRECAO_ACADEMICA", "ORIENTADOR", "CODEX_TECNICO"}
    if target in {AcademicState.M14, AcademicState.M15, AcademicState.M16, AcademicState.M17}:
        return {"AVALIADOR_INTERNO", "AVALIADOR_EXTERNO", "ORIENTADOR", "REITORIA"}
    if target == AcademicState.M18:
        return {"HOMOLOGADOR", "REITORIA"}
    if target in {AcademicState.M19, AcademicState.M20, AcademicState.M21, AcademicState.M22}:
        return {"BIBLIOTECARIO_IA", "EDITOR_IA", "HOMOLOGADOR"}
    return {"AUTOR_FUNCIONAL", "EDITOR_IA", "CODEX_TECNICO", "ORIENTADOR", "REITORIA"}


class AcademicStateMachine:
    def __init__(self) -> None:
        self._events: list[AcademicEvent] = []
        self._current: dict[str, AcademicState] = {}
        self._ids = count(1)

    def current_state(self, artifact_id: str) -> AcademicState:
        return self._current.get(artifact_id, AcademicState.M00)

    def events(self, artifact_id: str | None = None) -> tuple[AcademicEvent, ...]:
        if artifact_id is None:
            return tuple(self._events)
        return tuple(event for event in self._events if event.artifact_id == artifact_id)

    def transition(self, artifact_id: str, target: AcademicState, request: TransitionRequest) -> AcademicEvent:
        current = self.current_state(artifact_id)
        if target not in _ALLOWED.get(current, set()):
            raise TransitionError(f"transition blocked: {current.value} -> {target.value}")
        if request.role not in _required_roles(target):
            raise TransitionError(f"role {request.role} cannot promote to {target.value}")
        event = AcademicEvent(
            event_id=f"evt-{next(self._ids):06d}",
            artifact_id=artifact_id,
            from_state=current.value,
            to_state=target.value,
            actor=request.actor,
            role=request.role,
            evidence=request.evidence,
            version=request.version,
            timestamp=request.timestamp,
            classification=request.classification,
            risk=request.risk,
            justification=request.justification,
            result="ACCEPTED",
            rollback=request.rollback,
        )
        self._events.append(event)
        self._current[artifact_id] = target
        return event

    def rollback(self, event_id: str, request: TransitionRequest) -> AcademicEvent:
        original = next((event for event in self._events if event.event_id == event_id), None)
        if original is None:
            raise TransitionError(f"unknown event: {event_id}")
        if request.role not in {"CODEX_TECNICO", "HOMOLOGADOR", "REITORIA"}:
            raise TransitionError("rollback requires technical, homologating or rectoral authority")
        current = self.current_state(original.artifact_id)
        rollback_event = AcademicEvent(
            event_id=f"evt-{next(self._ids):06d}",
            artifact_id=original.artifact_id,
            from_state=current.value,
            to_state=original.from_state,
            actor=request.actor,
            role=request.role,
            evidence=request.evidence,
            version=request.version,
            timestamp=request.timestamp,
            classification=request.classification,
            risk=request.risk,
            justification=request.justification,
            result="ROLLED_BACK",
            rollback=event_id,
        )
        self._events.append(rollback_event)
        self._current[original.artifact_id] = AcademicState(original.from_state)
        return rollback_event

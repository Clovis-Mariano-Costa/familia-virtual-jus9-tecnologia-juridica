from __future__ import annotations

from dataclasses import dataclass

from .models import GateContext


@dataclass(frozen=True)
class GateDecision:
    gate: str
    allowed: bool
    reason_code: str
    reasons: tuple[str, ...]


class GateValidator:
    _publication_states = {
        "M19_SANITIZADO_PARA_PUBLICACAO",
        "M20_DEPOSITO_BIBLIOTECARIO_PENDENTE",
        "M21_PUBLICACAO_BIBLIOTECA_AUTORIZADA",
        "M22_PUBLICADO_NA_BIBLIOTECA",
    }

    def validate(self, context: GateContext) -> GateDecision:
        reasons: list[str] = []
        if not context.artifact_id.strip():
            reasons.append("artifact_id ausente")
        if not context.actor.strip() or context.role.strip().upper() in {"", "AUTOMATION", "SYSTEM"}:
            reasons.append("ator/role responsável ausente ou automático")
        if not context.evidence:
            reasons.append("evidência ausente")
        if context.secrets_detected:
            reasons.append("segredo detectado em log ou artefato")
        if context.target_state in self._publication_states:
            if not context.security_passed:
                reasons.append("gate de segurança não aprovado")
            if not context.tenant_isolated:
                reasons.append("isolamento de tenant não demonstrado")
            if not context.rollback_ready:
                reasons.append("rollback não demonstrado")
            if not context.dependencies_known:
                reasons.append("dependências da publicação desconhecidas")
            if not context.genealogy_valid:
                reasons.append("genealogia inválida ou ausente")
            if not context.sanitized:
                reasons.append("sanitização pendente")
        if context.target_state in {"M16_APROVADO_PELA_BANCA", "M18_HOMOLOGADO_INTERNAMENTE"}:
            if not context.approval_evidence:
                reasons.append("evidência de aprovação ausente")
            if not context.same_hash:
                reasons.append("avaliadores não apontam para o mesmo hash")
        if context.target_state in {"M18_HOMOLOGADO_INTERNAMENTE", "M21_PUBLICACAO_BIBLIOTECA_AUTORIZADA", "M22_PUBLICADO_NA_BIBLIOTECA"}:
            if not context.homologation_evidence:
                reasons.append("evidência de homologação ausente")
        if context.required_human_approval and context.role in {"CODEX_TECNICO", "EDITOR_IA", "BIBLIOTECARIO_IA"}:
            reasons.append("aprovação humana exigida e não demonstrada pelo ator atual")
        if reasons:
            return GateDecision("GATE_CYBERSECURITY_AND_ACADEMIC", False, "PROMOTION_BLOCKED_PENDING_EVIDENCE", tuple(reasons))
        return GateDecision("GATE_CYBERSECURITY_AND_ACADEMIC", True, "PROMOTION_ALLOWED", ())

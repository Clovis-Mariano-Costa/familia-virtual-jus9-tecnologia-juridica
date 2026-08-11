from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True)
class RIBRecord:
    """Minimal Responsible Identity Boundary record for an operation."""

    functional_identity: str
    model_version: str
    competencies: frozenset[str]
    accepted_by: str | None = None
    conflicts: tuple[str, ...] = ()
    valid: bool = True


@dataclass(frozen=True)
class SecurityDecision:
    allowed: bool
    reason_code: str
    reasons: tuple[str, ...] = ()


class RIBValidator:
    def validate(
        self,
        rib: RIBRecord | None,
        *,
        required_competency: str,
        action: str,
    ) -> SecurityDecision:
        reasons: list[str] = []
        if rib is None:
            reasons.append("RIB ausente")
        else:
            if not rib.valid:
                reasons.append("RIB inválido")
            if not rib.functional_identity.strip() or not rib.model_version.strip():
                reasons.append("identidade funcional ou versão ausente")
            if rib.accepted_by is None or not rib.accepted_by.strip():
                reasons.append("aceite humano do RIB ausente")
            if rib.conflicts:
                reasons.append("conflito declarado no RIB")
            if required_competency not in rib.competencies:
                reasons.append(f"competência ausente para {action}")
        if reasons:
            return SecurityDecision(False, "RIB_INVALID_OR_INSUFFICIENT", tuple(reasons))
        return SecurityDecision(True, "RIB_VALID", ())


@dataclass(frozen=True)
class ContentReview:
    accepted_as_data: bool
    instruction_authority: str
    quarantined: bool
    reason_code: str
    matches: tuple[str, ...] = ()


class PromptInjectionGuard:
    """Treat recovered content as data and quarantine obvious instruction attacks."""

    _patterns: tuple[tuple[str, re.Pattern[str]], ...] = (
        ("precedence_override", re.compile(r"\b(ignore|disregard|override)\b.{0,80}\b(previous|prior|system|developer)\b", re.I | re.S)),
        ("authority_spoofing", re.compile(r"\b(system message|developer message|admin instruction|root instruction)\b", re.I)),
        ("secret_exfiltration", re.compile(r"\b(reveal|print|dump|exfiltrate|send)\b.{0,80}\b(password|token|secret|private key|credential)s?\b", re.I | re.S)),
        ("safety_bypass", re.compile(r"\b(disable|bypass|circumvent)\b.{0,80}\b(safety|security|gate|policy|approval)\b", re.I | re.S)),
    )

    def review(self, content: str, *, source_trusted: bool = False) -> ContentReview:
        matches = tuple(name for name, pattern in self._patterns if pattern.search(content))
        if matches:
            return ContentReview(
                accepted_as_data=True,
                instruction_authority="NONE",
                quarantined=True,
                reason_code="UNTRUSTED_INSTRUCTION_QUARANTINED",
                matches=matches,
            )
        return ContentReview(
            accepted_as_data=True,
            instruction_authority="NONE" if not source_trusted else "SOURCE_ONLY",
            quarantined=False,
            reason_code="DATA_ONLY_NO_AUTHORITY",
        )


@dataclass(frozen=True)
class CyberSecurityContext:
    rib_valid: bool = False
    critical_vulnerabilities: int = 0
    high_vulnerabilities_without_mitigation: int = 0
    tenant_isolated: bool = False
    authentication_complete: bool = False
    authorization_complete: bool = False
    secrets_detected: bool = False
    rollback_ready: bool = False
    incident_response_ready: bool = False
    dependencies_known: bool = False
    kill_switch_engaged: bool = False


class CyberSecurityGate:
    """Fail-closed gate for security-sensitive promotion or publication."""

    def evaluate(self, context: CyberSecurityContext) -> SecurityDecision:
        reasons: list[str] = []
        if context.kill_switch_engaged:
            reasons.append("kill-switch acionado")
        if not context.rib_valid:
            reasons.append("RIB não validado")
        if context.critical_vulnerabilities > 0:
            reasons.append("vulnerabilidade crítica aberta")
        if context.high_vulnerabilities_without_mitigation > 0:
            reasons.append("vulnerabilidade alta sem mitigação comprovada")
        if not context.tenant_isolated:
            reasons.append("isolamento de tenant não demonstrado")
        if not context.authentication_complete:
            reasons.append("autenticação incompleta")
        if not context.authorization_complete:
            reasons.append("autorização incompleta")
        if context.secrets_detected:
            reasons.append("segredo detectado em log ou artefato")
        if not context.rollback_ready:
            reasons.append("rollback não demonstrado")
        if not context.incident_response_ready:
            reasons.append("resposta a incidente não exercitada")
        if not context.dependencies_known:
            reasons.append("dependências desconhecidas")
        if reasons:
            return SecurityDecision(False, "GATE_CYBERSECURITY_BLOCKED", tuple(reasons))
        return SecurityDecision(True, "GATE_CYBERSECURITY_PASSED", ())


class KillSwitch:
    def __init__(self) -> None:
        self._engaged = False
        self._reason = ""

    @property
    def engaged(self) -> bool:
        return self._engaged

    @property
    def reason(self) -> str:
        return self._reason

    def engage(self, *, actor: str, reason: str) -> None:
        if not actor.strip() or not reason.strip():
            raise ValueError("kill-switch requires accountable actor and reason")
        self._engaged = True
        self._reason = reason.strip()

    def release(self, *, actor: str, evidence: Iterable[str]) -> None:
        if actor.strip().upper() != "GUARDIAO_CIBERSEGURANCA":
            raise PermissionError("only GUARDIAO_CIBERSEGURANCA may release kill-switch")
        if not tuple(evidence):
            raise ValueError("kill-switch release requires evidence")
        self._engaged = False
        self._reason = ""


class SanitizedAuditLog:
    _secret_patterns = (
        re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+"),
        re.compile(r"(?i)((?:password|passwd|token|secret|api[_ -]?key|client[_ -]?secret)\s*[=:]\s*)[^\s,;]+"),
        re.compile(r"-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----", re.I | re.S),
    )

    def __init__(self) -> None:
        self._records: list[str] = []

    @classmethod
    def sanitize(cls, message: str) -> str:
        sanitized = message
        for pattern in cls._secret_patterns:
            sanitized = pattern.sub(lambda match: f"{match.group(1)}[REDACTED]" if match.lastindex else "[REDACTED]", sanitized)
        return sanitized

    def append(self, message: str) -> str:
        record = self.sanitize(message)
        self._records.append(record)
        return record

    def records(self) -> tuple[str, ...]:
        return tuple(self._records)

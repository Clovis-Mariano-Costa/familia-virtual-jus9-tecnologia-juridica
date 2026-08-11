from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json
import re
import unicodedata
from typing import Any, Iterable, Mapping


ALLOWED_STATES = {
    "SEMENTE_NAO_CANONICO",
    "EM_PESQUISA",
    "EM_REVISAO_ESPECIALIZADA",
    "APROVADO_PARA_CANONIZACAO",
    "CANONICO",
    "CORRIGIR",
    "FUNDIR",
    "REJEITADO",
    "HISTORICO",
    "SUPERADO_COM_GENEALOGIA",
    "REVOGADO_POR_INCOMPATIBILIDADE",
}

REQUIRED_BLOCKS = (
    "morphological_analysis",
    "etymology_phonetic_evolution",
    "historical_morphological_structure",
    "semantic_historical_change",
    "historical_morphological_summary",
)

REQUIRED_METADATA = (
    "entry_id",
    "term",
    "normalized_term",
    "version",
    "state",
    "source_refs",
    "genealogy",
)


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    entry_id: str | None = None

    def as_dict(self) -> dict[str, str | None]:
        return {"code": self.code, "message": self.message, "entry_id": self.entry_id}


def normalize_term(term: str) -> str:
    """Normalize only for comparison; preserve the original display term."""
    text = unicodedata.normalize("NFKC", str(term)).casefold()
    text = " ".join(text.split())
    return text.strip()


def stable_entry_id(term: str, source_position: int) -> str:
    material = f"500-seed:{source_position}:{normalize_term(term)}".encode("utf-8")
    return f"dict500-{sha256(material).hexdigest()[:16]}"


def _nonempty(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def _source_is_valid(source: Mapping[str, Any]) -> bool:
    return bool(str(source.get("source_id", "")).strip()) and bool(
        re.match(r"^https?://", str(source.get("url", "")))
    )


def validate_entry(entry: Mapping[str, Any], *, strict: bool = False) -> list[Issue]:
    issues: list[Issue] = []
    entry_id = str(entry.get("entry_id", "")) or None
    for field in REQUIRED_METADATA:
        if field not in entry or not _nonempty(entry.get(field)):
            issues.append(Issue("MISSING_REQUIRED_FIELD", f"campo obrigatório ausente: {field}", entry_id))

    state = str(entry.get("state", ""))
    if state and state not in ALLOWED_STATES:
        issues.append(Issue("INVALID_STATE", f"estado inválido: {state}", entry_id))

    term = str(entry.get("term", ""))
    if term and entry.get("normalized_term") != normalize_term(term):
        issues.append(Issue("NORMALIZATION_MISMATCH", "normalized_term não corresponde ao termo", entry_id))

    sources = entry.get("source_refs", [])
    if not isinstance(sources, list) or not all(isinstance(source, Mapping) for source in sources):
        issues.append(Issue("INVALID_SOURCE_LIST", "source_refs deve ser uma lista de objetos", entry_id))
    elif not sources:
        issues.append(Issue("SOURCE_PENDING", "nenhuma fonte registrada", entry_id))
    elif any(not _source_is_valid(source) for source in sources):
        issues.append(Issue("INVALID_SOURCE", "fonte sem source_id ou URL verificável", entry_id))

    genealogy = entry.get("genealogy")
    if not isinstance(genealogy, Mapping) or "parents" not in genealogy:
        issues.append(Issue("INVALID_GENEALOGY", "genealogia precisa declarar parents", entry_id))

    if state == "CANONICO" or strict:
        for field in REQUIRED_BLOCKS:
            if not _nonempty(entry.get(field)):
                issues.append(Issue("CANONICAL_FIELD_MISSING", f"bloco canônico ausente: {field}", entry_id))
        review = entry.get("review", {})
        if not isinstance(review, Mapping):
            issues.append(Issue("REVIEW_MISSING", "revisão independente ausente", entry_id))
        else:
            if review.get("linguistic") != "APPROVED":
                issues.append(Issue("LINGUISTIC_REVIEW_MISSING", "revisão linguística independente ausente", entry_id))
            if review.get("specialized") != "APPROVED":
                issues.append(Issue("SPECIALIZED_REVIEW_MISSING", "revisão especializada independente ausente", entry_id))
            if review.get("human_approval") != "APPROVED":
                issues.append(Issue("HUMAN_APPROVAL_MISSING", "aprovação humana competente ausente", entry_id))
        genealogy = entry.get("genealogy")
        if not isinstance(genealogy, Mapping) or not genealogy.get("verified", False):
            issues.append(Issue("GENEALOGY_UNVERIFIED", "genealogia não verificada", entry_id))

    return issues


def duplicate_groups(entries: Iterable[Mapping[str, Any]]) -> list[list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for entry in entries:
        groups[normalize_term(str(entry.get("term", "")))].append(str(entry.get("entry_id", "")))
    return [ids for ids in groups.values() if len(ids) > 1]


def genealogy_records(entries: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for entry in entries:
        payload = deepcopy(dict(entry))
        records.append(
            {
                "entry_id": entry.get("entry_id"),
                "version": entry.get("version"),
                "parents": list(entry.get("genealogy", {}).get("parents", [])),
                "source_refs": deepcopy(entry.get("source_refs", [])),
                "transformation": "INGEST_SEED_CORPUS",
                "destination": "dictionary_pipeline",
                "state": entry.get("state"),
                "payload_sha256": sha256(
                    json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
                ).hexdigest(),
            }
        )
    return records


def validate_corpus(corpus: Mapping[str, Any]) -> dict[str, Any]:
    entries = corpus.get("entries", [])
    issues: list[Issue] = []
    if not isinstance(entries, list):
        issues.append(Issue("INVALID_CORPUS", "entries deve ser uma lista"))
        entries = []

    expected_total = corpus.get("expected_total", 500)
    if len(entries) != expected_total:
        issues.append(Issue("TOTAL_MISMATCH", f"esperadas {expected_total} entradas; encontradas {len(entries)}"))

    ids = [str(entry.get("entry_id", "")) for entry in entries if isinstance(entry, Mapping)]
    for entry_id, count in Counter(ids).items():
        if not entry_id or count > 1:
            issues.append(Issue("DUPLICATE_ENTRY_ID", f"identificador repetido ou vazio: {entry_id}"))

    entry_issues = [issue for entry in entries if isinstance(entry, Mapping) for issue in validate_entry(entry)]
    issues.extend(entry_issues)
    duplicate_terms = duplicate_groups(entries)
    canonical_entries = sum(1 for entry in entries if entry.get("state") == "CANONICO")
    coverage_missing = Counter(
        field
        for entry in entries
        for field in REQUIRED_BLOCKS
        if not _nonempty(entry.get(field))
    )
    incomplete_entries = sum(
        any(not _nonempty(entry.get(field)) for field in REQUIRED_BLOCKS)
        for entry in entries
    )
    missing_blocks = Counter(
        issue.message.split(": ", 1)[-1]
        for issue in entry_issues
        if issue.code == "CANONICAL_FIELD_MISSING"
    )

    fatal_codes = {"INVALID_CORPUS", "TOTAL_MISMATCH", "DUPLICATE_ENTRY_ID", "INVALID_STATE", "INVALID_SOURCE", "INVALID_SOURCE_LIST", "INVALID_GENEALOGY"}
    fatal = any(issue.code in fatal_codes for issue in issues)
    return {
        "valid_shape": not fatal,
        "expected_total": expected_total,
        "total": len(entries),
        "state_counts": dict(Counter(str(entry.get("state")) for entry in entries)),
        "canonical_entries": canonical_entries,
        "duplicate_term_groups": duplicate_terms,
        "incomplete_entry_count": incomplete_entries,
        "coverage_missing_fields": dict(coverage_missing),
        "missing_canonical_blocks": dict(missing_blocks),
        "issue_count": len(issues),
        "fatal_issue_count": sum(issue.code in fatal_codes for issue in issues),
        "issues": [issue.as_dict() for issue in issues],
    }


def promote(entry: Mapping[str, Any], *, target_state: str, evidence: Mapping[str, Any]) -> dict[str, Any]:
    """Return a new entry only when the target gate is satisfied."""
    if target_state not in ALLOWED_STATES:
        raise ValueError(f"estado inválido: {target_state}")
    candidate = deepcopy(dict(entry))
    candidate["state"] = target_state
    issues = validate_entry(candidate, strict=target_state == "CANONICO")
    if target_state == "CANONICO":
        if evidence.get("independent_reviewers", 0) < 2:
            issues.append(Issue("INDEPENDENT_REVIEW_MISSING", "são necessários dois revisores independentes", entry.get("entry_id")))
        if evidence.get("human_approval") is not True:
            issues.append(Issue("HUMAN_APPROVAL_MISSING", "aprovação humana não comprovada", entry.get("entry_id")))
    if issues:
        raise ValueError("PROMOTION_BLOCKED_PENDING_EVIDENCE: " + "; ".join(issue.code for issue in issues))
    return candidate

"""Validation only: never counts, promulgates, mutates or deletes source data."""

from __future__ import annotations

import hashlib
import posixpath
from collections import Counter

ALLOWED_TRANSITIONS = {
    "RASCUNHO": {"QUARENTENA", "EM_REVISAO"},
    "QUARENTENA": {"RECUPERADO", "EM_REVISAO"},
    "RECUPERADO": {"EM_REVISAO"},
    "EM_REVISAO": {"PARA_VISTAS", "HISTORICO"},
    "PARA_VISTAS": {"APROVADO_NAO_PROMULGADO", "HISTORICO"},
    "APROVADO_NAO_PROMULGADO": {"HISTORICO"},
    "VIGENTE": {"VIGENTE_EM_TRANSICAO", "REVOGADO", "SUPERADO_COM_RASTRO"},
    "VIGENTE_EM_TRANSICAO": {"VIGENTE", "REVOGADO", "SUPERADO_COM_RASTRO"},
    "HISTORICO": set(), "SUPERADO_COM_RASTRO": set(), "REVOGADO": set(),
    "SEM_ESTADO_CONFIRMADO": {"EM_REVISAO", "HISTORICO"},
}


def validate_manifest(manifest: dict, files: dict[str, bytes]) -> dict:
    entries = manifest.get("files", [])
    expected = {str(entry.get("name")): str(entry.get("sha256", "")).lower() for entry in entries}
    actual = {str(name): hashlib.sha256(data).hexdigest() for name, data in files.items()}
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    mismatched = sorted(name for name in set(expected) & set(actual) if expected[name] != actual[name])
    codes = {str(entry.get("code")) for entry in entries if entry.get("code")}
    versions = {str(entry.get("version")) for entry in entries if entry.get("version")}
    declared_hashes = {str(entry.get("sha256")).lower() for entry in entries if entry.get("sha256")}
    return {
        "dry_run": True, "valid": not (missing or extra or mismatched) and len(codes) <= 1 and len(versions) <= 1 and len(declared_hashes) == len(entries),
        "missing": missing, "extra": extra, "mismatched": mismatched,
        "common_code": sorted(codes), "common_version": sorted(versions), "manifest_entries": len(entries),
        "writes": 0, "promulgation": False, "vote_count": None,
    }


def validate_votes(package: dict) -> dict:
    votes = package.get("votes", [])
    identities = [vote.get("identity") for vote in votes]
    declarations = [vote.get("declaration") for vote in votes]
    duplicate_identities = sorted(identity for identity, count in Counter(identities).items() if identity and count > 1)
    denominator = package.get("denominator")
    errors = []
    if duplicate_identities:
        errors.append("duplicate_identity")
    if any(not declaration for declaration in declarations):
        errors.append("missing_declaration")
    if denominator is not None and len(votes) > int(denominator):
        errors.append("votes_exceed_denominator")
    return {"valid": not errors, "errors": errors, "duplicate_identities": duplicate_identities, "votes_seen": len(votes), "denominator": denominator, "vote_count": None, "promulgated": False}


def validate_transition(current: str, proposed: str, *, human_gate: bool = False) -> dict:
    errors = []
    if proposed not in ALLOWED_TRANSITIONS.get(current, set()):
        errors.append("forbidden_transition")
    if proposed in {"VIGENTE", "REVOGADO"}:
        errors.append("normative_effect_blocked")
    if human_gate:
        errors.append("human_gate_is_not_automatically_consumed")
    return {"valid": not errors, "current": current, "proposed": proposed, "errors": errors, "dry_run": True}


def safe_zip_members(names: list[str]) -> dict:
    unsafe = sorted(name for name in names if posixpath.isabs(name) or ".." in posixpath.normpath(name).split("/") or "\\" in name)
    return {"safe": not unsafe, "unsafe": unsafe}

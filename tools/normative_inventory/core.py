"""Offline, deterministic and read-only normative inventory primitives."""

from __future__ import annotations

import hashlib
import json
import mimetypes
import re
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping

NORMATIVE_STATES = (
    "RASCUNHO", "QUARENTENA", "RECUPERADO", "EM_REVISAO", "PARA_VISTAS",
    "APROVADO_NAO_PROMULGADO", "VIGENTE", "VIGENTE_EM_TRANSICAO",
    "HISTORICO", "SUPERADO_COM_RASTRO", "REVOGADO", "SEM_ESTADO_CONFIRMADO",
)
_CODE = re.compile(r"\b(?:[A-Z]{2,}[A-Z0-9-]*\d[A-Z0-9-]*|[A-Z]{2,}-\d{2,})\b")
_VERSION = re.compile(r"\b(?:v(?:ers(?:ao|ion)?)[ ._-]*|ver[ ._-]*)?\d+(?:[._]\d+){0,3}\b", re.I)
_DATE = re.compile(r"\b(20\d{2}[-_]\d{2}[-_]\d{2}|\d{2}[-_]\d{2}[-_]20\d{2})\b")
_HASH = re.compile(r"\b(?:sha-?256[:= ]*)?([a-f0-9]{64})\b", re.I)
_STATE = re.compile(r"\b(?:estado|status|state)\s*[:=]\s*([A-Z_]+)\b", re.I)
_AUTHORITY = re.compile(r"\b(?:autoridade|authority|competente)\s*[:=]\s*([^\n;]+)", re.I)
_RELATION = re.compile(r"\b(substitui|substitutes|complementa|complements|revoga|revokes|sucessor(?:a)?|successor)\s*[:=]\s*([^\n;]+)", re.I)


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _ascii(value: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", value) if not unicodedata.combining(ch))


def normalize_name(value: str) -> str:
    value = _ascii(Path(value).name).casefold()
    value = re.sub(r"\.[a-z0-9]{1,8}$", "", value)
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def _first(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1) if pattern.groups else match.group(0)


def classify_candidate(name: str, text: str = "") -> str:
    sample = f"{name} {text[:12000]}".casefold()
    if any(word in sample for word in ("constituição", "constituicao", "emenda", "juramento-raiz", "normativo", "regulamento")):
        return "NORMATIVO_CANDIDATO"
    if any(word in sample for word in ("pedido", "programar", "implementação", "implementacao", "backlog")):
        return "PEDIDO_DE_PROGRAMACAO"
    return "DOCUMENTO_AUXILIAR"


def _state_from_text(text: str) -> str:
    candidate = _first(_STATE, text)
    if candidate:
        candidate = _ascii(candidate).upper()
        if candidate in NORMATIVE_STATES:
            return candidate
    upper = _ascii(text).upper()
    for state in sorted(NORMATIVE_STATES, key=len, reverse=True):
        if state in upper:
            return state
    return "SEM_ESTADO_CONFIRMADO"


def extract_metadata(name: str, text: str = "") -> dict[str, object]:
    sample = f"{name}\n{text[:20000]}"
    return {
        "code": _first(_CODE, sample),
        "version": _first(_VERSION, sample),
        "declared_hash": (_first(_HASH, sample) or "").lower() or None,
        "date": _first(_DATE, sample),
        "authority": (_first(_AUTHORITY, sample) or "").strip() or None,
        "state": _state_from_text(sample),
        "relations": [{"kind": m.group(1).upper(), "target": m.group(2).strip()} for m in _RELATION.finditer(sample)],
    }


def sensitive_marker(name: str, text: str = "") -> str:
    sample = f"{name}\n{text[:4000]}".casefold()
    return "SENSITIVE_REVIEW_REQUIRED" if any(token in sample for token in ("senha", "password", "token", "api_key", "private key", "cofre", "segredo")) else "NONE"


def _safe_text(path: Path) -> str:
    if path.suffix.casefold() not in {".md", ".txt", ".csv", ".json", ".yaml", ".yml"}:
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _iter_files(roots: Iterable[str | Path]) -> list[Path]:
    result: list[Path] = []
    for raw_root in roots:
        root = Path(raw_root)
        if root.is_file():
            result.append(root)
        elif root.is_dir():
            result.extend(path for path in root.rglob("*") if path.is_file() and not any(part in {".git", ".pytest_cache", "__pycache__", "node_modules"} for part in path.parts))
    return sorted(set(result), key=lambda path: str(path).casefold())


def _item_for_file(path: Path, root: Path | None, source: str) -> dict[str, object]:
    data = path.read_bytes()
    text = _safe_text(path)
    relative = str(path.relative_to(root)) if root and path.is_relative_to(root) else str(path)
    return {
        "source": source, "path": relative.replace("\\", "/"), "name": path.name,
        "normalized_name": normalize_name(path.name), "size_bytes": len(data),
        "mime": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        "sha256": hash_bytes(data), "metadata": extract_metadata(path.name, text),
        "classification": classify_candidate(path.name, text), "sensitive_marker": sensitive_marker(path.name, text),
    }


def _groups(items: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    by_hash: dict[str, list[str]] = defaultdict(list)
    by_shape: dict[str, list[str]] = defaultdict(list)
    for item in items:
        by_hash[str(item["sha256"])].append(str(item["path"]))
        by_shape[f"{item['normalized_name']}|{item['size_bytes']}|{item['mime']}"] .append(str(item["path"]))
    exact = [{"sha256": key, "paths": sorted(paths)} for key, paths in sorted(by_hash.items()) if len(paths) > 1]
    probable = [{"signature": key, "paths": sorted(paths)} for key, paths in sorted(by_shape.items()) if len(paths) > 1]
    return exact, probable


def build_inventory(roots: Iterable[str | Path], *, source: str = "LOCAL_CHECKOUT", generated_at: str | None = None) -> dict[str, object]:
    roots = [Path(root) for root in roots]
    root = roots[0] if len(roots) == 1 and roots[0].is_dir() else None
    items = [_item_for_file(path, root, source) for path in _iter_files(roots)]
    exact, probable = _groups(items)
    return {
        "schema": "normative-inventory-v1", "generated_at": generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "read_only": True, "roots": [str(root) for root in roots], "items": items,
        "duplicate_groups": {"exact": exact, "probable": probable},
        "summary": {"files": len(items), "unique_sha256": len({item["sha256"] for item in items}), "sensitive_marked": sum(item["sensitive_marker"] != "NONE" for item in items)},
    }


def compare_inventories(current: Mapping[str, object], previous: Mapping[str, object]) -> dict[str, object]:
    def keyed(inventory: Mapping[str, object]) -> dict[tuple[str, str], Mapping[str, object]]:
        return {(str(item.get("source")), str(item.get("path"))): item for item in inventory.get("items", [])}  # type: ignore[union-attr]
    before, after = keyed(previous), keyed(current)
    return {
        "added": [list(key) for key in sorted(set(after) - set(before))],
        "removed": [list(key) for key in sorted(set(before) - set(after))],
        "changed": [list(key) for key in sorted(set(before) & set(after)) if before[key].get("sha256") != after[key].get("sha256")],
    }


def build_norm_matrix(inventory: Mapping[str, object]) -> list[dict[str, object]]:
    rows = []
    for item in inventory.get("items", []):  # type: ignore[union-attr]
        metadata = item.get("metadata", {})
        rows.append({"path": item.get("path"), "code": metadata.get("code"), "version": metadata.get("version"), "state": metadata.get("state"), "authority": metadata.get("authority"), "sha256": item.get("sha256"), "classification": item.get("classification"), "sensitive_marker": item.get("sensitive_marker")})
    return sorted(rows, key=lambda row: str(row["path"]).casefold())

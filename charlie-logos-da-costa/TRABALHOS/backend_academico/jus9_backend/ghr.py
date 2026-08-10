from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from itertools import count
from typing import Any, Mapping

from .models import GenealogyRecord, utc_timestamp


class HashConflictError(ValueError):
    pass


def canonical_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_payload(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


class GenealogyLedger:
    def __init__(self) -> None:
        self._records: list[GenealogyRecord] = []
        self._ids = count(1)

    def records(self, artifact_id: str | None = None) -> tuple[GenealogyRecord, ...]:
        if artifact_id is None:
            return tuple(self._records)
        return tuple(record for record in self._records if record.artifact_id == artifact_id)

    def append(
        self,
        *,
        artifact_id: str,
        version: str,
        payload: Mapping[str, Any],
        source: str,
        transformation: str,
        destination: str,
        actor: str,
        classification: str,
        epistemic_state: str,
        parent_ids: tuple[str, ...] = (),
        supersedes: str | None = None,
    ) -> GenealogyRecord:
        digest = sha256_payload(payload)
        same_version = [r for r in self._records if r.artifact_id == artifact_id and r.version == version and r.status == "ACTIVE"]
        if same_version and any(r.sha256 != digest for r in same_version):
            raise HashConflictError(f"hash divergence for {artifact_id} version {version}")
        known_ids = {r.record_id for r in self._records}
        if any(parent not in known_ids for parent in parent_ids):
            raise ValueError("all parent records must exist before a child is appended")
        record = GenealogyRecord(
            record_id=f"ghr-{next(self._ids):06d}",
            artifact_id=artifact_id,
            version=version,
            parent_ids=parent_ids,
            source=source,
            transformation=transformation,
            destination=destination,
            actor=actor,
            classification=classification,
            epistemic_state=epistemic_state,
            sha256=digest,
            created_at=utc_timestamp(),
            supersedes=supersedes,
        )
        self._records.append(record)
        return record

    def tombstone(self, record_id: str, *, actor: str, reason: str) -> GenealogyRecord:
        original = next((r for r in self._records if r.record_id == record_id), None)
        if original is None:
            raise ValueError(f"unknown genealogy record: {record_id}")
        tombstone = GenealogyRecord(
            record_id=f"ghr-{next(self._ids):06d}",
            artifact_id=original.artifact_id,
            version=original.version,
            parent_ids=(original.record_id,),
            source=original.source,
            transformation=f"TOMBSTONE: {reason}",
            destination=original.destination,
            actor=actor,
            classification=original.classification,
            epistemic_state=original.epistemic_state,
            sha256=original.sha256,
            created_at=utc_timestamp(),
            status="REVOKED",
            supersedes=original.record_id,
        )
        self._records.append(tombstone)
        return tombstone

    @staticmethod
    def verify(payload: Mapping[str, Any], expected_sha256: str) -> bool:
        return sha256_payload(payload) == expected_sha256

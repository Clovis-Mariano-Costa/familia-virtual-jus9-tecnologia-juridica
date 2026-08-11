from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Iterable, Mapping

from .pipeline import duplicate_groups, normalize_term


def triage_corpus(entries: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    items = list(entries)
    by_term: dict[str, list[str]] = defaultdict(list)
    for entry in items:
        by_term[normalize_term(str(entry.get("term", "")))].append(str(entry.get("entry_id", "")))

    decisions: list[dict[str, Any]] = []
    for entry in items:
        normalized = normalize_term(str(entry.get("term", "")))
        duplicate = len(by_term[normalized]) > 1
        decisions.append(
            {
                "entry_id": entry.get("entry_id"),
                "term": entry.get("term"),
                "current_state": entry.get("state"),
                "decision": "DUPLICATA_POTENCIAL" if duplicate else "EM_PESQUISA",
                "reason": (
                    "normalização encontrou outro identificador; exigir decisão de fundir ou manter"
                    if duplicate
                    else "semente exige fontes independentes, ficha completa e revisão especializada"
                ),
                "related_entry_ids": by_term[normalized] if duplicate else [],
            }
        )

    return {
        "total": len(items),
        "decision_counts": dict(Counter(item["decision"] for item in decisions)),
        "duplicate_groups": duplicate_groups(items),
        "decisions": decisions,
    }

"""Validação governada de sementes de dicionário."""

from .pipeline import (
    ALLOWED_STATES,
    REQUIRED_BLOCKS,
    duplicate_groups,
    genealogy_records,
    promote,
    validate_corpus,
    validate_entry,
)
from .triage import triage_corpus

__all__ = [
    "ALLOWED_STATES",
    "REQUIRED_BLOCKS",
    "duplicate_groups",
    "genealogy_records",
    "promote",
    "validate_corpus",
    "validate_entry",
    "triage_corpus",
]

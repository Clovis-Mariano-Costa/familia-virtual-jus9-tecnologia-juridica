from __future__ import annotations

import json
from pathlib import Path
import unittest

from dictionary_pipeline import duplicate_groups, genealogy_records, promote, triage_corpus, validate_corpus


ROOT = Path(__file__).resolve().parents[1]


class DictionaryPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = json.loads((ROOT / "data" / "lote_500_sementes.json").read_text(encoding="utf-8"))

    def test_lote_has_500_noncanonical_entries(self) -> None:
        self.assertEqual(self.corpus["expected_total"], 500)
        self.assertEqual(len(self.corpus["entries"]), 500)
        self.assertTrue(all(entry["state"] == "SEMENTE_NAO_CANONICO" for entry in self.corpus["entries"]))

    def test_shape_is_valid_and_incompleteness_is_visible(self) -> None:
        report = validate_corpus(self.corpus)
        self.assertTrue(report["valid_shape"])
        self.assertEqual(report["canonical_entries"], 0)
        self.assertEqual(report["incomplete_entry_count"], 500)
        self.assertEqual(report["coverage_missing_fields"]["morphological_analysis"], 500)
        self.assertEqual(report["fatal_issue_count"], 0)

    def test_duplicate_detection_is_normalized(self) -> None:
        entries = [{"entry_id": "a", "term": "  Alpha  "}, {"entry_id": "b", "term": "alpha"}]
        self.assertEqual(duplicate_groups(entries), [["a", "b"]])

    def test_genealogy_is_reproducible(self) -> None:
        records = genealogy_records(self.corpus["entries"][:2])
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["transformation"], "INGEST_SEED_CORPUS")
        self.assertEqual(records[0]["parents"], [])
        self.assertTrue(records[0]["payload_sha256"])

    def test_canonical_promotion_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "PROMOTION_BLOCKED_PENDING_EVIDENCE"):
            promote(self.corpus["entries"][0], target_state="CANONICO", evidence={})

    def test_canonical_promotion_requires_independent_reviewers(self) -> None:
        entry = dict(self.corpus["entries"][0])
        entry.update(
            {
                "morphological_analysis": "documented",
                "etymology_phonetic_evolution": "documented",
                "historical_morphological_structure": "documented",
                "semantic_historical_change": "documented",
                "historical_morphological_summary": "documented",
                "review": {"linguistic": "APPROVED", "specialized": "APPROVED", "human_approval": "APPROVED"},
                "genealogy": {"parents": [], "verified": True},
            }
        )
        with self.assertRaisesRegex(ValueError, "INDEPENDENT_REVIEW_MISSING"):
            promote(entry, target_state="CANONICO", evidence={"human_approval": True, "independent_reviewers": 1})

    def test_canonical_promotion_succeeds_only_with_all_gates(self) -> None:
        entry = dict(self.corpus["entries"][0])
        entry.update(
            {
                "morphological_analysis": "documented",
                "etymology_phonetic_evolution": "documented",
                "historical_morphological_structure": "documented",
                "semantic_historical_change": "documented",
                "historical_morphological_summary": "documented",
                "review": {"linguistic": "APPROVED", "specialized": "APPROVED", "human_approval": "APPROVED"},
                "genealogy": {"parents": [], "verified": True},
            }
        )
        promoted = promote(entry, target_state="CANONICO", evidence={"human_approval": True, "independent_reviewers": 2})
        self.assertEqual(promoted["state"], "CANONICO")

    def test_triage_keeps_all_seeds_in_research(self) -> None:
        report = triage_corpus(self.corpus["entries"])
        self.assertEqual(report["total"], 500)
        self.assertEqual(report["decision_counts"], {"EM_PESQUISA": 500})
        self.assertEqual(report["duplicate_groups"], [])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
from pathlib import Path

from dictionary_pipeline import validate_corpus


ROOT = Path(__file__).resolve().parent


def main() -> int:
    corpus = json.loads((ROOT / "data" / "lote_500_sementes.json").read_text(encoding="utf-8"))
    report = validate_corpus(corpus)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid_shape"] and report["canonical_entries"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

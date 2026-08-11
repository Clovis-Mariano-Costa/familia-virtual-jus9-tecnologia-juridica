from __future__ import annotations

import json
from pathlib import Path

from dictionary_pipeline.triage import triage_corpus


ROOT = Path(__file__).resolve().parent


def main() -> int:
    corpus = json.loads((ROOT / "data" / "lote_500_sementes.json").read_text(encoding="utf-8"))
    print(json.dumps(triage_corpus(corpus["entries"]), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

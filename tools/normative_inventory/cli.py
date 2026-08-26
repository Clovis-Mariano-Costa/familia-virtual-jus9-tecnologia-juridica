"""Command line entrypoint; output is confined to the explicit output folder."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .core import build_inventory, build_norm_matrix, canonical_json, compare_inventories


def _csv_safe(value: object) -> str:
    text = str(value if value is not None else "")
    if text.startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MJ9 read-only normative inventory")
    parser.add_argument("--root", action="append", required=True, help="local root (repeatable)")
    parser.add_argument("--output", required=True, help="new/generated output directory")
    parser.add_argument("--previous", help="previous generated inventory JSON")
    args = parser.parse_args(argv)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    inventory = build_inventory(args.root)
    if args.previous:
        previous = json.loads(Path(args.previous).read_text(encoding="utf-8"))
        inventory["diff"] = compare_inventories(inventory, previous)
    (output / "inventory.json").write_text(canonical_json(inventory) + "\n", encoding="utf-8")
    (output / "norm-matrix.json").write_text(canonical_json(build_norm_matrix(inventory)) + "\n", encoding="utf-8")
    with (output / "norm-matrix.csv").open("w", encoding="utf-8", newline="") as handle:
        rows = build_norm_matrix(inventory)
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["path"])
        writer.writeheader()
        writer.writerows({key: _csv_safe(value) for key, value in row.items()} for row in rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

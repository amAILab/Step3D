#!/usr/bin/env python3
"""Export Step3D content registry from Google Sheet.

Default is --dry-run metadata only. Use --out to save fetched tabs as JSON.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "data" / "content_sheet_config.json").read_text(encoding="utf-8"))


def read_range(range_name: str) -> dict[str, Any]:
    params = {"spreadsheetId": CONFIG["spreadsheetId"], "range": range_name}
    proc = subprocess.run(["gws", "sheets", "spreadsheets", "values", "get", "--params", json.dumps(params, ensure_ascii=False)], text=True, capture_output=True, check=True)
    return json.loads(proc.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="write exported content JSON to path")
    parser.add_argument("--dry-run", action="store_true", help="print planned tabs without calling Sheets")
    args = parser.parse_args()
    if args.dry_run or not args.out:
        print(json.dumps({"ok": True, "dryRun": True, "sheet": CONFIG["spreadsheetUrl"], "tabs": CONFIG["tabs"]}, ensure_ascii=False, indent=2))
        return 0
    data = {name: read_range(rng).get("values", []) for name, rng in CONFIG["tabs"].items()}
    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"sheet": CONFIG["spreadsheetUrl"], "tabs": data}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(out), "tabs": list(data)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

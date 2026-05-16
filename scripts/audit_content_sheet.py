#!/usr/bin/env python3
"""Audit Step3D Google Sheet CRM/CMS structure and minimal completeness."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "data" / "content_sheet_config.json").read_text(encoding="utf-8"))
SPREADSHEET_ID = CONFIG["spreadsheetId"]
REQUIRED = {
    "Settings": {"range": "Settings!A1:C200", "min_rows": 6, "headers": ["key", "value", "notes"]},
    "Content": {"range": "Content!A1:K200", "min_rows": 8, "headers": ["id", "type", "status", "title", "section_or_url", "draft", "final_text", "cta", "keywords", "owner", "updatedAt"]},
    "Cases": {"range": "Cases!A1:J200", "min_rows": 4, "headers": ["id", "status", "title", "url", "problem", "solution", "result", "media", "cta", "updatedAt"]},
    "FAQ": {"range": "FAQ!A1:H200", "min_rows": 8, "headers": ["id", "status", "question", "answer", "page", "schema", "owner", "updatedAt"]},
    "Pages": {"range": "Pages!A1:J200", "min_rows": 25, "headers": ["url", "status", "title", "h1", "description", "target_keyword", "cta", "source_file", "last_checked", "notes"]},
    "Backlog": {"range": "Backlog!A1:H200", "min_rows": 8, "headers": ["id", "status", "priority", "area", "task", "reason", "owner", "createdAt"]},
}


def gws_get(range_name: str) -> list[list[str]]:
    params = json.dumps({"spreadsheetId": SPREADSHEET_ID, "range": range_name}, ensure_ascii=False)
    proc = subprocess.run(
        ["gws", "sheets", "spreadsheets", "values", "get", "--params", params],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout).get("values", [])


def main() -> int:
    report = {"sheet": CONFIG["spreadsheetUrl"], "tabs": {}}
    errors: list[str] = []
    for tab, spec in REQUIRED.items():
        values = gws_get(spec["range"])
        header = values[0] if values else []
        rows = values[1:]
        report["tabs"][tab] = {"rows": len(rows), "columns": len(header)}
        if header[: len(spec["headers"])] != spec["headers"]:
            errors.append(f"{tab}: header mismatch")
        non_empty = [row for row in rows if any(str(cell).strip() for cell in row)]
        if len(non_empty) < spec["min_rows"]:
            errors.append(f"{tab}: expected at least {spec['min_rows']} rows, got {len(non_empty)}")
        for idx, row in enumerate(non_empty, start=2):
            required_width = min(len(spec["headers"]), len(header))
            if len(row) < required_width or any(not str(cell).strip() for cell in row[:required_width]):
                errors.append(f"{tab}: row {idx} has empty required cells")
                break
    if errors:
        print(json.dumps({"ok": False, "errors": errors, **report}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": True, **report}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

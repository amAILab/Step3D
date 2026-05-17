#!/usr/bin/env python3
"""Append a validated Step3D lead to the Google Sheet CRM.

Safe mode:
  --sample --dry-run prints the row and does not call Google APIs.
Real append:
  echo '{...lead payload...}' | python3 scripts/append_lead_to_sheet.py
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "data" / "google_sheet_config.json").read_text(encoding="utf-8"))
VALIDATOR = ROOT / "scripts" / "validate_lead_payload.py"
ROUTER = ROOT / "scripts" / "lead_router.py"

COLUMNS = [
    "id",
    "createdAt",
    "status",
    "name",
    "contact",
    "email",
    "projectType",
    "description",
    "deadline",
    "quantity",
    "dimensions",
    "hasFiles",
    "leadSource",
    "leadIntent",
    "page",
    "nextStep",
    "owner",
]


def router_result(raw: str, sample: bool) -> dict[str, Any]:
    cmd = [sys.executable, str(ROUTER), "--json"]
    if sample:
        cmd.append("--sample")
        proc = subprocess.run(cmd, text=True, capture_output=True, check=True)
    else:
        proc = subprocess.run(cmd, input=raw, text=True, capture_output=True, check=True)
    return json.loads(proc.stdout)


def build_row(result: dict[str, Any]) -> list[str]:
    lead = result["lead"]
    return [
        result.get("projectId") or result.get("id", ""),
        lead.get("createdAt") or lead.get("submittedAt", ""),
        "new",
        lead.get("name", ""),
        lead.get("contact", ""),
        lead.get("email", ""),
        lead.get("projectType") or lead.get("service", ""),
        lead.get("description") or lead.get("task", ""),
        lead.get("deadline", ""),
        lead.get("quantity", ""),
        lead.get("dimensions", ""),
        lead.get("hasFiles") or lead.get("files", ""),
        lead.get("leadSource", ""),
        lead.get("leadIntent", ""),
        lead.get("page", ""),
        "проверить файлы/фото и подготовить ответ",
        "Никита",
    ]


def append_row(row: list[str]) -> dict[str, Any]:
    body = {"range": CONFIG["leadsRange"], "majorDimension": "ROWS", "values": [row]}
    params = {"spreadsheetId": CONFIG["spreadsheetId"], "range": CONFIG["leadsRange"], "valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS"}
    proc = subprocess.run(
        ["gws", "sheets", "spreadsheets", "values", "append", "--params", json.dumps(params, ensure_ascii=False), "--json", json.dumps(body, ensure_ascii=False)],
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = router_result(sys.stdin.read(), args.sample)
    row = build_row(result)
    if args.dry_run:
        print(json.dumps({"ok": True, "dryRun": True, "sheet": CONFIG["spreadsheetUrl"], "columns": COLUMNS, "row": row}, ensure_ascii=False, indent=2))
        return 0
    response = append_row(row)
    print(json.dumps({"ok": True, "sheet": CONFIG["spreadsheetUrl"], "append": response, "leadId": result.get("id")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

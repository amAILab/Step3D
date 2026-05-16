#!/usr/bin/env python3
"""Backend-ready Step3D lead router.

This script is intentionally safe by default: it validates and summarizes a lead,
but does not send email/Telegram unless a future explicit transport is added.
It is useful for local server, cron smoke tests, Cloudflare/VPS migration and QA.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_lead_payload.py"

LABELS = {
    "name": "Имя",
    "email": "Email",
    "contact": "Контакт",
    "projectType": "Тип проекта",
    "deadline": "Срок",
    "quantity": "Количество",
    "dimensions": "Габариты",
    "hasFiles": "Файлы",
    "description": "Описание",
    "leadSource": "Источник",
    "leadIntent": "Intent",
    "page": "Страница",
    "submittedAt": "Время",
}


def validate(raw: str) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        input=raw,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stdout.strip() or proc.stderr.strip() or "lead validation failed")
    return json.loads(proc.stdout)["lead"]


def build_summary(lead: dict[str, str]) -> str:
    lines = ["🦞 Новая заявка Step3D", ""]
    for key in LABELS:
        value = lead.get(key)
        if value:
            lines.append(f"{LABELS[key]}: {value}")
    lines.extend([
        "",
        "Следующий шаг: проверить файлы/фото, уточнить критичные размеры и дать предварительный маршрут: CAD / печать / сканирование / реверс / серия.",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print machine-readable routing result")
    parser.add_argument("--sample", action="store_true", help="use validator sample")
    args = parser.parse_args()

    if args.sample:
        proc = subprocess.run([sys.executable, str(VALIDATOR), "--sample"], text=True, capture_output=True, check=True)
        lead = json.loads(proc.stdout)["lead"]
    else:
        lead = validate(sys.stdin.read())

    result = {
        "ok": True,
        "transport": "dry-run",
        "to_email": "projects.step3d@gmail.com",
        "cc_email": "stepgptai@gmail.com",
        "telegram": "@step_3d_mngr",
        "subject": f"Новая заявка Step3D — {lead.get('projectType') or 'без типа'}",
        "summary": build_summary(lead),
        "lead": lead,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["summary"])
        print("\nDRY_RUN: внешняя отправка не выполнена")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

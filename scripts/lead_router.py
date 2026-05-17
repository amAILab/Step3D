#!/usr/bin/env python3
"""Backend-ready Step3D lead router.

Safe by default: validates and summarizes a lead, but does not send email/Telegram.
Optional local writes create a JSONL audit log and a TASK_INBOX card.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
VALIDATOR = ROOT / "scripts" / "validate_lead_payload.py"
LOG_PATH = ROOT / "data" / "leads_log.jsonl"
TASK_INBOX = WORKSPACE / "TASK_INBOX.md"

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
    proc = subprocess.run([sys.executable, str(VALIDATOR)], input=raw, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.stdout.strip() or proc.stderr.strip() or "lead validation failed")
    return json.loads(proc.stdout)["lead"]


def lead_id(lead: dict[str, str]) -> str:
    existing = (lead.get("projectId") or "").strip().upper()
    if existing.startswith("S3D-"):
        return "".join(ch for ch in existing if ch.isalnum() or ch == "-")[:32]
    now = datetime.now(timezone.utc)
    digest = hashlib.sha1("|".join([lead.get("contact", ""), lead.get("description", ""), lead.get("task", ""), lead.get("submittedAt", "")]).encode("utf-8")).hexdigest()[:4].upper()
    return f"S3D-{now:%y%m%d}-{digest}"


def build_summary(lead: dict[str, str]) -> str:
    lines = ["🦞 Новая заявка Step3D", ""]
    for key in LABELS:
        value = lead.get(key)
        if value:
            lines.append(f"{LABELS[key]}: {value}")
    lines.extend(["", "Следующий шаг: проверить файлы/фото, уточнить критичные размеры и дать предварительный маршрут: CAD / печать / сканирование / реверс / серия."])
    return "\n".join(lines)


def append_log(lead: dict[str, str], result: dict[str, Any]) -> str:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    item = {
        "id": result["id"],
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "lead": lead,
        "route": {k: result[k] for k in ["transport", "to_email", "cc_email", "telegram", "subject"]},
    }
    previous = LOG_PATH.read_text(encoding="utf-8") if LOG_PATH.exists() else ""
    LOG_PATH.write_text(previous + json.dumps(item, ensure_ascii=False) + "\n", encoding="utf-8")
    return str(LOG_PATH)


def append_task(lead: dict[str, str], result: dict[str, Any]) -> str:
    TASK_INBOX.parent.mkdir(parents=True, exist_ok=True)
    block = f"""

## [Step3D lead] {result['id']} — {lead.get('projectType') or 'без типа'}
- Статус: inbox
- Контакт: {lead.get('contact') or 'не указан'}
- Email: {lead.get('email') or 'не указан'}
- Задача: {lead.get('description') or 'не указана'}
- Срок/кол-во/габариты: {lead.get('deadline') or '-'} / {lead.get('quantity') or '-'} / {lead.get('dimensions') or '-'}
- Источник: {lead.get('page') or lead.get('leadSource') or 'Step3D'}
- Следующий шаг: проверить файлы/фото и подготовить короткий ответ клиенту.
"""
    old = TASK_INBOX.read_text(encoding="utf-8") if TASK_INBOX.exists() else "# TASK_INBOX\n"
    if result["id"] not in old:
        TASK_INBOX.write_text(old.rstrip() + block + "\n", encoding="utf-8")
    return str(TASK_INBOX)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print machine-readable routing result")
    parser.add_argument("--sample", action="store_true", help="use validator sample")
    parser.add_argument("--write-log", action="store_true", help="append normalized lead to data/leads_log.jsonl")
    parser.add_argument("--write-task", action="store_true", help="append lead card to workspace TASK_INBOX.md")
    args = parser.parse_args()

    if args.sample:
        proc = subprocess.run([sys.executable, str(VALIDATOR), "--sample"], text=True, capture_output=True, check=True)
        lead = json.loads(proc.stdout)["lead"]
    else:
        lead = validate(sys.stdin.read())

    project_id = lead_id(lead)
    lead["projectId"] = project_id
    result: dict[str, Any] = {
        "ok": True,
        "id": project_id,
        "projectId": project_id,
        "status": "created",
        "nextStep": "проверить файлы/фото и подготовить первый ответ",
        "transport": "dry-run",
        "to_email": "projects.step3d@gmail.com",
        "cc_email": "stepgptai@gmail.com",
        "telegram": "@step_3d_mngr",
        "subject": f"Новая заявка Step3D — {lead.get('projectType') or 'без типа'}",
        "summary": build_summary(lead),
        "lead": lead,
    }
    if args.write_log:
        result["log_path"] = append_log(lead, result)
    if args.write_task:
        result["task_inbox"] = append_task(lead, result)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["summary"])
        print("\nDRY_RUN: внешняя отправка не выполнена")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

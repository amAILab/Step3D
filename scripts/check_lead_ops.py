#!/usr/bin/env python3
"""Step3D lead-ops control check.

One command for recurring checks of the request page, lead routing, reply drafts,
CRM dry-run and release guards. Safe by default: no external messages are sent.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CheckFailed(RuntimeError):
    pass


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        raise CheckFailed(f"нет файла: {rel}")
    return path.read_text(encoding="utf-8")


def require_snippets(rel: str, checks: dict[str, str], errors: list[str]) -> None:
    text = read(rel)
    for label, snippet in checks.items():
        if snippet not in text:
            errors.append(f"{rel}: нет проверки «{label}» → {snippet}")


def run_cmd(label: str, cmd: list[str], errors: list[str], notes: list[str]) -> None:
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    output = (proc.stdout + proc.stderr).strip()
    if proc.returncode != 0:
        errors.append(f"{label}: ошибка {proc.returncode}\n{output}")
        return
    first = output.splitlines()[0] if output else "OK"
    notes.append(f"{label}: {first}")


def check_router_json(errors: list[str], notes: list[str]) -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/lead_router.py", "--sample", "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        errors.append(f"lead_router sample json: ошибка {proc.returncode}\n{proc.stdout}{proc.stderr}")
        return
    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        errors.append(f"lead_router sample json: не JSON: {exc}")
        return
    for key in ["id", "status", "priority", "slaHours", "nextStep", "summary", "lead"]:
        if key not in result:
            errors.append(f"lead_router sample json: нет поля {key}")
    if not str(result.get("id", "")).startswith("S3D-"):
        errors.append("lead_router sample json: ID не начинается с S3D-")
    if result.get("transport") != "dry-run":
        errors.append("lead_router sample json: внешний транспорт должен быть dry-run")
    notes.append(f"lead_router: {result.get('id')} / {result.get('status')} / SLA {result.get('slaHours')} ч")


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []

    require_snippets(
        "app/index.html",
        {
            "контакт обязателен": "id=\"contact\"",
            "описание задачи обязательно": "id=\"task\"",
            "минимум описания": "minlength=\"20\"",
            "номер S3D": "function id(){return 'S3D-'",
            "без автооткрытия Telegram": "Дослать файлы",
            "файлы не хранятся на GitHub Pages": "Файлы не хранятся на GitHub Pages",
            "FormSubmit fallback": "https://formsubmit.co/projects.step3d@gmail.com",
            "Telegram из конфига": "leadConfig.managerTelegram",
            "карточка проекта": "../account/?projectId=",
            "операционный маршрут": "ops-strip",
            "минимум для инженера": "Минимум для ответа инженера",
            "после отправки": "После отправки",
        },
        errors,
    )
    require_snippets(
        "content/lead-reply-templates-2026-05-09.md",
        {
            "только фото": "Клиент прислал только фото детали",
            "цена печати": "сколько стоит напечатать",
            "срочная замена": "срочная замена детали",
            "не просим длинное ТЗ": "Фото достаточно для первого шага",
        },
        errors,
    )
    require_snippets(
        "content/lead-response-playbook-2026-05-09-evening.md",
        {
            "классификация 2 минуты": "Классификация заявки за 2 минуты",
            "не обещать без проверки": "Когда не обещать сразу",
            "не отправлять без Никиты": "Публиковать/отправлять клиенту только после подтверждения Никиты",
        },
        errors,
    )
    require_snippets(
        "docs/server-lead-pipeline.md",
        {
            "если нет новых заявок": "NO_NEW_LEADS",
            "dry-run smoke": "python3 scripts/check_step3d_leads.py --self-test",
            "Google Sheet CRM": "Google Sheet CRM",
            "не хранить токены": "Не хранить токены в репозитории",
        },
        errors,
    )

    run_cmd("валидатор заявки", [sys.executable, "scripts/validate_lead_payload.py", "--sample"], errors, notes)
    check_router_json(errors, notes)
    run_cmd("таблица CRM dry-run", [sys.executable, "scripts/append_lead_to_sheet.py", "--sample", "--dry-run"], errors, notes)
    run_cmd("мониторинг/ответ self-test", [sys.executable, "scripts/check_step3d_leads.py", "--self-test"], errors, notes)
    run_cmd("маршрут заявки", [sys.executable, "scripts/check_request_flow.py"], errors, notes)
    run_cmd("релизная готовность", [sys.executable, "scripts/check_release_readiness.py"], errors, notes)

    if errors:
        print("LEAD_OPS_CHECK_FAIL")
        print("\n".join(f"- {e}" for e in errors))
        return 1

    print("LEAD_OPS_CHECK_OK")
    for note in notes:
        print(f"- {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

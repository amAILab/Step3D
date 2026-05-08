#!/usr/bin/env python3
"""Check Gmail for new Step3D form submissions and print a concise alert.

Uses mcporter + google-workspace MCP OAuth. Keeps a local seen-id file so
OpenClaw can run it periodically without duplicate notifications.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".lead_monitor_seen.json"
QUERY = 'newer_than:30d subject:"Новая заявка Step3D"'


def call_tool(tool: str, **kwargs):
    cmd = [
        "mcporter",
        "call",
        "--server",
        "google-workspace",
        "--tool",
        tool,
        "--output",
        "json",
    ]
    for key, value in kwargs.items():
        cmd.append(f"{key}={value}")
    raw = subprocess.check_output(cmd, text=True)
    return json.loads(raw)


def load_seen() -> set[str]:
    if not STATE.exists():
        return set()
    try:
        return set(json.loads(STATE.read_text(encoding="utf-8")))
    except Exception:
        return set()


def save_seen(ids: set[str]) -> None:
    STATE.write_text(json.dumps(sorted(ids), ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    seen = load_seen()
    result = call_tool("gmail.search", query=QUERY, maxResults=10)
    messages = result.get("messages", []) or []
    ids = [m["id"] for m in messages if m.get("id")]

    if not STATE.exists():
        save_seen(set(ids))
        print("NO_NEW_LEADS: мониторинг заявок Step3D инициализирован.")
        return 0

    new_ids = [mid for mid in ids if mid not in seen]
    if not new_ids:
        print("NO_NEW_LEADS")
        return 0

    alerts = []
    for mid in reversed(new_ids):
        msg = call_tool("gmail.get", messageId=mid)
        seen.add(mid)
        body = (msg.get("body") or msg.get("snippet") or "").strip()
        import html as html_lib
        import re

        pairs = re.findall(
            r"<strong>([^<]+)</strong>.*?<pre[^>]*>(.*?)</pre>",
            body,
            flags=re.S | re.I,
        )
        labels = {
            "name": "Имя",
            "contact": "Контакт",
            "projectType": "Тип проекта",
            "deadline": "Срок",
            "quantity": "Количество",
            "dimensions": "Габариты",
            "hasFiles": "Файлы/фото",
            "description": "Описание",
            "source": "Источник",
            "page": "Страница",
            "submittedAt": "Время отправки",
        }
        useful = []
        for key, value in pairs:
            key = html_lib.unescape(key).strip()
            value = html_lib.unescape(re.sub(r"<[^>]+>", "", value)).strip()
            if key.startswith("_") or key == "_honey" or not value:
                continue
            useful.append(f"{labels.get(key, key)}: {value}")
        if not useful:
            plain = html_lib.unescape(re.sub(r"<[^>]+>", " ", body))
            plain = re.sub(r"\s+", " ", plain).strip()
            useful = [plain[:800] or msg.get("snippet") or "Новая заявка без текста"]
        summary = "\n".join(useful[:12])
        alerts.append(
            "🦞 Новая заявка Step3D\n"
            f"Тема: {msg.get('subject', 'без темы')}\n"
            f"От: {msg.get('from', 'неизвестно')}\n"
            f"Дата: {msg.get('date', '')}\n\n"
            f"{summary}"
        )

    save_seen(seen)
    print("\n\n---\n\n".join(alerts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

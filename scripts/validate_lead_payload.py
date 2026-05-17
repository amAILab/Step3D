#!/usr/bin/env python3
"""Validate a Step3D lead payload before sending it to a backend/mail router.

Usage:
  echo '{"contact":"@user","description":"Need STL by photo"}' | python3 scripts/validate_lead_payload.py
  python3 scripts/validate_lead_payload.py --sample
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "data" / "lead_schema.json").read_text(encoding="utf-8"))
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

SAMPLE = {
    "name": "Тест",
    "email": "",
    "contact": "@step_3d_mngr",
    "projectType": "STL-модель по фото или референсу",
    "deadline": "на этой неделе",
    "quantity": "1",
    "dimensions": "700 мм",
    "hasFiles": "фото",
    "description": "Нужно оценить STL-модель по фото и подготовку к 3D-печати.",
    "leadSource": "validator sample",
    "leadIntent": "backend smoke test",
    "page": "https://amailab.github.io/Step3D/#brief",
    "submittedAt": datetime.now(timezone.utc).isoformat(),
    "botField": "",
}


def fail(message: str) -> None:
    print(f"INVALID: {message}")
    raise SystemExit(1)


def print_usage_error() -> None:
    print("INVALID: empty input")
    print("Usage: echo '{\"contact\":\"@user\",\"description\":\"Need STL by photo\"}' | python3 scripts/validate_lead_payload.py")
    print("Or:    python3 scripts/validate_lead_payload.py --sample")
    raise SystemExit(2)


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def validate(payload: dict[str, Any]) -> dict[str, str]:
    payload = dict(payload)
    if not as_text(payload.get("description")) and as_text(payload.get("task")):
        payload["description"] = as_text(payload.get("task"))
    if not as_text(payload.get("task")) and as_text(payload.get("description")):
        payload["task"] = as_text(payload.get("description"))
    if not as_text(payload.get("projectType")) and as_text(payload.get("service")):
        payload["projectType"] = as_text(payload.get("service"))
    if not as_text(payload.get("hasFiles")) and as_text(payload.get("files")):
        payload["hasFiles"] = "files/slinks provided"
    clean: dict[str, str] = {}
    if as_text(payload.get("botField") or payload.get("_honey")):
        fail("honeypot field is filled")

    for key, spec in SCHEMA.get("properties", {}).items():
        value = as_text(payload.get(key, ""))
        if CONTROL_RE.search(value):
            fail(f"field `{key}` contains control characters")
        max_len = spec.get("maxLength")
        min_len = spec.get("minLength")
        if max_len is not None and len(value) > max_len:
            fail(f"field `{key}` is too long: {len(value)} > {max_len}")
        if key in SCHEMA.get("required", []) and len(value) < int(min_len or 1):
            fail(f"required field `{key}` is empty or too short")
        if value:
            clean[key] = value

    email = clean.get("email", "")
    if email and not EMAIL_RE.match(email):
        fail("email has invalid format")

    if not clean.get("description") and not clean.get("task"):
        fail("required field `description` or `task` is empty or too short")
    if len(clean.get("description") or clean.get("task") or "") < 8:
        fail("description/task is too short")

    contact = clean.get("contact", "")
    if not ("@" in contact or re.search(r"\d{6,}", contact) or EMAIL_RE.match(contact)):
        fail("contact should contain Telegram username, email, or phone-like number")

    if "submittedAt" not in clean:
        clean["submittedAt"] = datetime.now(timezone.utc).isoformat()
    return clean


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", action="store_true", help="validate built-in sample payload")
    args = parser.parse_args()
    raw = json.dumps(SAMPLE, ensure_ascii=False) if args.sample else sys.stdin.read()
    if not raw.strip():
        print_usage_error()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    if not isinstance(payload, dict):
        fail("payload must be a JSON object")
    clean = validate(payload)
    print(json.dumps({"ok": True, "lead": clean}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

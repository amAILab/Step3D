#!/usr/bin/env python3
"""Final Step3D release readiness smoke check.

Checks the core static product path, not external APIs:
home → app → viewer → thanks/account, plus backend/CRM/SEO guardrails.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    "index.html": [
        "href=\"app/#app-brief\"",
        "hero-flow-strip",
        "projectNextStep",
        "trust-compact-title",
        "LocalBusiness",
        "FAQPage",
    ],
    "app/index.html": [
        "Не форма. Рабочее место для заявки",
        "source-card",
        "step3d:viewerBrief",
        "STEP3D_LEAD_CONFIG",
        "WebApplication",
    ],
    "viewer/index.html": [
        "step3d:viewerBrief",
        "Передать расчёт в заявку",
        "cdnFallback",
        "href=\"../app/#app-brief\"",
    ],
    "thanks/index.html": [
        "thanksProjectCard",
        "Открыть карточку заявки",
        "href=\"../app/#app-brief\"",
    ],
    "account/index.html": [
        "Проект пока не выбран",
        "replace(/[^A-Z0-9-]/gi",
        "escapeHtml",
        "href=\"../app/#app-brief\"",
    ],
    "assets/lead-config.js": [
        "STEP3D_LEAD_CONFIG",
        "primaryEndpoint",
        "formSubmitEndpoint",
        "managerTelegram",
    ],
    "data/lead_schema.json": [
        "projectId",
        "service",
        "task",
        "files",
    ],
    "data/crm_statuses.json": [
        "needs_files",
        "estimating",
        "quoted",
        "sla",
    ],
    "scripts/mock_lead_api.py": [
        "mock-local",
        "projectId",
    ],
}

missing: list[str] = []
for rel, needles in CHECKS.items():
    path = ROOT / rel
    if not path.exists():
        missing.append(f"{rel}: file missing")
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            missing.append(f"{rel}: missing {needle}")

if missing:
    print("RELEASE_READINESS_FAIL")
    for item in missing:
        print(item)
    raise SystemExit(1)

print(f"RELEASE_READINESS_OK files={len(CHECKS)} checks={sum(len(v) for v in CHECKS.values())}")

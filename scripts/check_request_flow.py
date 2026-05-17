#!/usr/bin/env python3
"""Smoke-check the Step3D request flow across static pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_CACHE_VERSION = 4
CHECKS = {
    "index.html": {
        "hero flow": "hero-flow-strip",
        "project next step": 'id="projectNextStep"',
        "quick lead guard": "quickLeadIsReady",
        "no telegram auto-open": "Дослать файлы",
        "stored lead": "step3d:lastLead",
        "production handoff": "production-handoff",
        "live case journey": "case-journey",
    },
    "thanks/index.html": {
        "project card": 'id="thanksProjectCard"',
        "four-step flow": "flow-next-grid",
        "account CTA": "Открыть карточку заявки",
    },
    "viewer/index.html": {
        "viewer brief storage": "step3d:viewerBrief",
        "app handoff": "../app/#app-brief",
        "save and create CTA": "Передать расчёт в заявку",
        "saved handoff notice": "viewerSaved",
        "cdn fallback": "cdnFallback",
    },
    "app/index.html": {
        "ai workspace title": "Не форма. Рабочее место для заявки",
        "viewer brief import": "step3d:viewerBrief",
        "scenario cards": "source-card",
        "service prefill": "data-preset",
        "readiness meter": "meterFill",
        "next actions": "nextActions",
        "honest file handoff": "Файлы не хранятся на GitHub Pages",
        "lead config manager": "leadConfig.managerTelegram",
        "contact accepts telegram": "Телефон, email или @telegram",
        "account handoff": "../account/?projectId=",
        "operations strip": "ops-strip",
        "client minimum check": "Минимум для ответа инженера",
        "after submit instruction": "После отправки",
    },
    "account/index.html": {
        "project id sanitizing": "replace(/[^A-Z0-9-]/gi,'')",
        "escape html": "escapeHtml",
        "b2b next action": "B2B-следующий шаг",
    },
    "service-worker.js": {
        "skip waiting message": "SKIP_WAITING",
    },
    "assets/pwa-install.js": {
        "update banner": "Доступна свежая версия Step3D",
        "controller reload": "controllerchange",
    },
    "assets/lead-config.js": {
        "lead endpoint config": "STEP3D_LEAD_CONFIG",
        "formsubmit fallback": "formSubmitEndpoint",
        "telegram manager": "managerTelegram",
    },
}


def main() -> int:
    errors: list[str] = []
    for rel, snippets in CHECKS.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for label, snippet in snippets.items():
            if snippet not in text:
                errors.append(f"{rel}: missing {label}: {snippet}")
    service_worker = (ROOT / "service-worker.js").read_text(encoding="utf-8")
    cache_match = re.search(r"step3d-pwa-v(\d+)", service_worker)
    if not cache_match or int(cache_match.group(1)) < MIN_CACHE_VERSION:
        errors.append(f"service-worker.js: cache version must be step3d-pwa-v{MIN_CACHE_VERSION}+")

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    for rel in ["viewer/index.html", "thanks/index.html"]:
        if "#app-brief" not in (ROOT / rel).read_text(encoding="utf-8"):
            errors.append(f"{rel}: missing app brief handoff")
    if "window.open(`${managerTelegram}" in index or "window.setTimeout(() => window.open" in index:
        errors.append("index.html: Telegram auto-open after submit/fallback is back")
    if errors:
        raise SystemExit("REQUEST_FLOW_CHECK_FAILED\n" + "\n".join(errors))
    print("REQUEST_FLOW_CHECK_OK pages=5 checks=%d" % sum(len(v) for v in CHECKS.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

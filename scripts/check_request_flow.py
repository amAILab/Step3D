#!/usr/bin/env python3
"""Smoke-check the Step3D request flow across static pages."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = {
    "index.html": {
        "hero flow": "hero-flow-strip",
        "project next step": 'id="projectNextStep"',
        "quick lead guard": "quickLeadIsReady",
        "no telegram auto-open": "Дослать файлы",
        "stored lead": "step3d:lastLead",
    },
    "thanks/index.html": {
        "project card": 'id="thanksProjectCard"',
        "four-step flow": "flow-next-grid",
        "account CTA": "Открыть статус проекта",
    },
    "viewer/index.html": {
        "viewer brief storage": "step3d:viewerBrief",
        "app handoff": "../app/#app-brief",
        "cdn fallback": "cdnFallback",
    },
    "app/index.html": {
        "viewer import banner": 'id="viewerImportBanner"',
        "viewer brief import": "step3d:viewerBrief",
        "sketch launcher": "sketch-phone",
        "service prefill": "data-app-task",
        "brief progress": "briefProgressText",
        "project next actions": "projectNextActions",
    },
    "account/index.html": {
        "project id sanitizing": "replace(/[^A-Z0-9-]/gi,'')",
        "escape html": "escapeHtml",
        "b2b next action": "B2B-следующий шаг",
    },
    "service-worker.js": {
        "cache version bump": "step3d-pwa-v3",
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
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    if "window.open(`${managerTelegram}" in index or "window.setTimeout(() => window.open" in index:
        errors.append("index.html: Telegram auto-open after submit/fallback is back")
    if errors:
        raise SystemExit("REQUEST_FLOW_CHECK_FAILED\n" + "\n".join(errors))
    print("REQUEST_FLOW_CHECK_OK pages=5 checks=%d" % sum(len(v) for v in CHECKS.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

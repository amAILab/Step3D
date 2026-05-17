#!/usr/bin/env python3
"""Check that key Step3D conversion actions expose metric hooks."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"
REQUIRED_METRICS = {"brief_click", "telegram_click"}
REQUIRED_GOALS = {"lead_form_submit", "brief_template_copy", "micro_calc_change", "quick_lead_preset", "lead_mode_switch"}


def main() -> int:
    text = HTML.read_text(encoding="utf-8")
    metrics = set(re.findall(r"data-metric=[\"']([^\"']+)[\"']", text))
    hooks = len(re.findall(r'\bdata-metric=', text))
    missing_metrics = sorted(REQUIRED_METRICS - metrics)
    missing_goals = sorted(goal for goal in REQUIRED_GOALS if goal not in text)
    if missing_metrics or missing_goals:
        raise SystemExit(f"ANALYTICS_EVENTS_MISSING metrics={missing_metrics} goals={missing_goals}")
    print(f"ANALYTICS_EVENTS_OK metrics={len(metrics)} hooks={hooks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

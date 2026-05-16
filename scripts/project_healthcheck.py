#!/usr/bin/env python3
"""Step3D project healthcheck: site, SEO, lead pipeline and deploy-ready files."""
from __future__ import annotations

import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "index.html",
    "account/index.html",
    "account/demo/index.html",
    "sitemap.xml",
    "robots.txt",
    "data/lead_schema.json",
    "docs/server-lead-pipeline.md",
    ".well-known/security.txt",
    "scripts/validate_lead_payload.py",
    "scripts/lead_router.py",
    "scripts/append_lead_to_sheet.py",
    "data/google_sheet_config.json",
    "data/content_sheet_config.json",
    "docs/content-cms-sheet.md",
    "scripts/export_content_sheet.py",
]


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT, text=True, stderr=subprocess.STDOUT)


def check_files() -> None:
    missing = [p for p in REQUIRED_FILES if not (ROOT / p).exists()]
    if missing:
        raise AssertionError(f"missing required files: {missing}")


def check_home() -> None:
    soup = BeautifulSoup((ROOT / "index.html").read_text(encoding="utf-8"), "html.parser")
    form = soup.find("form", id="leadForm")
    assert form and form.get("action") == "https://formsubmit.co/projects.step3d@gmail.com"
    names = {tag.get("name") for tag in form.find_all(["input", "textarea", "select"]) if tag.get("name")}
    for name in ["contact", "description", "page", "submittedAt", "utm_source", "utm_medium", "utm_campaign", "utm_content", "_cc", "_honey"]:
        assert name in names, f"lead form field missing: {name}"
    jsonld = []
    for script in soup.find_all("script", type="application/ld+json"):
        jsonld.append(json.loads(script.string or script.get_text()))
    assert any(item.get("@type") == "FAQPage" for item in jsonld), "FAQPage schema missing"


def check_sitemap() -> None:
    tree = ET.parse(ROOT / "sitemap.xml")
    urls = [loc.text for loc in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    for url in [
        "https://amailab.github.io/Step3D/",
        "https://amailab.github.io/Step3D/gallery/",
        "https://amailab.github.io/Step3D/account/",
        "https://amailab.github.io/Step3D/data/lead_schema.json",
        "https://amailab.github.io/Step3D/docs/server-lead-pipeline.md",
    ]:
        assert url in urls, f"sitemap URL missing: {url}"


def main() -> int:
    check_files()
    check_home()
    check_sitemap()
    run([sys.executable, "scripts/validate_site.py"])
    run([sys.executable, "scripts/validate_lead_payload.py", "--sample"])
    run([sys.executable, "scripts/lead_router.py", "--sample", "--json"])
    run([sys.executable, "scripts/lead_router.py", "--sample", "--write-log", "--json"])
    (ROOT / "data" / "leads_log.jsonl").write_text("", encoding="utf-8")
    run([sys.executable, "scripts/check_step3d_leads.py", "--self-test"])
    run([sys.executable, "scripts/check_analytics_events.py"])
    run([sys.executable, "scripts/append_lead_to_sheet.py", "--sample", "--dry-run"])
    run([sys.executable, "scripts/export_content_sheet.py", "--dry-run"])
    print("STEP3D_PROJECT_HEALTHCHECK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

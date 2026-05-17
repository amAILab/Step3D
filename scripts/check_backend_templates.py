#!/usr/bin/env python3
"""Check backend-ready templates/docs for Step3D lead intake."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS = {
    "assets/lead-config.js": ["STEP3D_LEAD_CONFIG", "primaryEndpoint", "formSubmitEndpoint"],
    "docs/backend_endpoint_contract.md": ["Step3D lead backend endpoint contract", "primaryEndpoint", "FormData"],
    "backend/google-apps-script/Code.gs": ["function doPost", "appendLead_", "notifyTelegram_", "SHEET_ID"],
    "backend/google-apps-script/README.md": ["Google Apps Script backend", "primaryEndpoint", "Web App URL"],
    "docs/file_intake_contract.md": ["Step3D file intake contract", "S3D-", "Backend-upload MVP"],
    "scripts/mock_lead_api.py": ["Local mock Step3D lead API", "projectId", "mock-local"],
    "data/lead_schema.json": ["projectId", "task", "service", "files"],
    "data/crm_statuses.json": ["needs_files", "estimating", "firstReplyHours", "followupHours"],
}

def main() -> int:
    errors = []
    for rel, snippets in CHECKS.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{rel}: missing {snippet}")
    if errors:
        raise SystemExit("BACKEND_TEMPLATE_CHECK_FAILED\n" + "\n".join(errors))
    print(f"BACKEND_TEMPLATE_CHECK_OK files={len(CHECKS)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

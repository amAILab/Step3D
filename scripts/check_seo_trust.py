#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks = {
    'index.html': [
        'trust-compact-title',
        'Файлы и NDA',
        'B2B-документы',
        'b2b-card--quiet',
        'LocalBusiness',
        'FAQPage',
    ],
    'app/index.html': [
        'WebApplication',
        'Step3D App',
        'applicationCategory',
    ],
}
missing = []
for rel, needles in checks.items():
    text = (ROOT / rel).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            missing.append(f'{rel}: {needle}')
if missing:
    print('SEO_TRUST_CHECK_FAIL')
    for item in missing:
        print(item)
    raise SystemExit(1)
print(f'SEO_TRUST_CHECK_OK files={len(checks)} checks={sum(len(v) for v in checks.values())}')

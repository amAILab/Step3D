#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
checks = {
    'index.html': [
        'hidden aria-hidden="true"',
        'trapStoryFocus',
        'mobileMenu.hidden = true',
        'Viewer не обязателен',
        'Оставить заявку',
    ],
    'app/index.html': [
        'function activateTab',
        'ArrowRight',
        'aria-invalid',
        'Дослать файлы в Telegram',
        'Скопировать заявку',
        '3–5 ракурсов',
    ],
    'viewer/index.html': [
        'Заявка по фото без Viewer',
        'Что нужно для заявки',
        'Viewer не обязателен',
    ],
    'account/index.html': [
        'Карточка заявки',
        'Карточка заявки S3D',
        'Карточка пока preview',
    ],
    'assets/minimal-ui.css': [
        'prefers-reduced-motion',
        'focus-visible',
        'aria-invalid',
        'safe-area-inset-bottom',
    ],
}
missing=[]
for rel, needles in checks.items():
    text=(ROOT/rel).read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            missing.append(f'{rel}: {needle}')
if missing:
    print('UX_UI_2_CHECK_FAIL')
    print('\n'.join(missing))
    raise SystemExit(1)
print(f'UX_UI_2_CHECK_OK files={len(checks)} checks={sum(len(v) for v in checks.values())}')

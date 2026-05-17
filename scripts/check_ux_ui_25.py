#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks={
 'assets/step3d-design-system.css':['--s3d-bg','--s3d-surface','s3d-surface','s3d-grid-3'],
 'assets/ux-ui-100.css':['Stage 7: bottom nav','Stages 16–20','prefers-reduced-motion','max-width:1120px','bottom-nav{grid-template-columns:repeat(3'],
 'index.html':['Покажите деталь','home-focus-strip','Оставить заявку'],
 'app/index.html':['Опишите деталь','required-later','Оставить заявку','Дослать файлы в Telegram'],
 'viewer/index.html':['Есть STL?','Что нужно для заявки','Заявка по фото без Viewer'],
 'account/index.html':['Карточка заявки','preview-карточка','подтверждение приходит'],
 'thanks/index.html':['Заявка принята. Дальше — файлы','Открыть карточку заявки'],
 'docs/ux_ui_25_stages.md':['Stage 1','Stage 20','25 этапов']
}
missing=[]
for rel,needles in checks.items():
 t=(ROOT/rel).read_text(encoding='utf-8')
 for n in needles:
  if n not in t: missing.append(f'{rel}: {n}')
if missing:
 print('UX_UI_25_CHECK_FAIL')
 print('\n'.join(missing))
 raise SystemExit(1)
print(f'UX_UI_25_CHECK_OK files={len(checks)} checks={sum(len(v) for v in checks.values())}')

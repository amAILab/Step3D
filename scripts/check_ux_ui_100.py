#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
checks={
 'docs/ux_ui_100_stages.md':['100 этапов','Stages 66–85','Stage 1–10 result'],
 'assets/ux-ui-10.css':['Ollama + NotebookLM','ux-source-board','Stages 66–85','content-visibility'],
 'index.html':['Оставить заявку','ollama-home-note','home-focus-strip'],
 'app/index.html':['Опишите деталь','Получите маршрут','ux-source-board','Оставить заявку'],
 'viewer/index.html':['Есть STL?','Передать расчёт в заявку','Источник готов'],
 'account/index.html':['Карточка заявки S3D','не личный кабинет'],
 'thanks/index.html':['Заявка принята. Дальше — файлы','Дослать файлы в Telegram'],
}
missing=[]
for rel, needles in checks.items():
 t=(ROOT/rel).read_text(encoding='utf-8')
 for n in needles:
  if n not in t: missing.append(f'{rel}: {n}')
if missing:
 print('UX_UI_100_CHECK_FAIL')
 print('\n'.join(missing))
 raise SystemExit(1)
print(f'UX_UI_100_CHECK_OK files={len(checks)} checks={sum(len(v) for v in checks.values())}')

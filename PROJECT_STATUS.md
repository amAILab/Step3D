# Step3D — текущий статус

Публичный сайт: https://amailab.github.io/Step3D/

## Production

- Хостинг: GitHub Pages.
- Форма: FormSubmit → `projects.step3d@gmail.com`, cc `stepgptai@gmail.com`.
- Success page: https://amailab.github.io/Step3D/thanks/
- Галерея: https://amailab.github.io/Step3D/gallery/
- Схема заявки: https://amailab.github.io/Step3D/data/lead_schema.json
- Серверный контур: https://amailab.github.io/Step3D/docs/server-lead-pipeline.md

## Проверки перед словами «готово»

```bash
python3 scripts/project_healthcheck.py
python3 scripts/validate_site.py
git diff --check
```

Если менялись generated/SEO страницы:

```bash
python3 scripts/build_static_pages.py
```

Если менялась серверная/lead часть:

```bash
python3 scripts/validate_lead_payload.py --sample
python3 scripts/lead_router.py --sample --json
python3 scripts/check_step3d_leads.py --self-test
```

## Деплой

```bash
git add ...
git commit -m "..."
git push
gh run watch --exit-status $(gh run list --limit 1 --json databaseId -q '.[0].databaseId')
```

После деплоя Никите обязательно дать ссылку: https://amailab.github.io/Step3D/

## Важные ограничения

- Email в форме необязателен; обязательный контакт — телефон/Telegram.
- Файлы пока отправляются в Telegram: https://t.me/step_3d_mngr
- Не отправлять внешние письма/сообщения клиентам без подтверждения.
- Если `scripts/check_step3d_leads.py` выводит `NO_NEW_LEADS`, отвечать строго `NO_REPLY`.


## Локальный журнал лидов

- `scripts/lead_router.py --write-log` пишет нормализованную заявку в `data/leads_log.jsonl`.
- `scripts/lead_router.py --write-task` создаёт карточку в `../TASK_INBOX.md`.
- По умолчанию роутер работает в `dry-run` и не отправляет внешние сообщения.


## Google Sheet CRM

- Таблица: Step3D Leads CRM — https://docs.google.com/spreadsheets/d/1MfJmmxDq2WNpfAoUsiPQktpj7Y5N12Dc6fKYGvu6D2Y/edit
- Конфиг: `data/google_sheet_config.json`.
- Dry-run проверки: `python3 scripts/append_lead_to_sheet.py --sample --dry-run`.
- Реальная запись валидированной заявки: `python3 scripts/append_lead_to_sheet.py < lead.json`.


## Личный кабинет

- Preview-страница: `https://amailab.github.io/Step3D/account/`.
- Демо проекта: `https://amailab.github.io/Step3D/account/demo/`.
- Сейчас это frontend-ready слой без настоящей авторизации; для реального кабинета нужен backend/auth и хранилище файлов.


## Контент в Google Sheet

- Таблица используется как CMS/реестр контента: `Content`, `Cases`, `FAQ`, `Pages`, `Backlog`.
- Документация: `docs/content-cms-sheet.md`.
- Экспорт: `python3 scripts/export_content_sheet.py --dry-run` или `--out data/content_export.json`.
- Production всё ещё контролируется GitHub/diff/review, чтобы случайная правка в таблице не ломала сайт.

# Step3D server / lead pipeline

Цель: заявки с сайта не должны теряться, даже пока сайт опубликован как статический GitHub Pages.

## Текущий production-контур

1. Форма на `https://amailab.github.io/Step3D/#brief` отправляет данные в FormSubmit:
   - получатель: `projects.step3d@gmail.com`;
   - копия: `stepgptai@gmail.com`;
   - success page: `/thanks/`.
2. Мониторинг заявок: `scripts/check_step3d_leads.py` читает Gmail через google-workspace/mcporter.
3. Если новых заявок нет, скрипт печатает строго `NO_NEW_LEADS`.
4. Если заявка есть, скрипт форматирует сводку и может отправить автоответ по email, если email указан.

## Backend-ready слой

Добавлены безопасные локальные компоненты:

- `data/lead_schema.json` — контракт заявки;
- `scripts/validate_lead_payload.py` — локальная валидация payload;
- `scripts/lead_router.py` — dry-run роутер заявки: нормализует payload, готовит тему, сводку, email/Telegram назначения;
- `scripts/check_step3d_leads.py --self-test` — smoke test мониторинга без Gmail и без внешней отправки.

## Smoke checks

```bash
python3 scripts/validate_lead_payload.py --sample
python3 scripts/lead_router.py --sample --json
python3 scripts/check_step3d_leads.py --self-test
python3 scripts/validate_site.py
git diff --check
```

## Безопасный переход на свой сервер

Приоритет Никиты: если сайту Step3D нужен сервер, сначала рассматривать компьютер Никиты как сервер, если это безопасно и технически подходит.

Варианты:

1. **Оставить GitHub Pages + FormSubmit**
   - минимальный риск;
   - зависимость от FormSubmit и подтверждения адреса;
   - мониторинг через Gmail остаётся обязательным.

2. **Компьютер Никиты как сервер**
   - подходит для внутреннего lead API или webhook;
   - риски: доступность ПК, динамический IP/NAT, безопасность портов, резервное питание/интернет;
   - безопаснее публиковать через Cloudflare Tunnel/Tailscale Funnel, а не открывать порт напрямую.

3. **Cloudflare Worker / Railway / VPS**
   - стабильнее как публичный endpoint;
   - можно использовать `lead_schema.json` и логику `lead_router.py` как контракт;
   - внешние отправки email/Telegram включать только после отдельного подтверждения и секретов.

## Правила безопасности

- Не хранить токены в репозитории.
- Не печатать секреты в логах.
- Не включать внешнюю отправку клиентам без явного подтверждения.
- Honeypot `_honey` / `botField` должен оставаться пустым.
- Обязательный контакт: телефон или Telegram; email необязателен.
- Для важных заявок фиксировать карточку в `TASK_INBOX.md` и готовить короткий ответ клиенту.


## Локальный журнал лидов

- `scripts/lead_router.py --write-log` пишет нормализованную заявку в `data/leads_log.jsonl`.
- `scripts/lead_router.py --write-task` создаёт карточку в `../TASK_INBOX.md`.
- По умолчанию роутер работает в `dry-run` и не отправляет внешние сообщения.


## Google Sheet CRM

- Таблица: Step3D Leads CRM — https://docs.google.com/spreadsheets/d/1MfJmmxDq2WNpfAoUsiPQktpj7Y5N12Dc6fKYGvu6D2Y/edit
- Конфиг: `data/google_sheet_config.json`.
- Dry-run проверки: `python3 scripts/append_lead_to_sheet.py --sample --dry-run`.
- Реальная запись валидированной заявки: `python3 scripts/append_lead_to_sheet.py < lead.json`.

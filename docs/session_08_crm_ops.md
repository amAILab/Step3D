# Session 08 — CRM / операционный контур Step3D

Цель: чтобы лиды попадали не просто в таблицу, а в управляемую операционную схему: статус, приоритет, SLA, ответственный и следующий шаг.

## Что изменено

### CRM statuses

Добавлен `data/crm_statuses.json`:

- `new` — новая заявка, не разобрана;
- `needs_files` — не хватает фото/STL/STEP/размеров;
- `estimating` — инженер считает маршрут, срок и вилку;
- `quoted` — оценка отправлена;
- `in_work` — задача согласована и запущена;
- `done` — завершено;
- `lost` — неактуально / отказ / не подходит.

Также задан SLA:

- первый ответ: 24 часа;
- срочный первый ответ: 4 часа;
- follow-up: 48 часов.

### Lead router

`scripts/lead_router.py` теперь классифицирует лид:

- если есть файлы/фото/STL/STEP/Viewer brief → `estimating`;
- если файлов/размеров нет → `needs_files`;
- если есть срочность (`сегодня`, `завтра`, `urgent`, `asap`) → `priority=urgent`, SLA 4 часа;
- если B2B/NDA/счёт/договор → `priority=high` и nextStep дополняется документами.

Ответ router теперь содержит:

```json
{
  "status": "estimating",
  "priority": "normal",
  "slaHours": "24",
  "owner": "Никита",
  "nextStep": "подготовить первый ответ: маршрут, срок, цена-вилка, риски"
}
```

### Google Sheet row

`scripts/append_lead_to_sheet.py` теперь добавляет в row:

- `nextStep`
- `owner`
- `priority`
- `slaHours`

Это делает таблицу не просто архивом лидов, а рабочим inbox.

## Проверки

- `python3 scripts/lead_router.py --sample --json` → OK
- `python3 scripts/append_lead_to_sheet.py --sample --dry-run` → OK
- `python3 scripts/check_backend_templates.py` → OK
- `python3 scripts/project_healthcheck.py` → OK
- `python3 scripts/validate_site.py` → OK
- `python3 scripts/check_request_flow.py` → OK

## Итог

Операционная логика Step3D стала яснее: каждый лид получает статус, приоритет, SLA и следующий шаг. Следующая сессия — SEO / trust / B2B без перегруза: оставить доверие, но не ломать минимализм.

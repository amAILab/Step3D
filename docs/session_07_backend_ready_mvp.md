# Session 07 — backend-ready MVP

Цель: довести backend-ready контур до состояния, где фронт может получить настоящий server-side `projectId`, а локальные проверки ловят рассинхрон между App payload и backend schema.

## Что изменено

### Schema / validator

- `data/lead_schema.json` теперь знает поля App:
  - `projectId`
  - `service`
  - `task`
  - `files`
  - `createdAt`
- `scripts/validate_lead_payload.py` принимает alias-поля:
  - `task` ↔ `description`
  - `service` → `projectType`
  - `files` → `hasFiles`
- Контакт теперь может быть Telegram, телефон или email.
- Это убирает риск, что App отправляет `task`, а backend ждёт только `description`.

### Router / projectId

- `scripts/lead_router.py` теперь возвращает нормальный Step3D ID:
  - `S3D-YYMMDD-XXXX`
- Если фронт/сервер уже передал `projectId`, router принимает его и очищает.
- Ответ router теперь ближе к production API:

```json
{
  "ok": true,
  "id": "S3D-260517-XXXX",
  "projectId": "S3D-260517-XXXX",
  "status": "created",
  "nextStep": "проверить файлы/фото и подготовить первый ответ"
}
```

### Sheet append

- `scripts/append_lead_to_sheet.py` теперь пишет:
  - `projectId` как ID;
  - `createdAt` или `submittedAt`;
  - `service`/`task`/`files` alias-поля, если они пришли из App.

### Mock API

Добавлен `scripts/mock_lead_api.py` — локальный mock production endpoint:

```bash
python3 scripts/mock_lead_api.py --sample
python3 scripts/mock_lead_api.py --sample --write-log
```

Он возвращает форму ответа, которую ждёт фронт, и может писать `data/leads_log.jsonl`.

### Backend checks

- `scripts/check_backend_templates.py` теперь проверяет:
  - mock API;
  - App-поля в schema;
  - backend docs/templates.

## Проверки

- `python3 scripts/validate_lead_payload.py --sample` → OK
- App-like payload с `task/service/files` → OK
- `python3 scripts/lead_router.py --sample --json` → OK
- `python3 scripts/append_lead_to_sheet.py --sample --dry-run` → OK
- `python3 scripts/mock_lead_api.py --sample --write-log` → OK
- `python3 scripts/check_backend_templates.py` → OK

## Итог

Фронт ещё не переключён на реальный backend URL, но контракт стал консистентным: App payload, validator, router, Sheet и mock API теперь говорят на одном языке. Следующий production-шаг — поднять Apps Script/Railway/Firebase endpoint и поставить его в `assets/lead-config.js → primaryEndpoint`.

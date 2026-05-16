# Step3D lead backend endpoint contract

Фронт теперь читает `window.STEP3D_LEAD_CONFIG` из `assets/lead-config.js`.

## Как переключить endpoint

В `assets/lead-config.js` заменить:

```js
primaryEndpoint: ''
```

на URL backend/API, например Apps Script Web App, Railway или Firebase Function.
`formSubmitEndpoint` оставить как fallback.

## Ожидаемый запрос

`POST multipart/form-data` или совместимый `FormData`.

Поля:
- `projectId`
- `name`
- `email`
- `contact`
- `projectType` / `service`
- `task` / `description`
- `deadline`
- `quantity`
- `dimensions`
- `hasFiles` / `files`
- `source`
- `page`
- `utm_*`
- `referrer`
- `submittedAt` / `createdAt`

## Ожидаемый ответ

```json
{ "ok": true, "id": "S3D-...", "status": "created" }
```

Если backend недоступен, фронт показывает ручной fallback: Telegram/email и сохраняет заявку локально.

## Server-side validator

Использовать:

```bash
python3 scripts/validate_lead_payload.py --sample
python3 scripts/lead_router.py --sample --json
python3 scripts/append_lead_to_sheet.py --sample --dry-run
```

## MVP backend обязанности

1. Валидировать payload по `data/lead_schema.json`.
2. Присвоить/принять `projectId`.
3. Записать лид в Google Sheet/CRM.
4. Вернуть JSON `{ok:true}`.
5. Не хранить приватные файлы публично.
6. Для файлов выдавать приватную upload-ссылку или принимать ссылку на Drive/Telegram.

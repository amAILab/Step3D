# Step3D Backend/Auth MVP

Цель: безопасно перейти от статического preview/PWA к рабочему кабинету и Telegram Mini App, где можно хранить заявки, статусы, файлы и историю решений.

## Что уже есть

- Статический сайт и PWA: `/`, `/app/`, `/account/`, `/viewer/`.
- Форма заявки через FormSubmit.
- Локальная схема заявки: `data/lead_schema.json`.
- Dry-run роутер: `scripts/lead_router.py`.
- Google Sheet CRM/CMS как операционный слой, но не единственный production-источник.
- Проверка Telegram `initData` для будущего backend: `scripts/verify_telegram_init_data.py`.

## Минимальная архитектура

```text
Telegram Mini App / PWA
        |
        | HTTPS JSON
        v
Step3D Backend API
        |
        +-- Verify Telegram initData / одноразовый magic-link
        +-- Validate lead payload by data/lead_schema.json
        +-- Store project card + status history
        +-- Store files in private bucket/folder
        +-- Append normalized row to CRM Sheet
        +-- Notify manager in Telegram/email
```

## MVP API

### `POST /api/auth/telegram`

Вход: raw `initData` из Telegram WebApp.

Проверки:
1. HMAC `hash` по алгоритму Telegram WebApp.
2. `auth_date` не старше 24 часов.
3. `user.id` не используется как единственное право доступа: он только идентификатор клиента.

Ответ:

```json
{
  "sessionToken": "short-lived-jwt-or-random-session-id",
  "expiresIn": 86400,
  "client": { "telegramId": "7260915527" }
}
```

### `POST /api/leads`

Вход: заявка из `/app/` или `/viewer/`.

Обязательные поля:
- `contact`;
- `description`;
- `leadSource`;
- `files` или явная пометка, что файлы будут досланы позже.

Backend делает:
1. Валидацию payload.
2. Нормализацию в формат CRM.
3. Создание `projectId` вида `S3D-YYYYMMDD-001`.
4. Запись в хранилище/таблицу.
5. Уведомление менеджеру.

### `GET /api/projects/:projectId`

Возвращает карточку проекта только если клиент авторизован и проект связан с его контактом/Telegram ID.

```json
{
  "projectId": "S3D-20260517-001",
  "status": "needs-input",
  "nextStep": "Дослать 2 ракурса и критичный размер в мм",
  "route": "CAD/STL по фото → проверка → печать",
  "risks": ["По одному фото нельзя гарантировать посадки"],
  "files": [],
  "updatedAt": "2026-05-17T00:00:00+03:00"
}
```

### `POST /api/projects/:projectId/files`

Только после auth. Файлы не хранятся на GitHub Pages.

Правила:
- лимит размера на MVP: 50–100 МБ;
- whitelist расширений: `stl`, `step`, `stp`, `obj`, `3mf`, `zip`, `jpg`, `png`, `pdf`;
- приватное хранение;
- ссылка с ограниченным сроком жизни для скачивания.

## Безопасность

- Не доверять Telegram `initData` на фронте: проверка только на backend.
- Не хранить приватные файлы в репозитории или GitHub Pages.
- Не показывать реальные статусы проекта без авторизации.
- Не логировать токены, raw session tokens и приватные файлы.
- CORS разрешать только домены Step3D/Mini App.
- Rate limit на заявки и загрузку файлов.

## Где запускать первым этапом

Рекомендация: начать с маленького backend на Railway/Fly/VPS или локальном сервере Никиты за туннелем только для тестов.

Для production безопаснее внешний HTTPS-хостинг, потому что домашний ПК может быть недоступен, а для Telegram Mini App нужен стабильный HTTPS.

## Definition of Done для backend MVP

- `scripts/verify_telegram_init_data.py --self-test` проходит.
- `POST /api/leads` создаёт projectId и нормализованную заявку.
- Заявка попадает в CRM/лог и отправляет уведомление менеджеру.
- `/account/` может открыть демо или реальную карточку по session token.
- Файлы не попадают в публичный репозиторий.
- Healthcheck проекта включает проверку Telegram initData verifier.

# Step3D Google Sheet CMS / content registry

Google Sheet используется не как единственный источник сайта, а как удобная редакционная CMS-таблица.

Таблица: https://docs.google.com/spreadsheets/d/1MfJmmxDq2WNpfAoUsiPQktpj7Y5N12Dc6fKYGvu6D2Y/edit

## Почему так лучше

- GitHub остаётся источником опубликованного сайта и истории изменений.
- Google Sheet удобен для правок текстов, идей, FAQ, кейсов, backlog и статусов без копания в HTML.
- Генерацию сайта из Sheet можно включить позже и только для выбранных блоков.
- Нет риска случайно сломать продакшен одной правкой в таблице.

## Вкладки

- `Leads` — CRM заявок.
- `Settings` — рабочие настройки проекта.
- `Content` — тексты блоков сайта: hero, CTA, описания, секции.
- `Cases` — кейсы и proof-of-work.
- `FAQ` — вопросы/ответы и schema-кандидаты.
- `Pages` — реестр страниц, SEO-title, H1, description, keyword, CTA.
- `Backlog` — задачи развития сайта/кабинета/backend.

## Скрипты

```bash
python3 scripts/export_content_sheet.py --dry-run
python3 scripts/export_content_sheet.py --out data/content_export.json
```

Пока экспорт не перезаписывает сайт. Это осознанно: сначала таблица как реестр, потом аккуратная генерация отдельных блоков.

## Правило работы

1. Идеи, FAQ, кейсы, тексты и backlog можно заносить в Sheet.
2. Для публикации на сайте: экспорт → review diff → правка HTML/генератора → `project_healthcheck` → commit/push/deploy.
3. Не делать Google Sheet единственным источником правды для production без отдельного backend/generation review.

## Контроль заполнения

Таблица считается рабочей, если заполнены вкладки `Settings`, `Content`, `Cases`, `FAQ`, `Pages`, `Backlog` и проходит аудит:

```bash
python3 scripts/audit_content_sheet.py
python3 scripts/export_content_sheet.py --out data/content_export.json
```

Минимальные пороги аудита: Content ≥ 8 строк, Cases ≥ 4, FAQ ≥ 8, Pages ≥ 25, Backlog ≥ 8.

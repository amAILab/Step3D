# Step3D project audit — 2026-05-16

## Итоговая оценка

Step3D сейчас выглядит как полноценный коммерческий preview/landing: понятный оффер, SEO-посадочные, галерея работ, кейсы, форма заявки, lead-monitor и backend-ready слой.

Оценка состояния после спринтов: **8.7 / 10**.

## Сильные стороны

- Чёткий фокус: оценка и изготовление 3D-детали по фото, образцу или STL.
- Есть коммерческая структура: hero → сценарии → доверие → кейсы → стоимость → заявка.
- SEO-слой: sitemap, canonical, service pages, FAQ schema, LocalBusiness/Service JSON-LD.
- Доказательства: галерея из Telegram-канала, кейсы, публичные материалы.
- Форма заявки не требует email, основа контакта — телефон/Telegram.
- Заявки маршрутизируются на `projects.step3d@gmail.com` и копию `stepgptai@gmail.com`.
- Добавлен backend-ready слой: schema, validator, dry-run router, lead monitor self-test.

## Риски

- Production всё ещё статический GitHub Pages + FormSubmit; нет собственного server API.
- FormSubmit может требовать подтверждения адреса и зависит от внешнего сервиса.
- Нет реальной загрузки файлов в форму: файлы отправляются через Telegram.
- Нет CRM/таблицы для автологирования лидов; мониторинг работает через Gmail.
- Сайт быстро растёт, часть CSS накоплена итерационно — нужен будущий refactor в отдельные CSS-модули.
- GitHub Actions предупреждает про будущую замену Node.js 20 в actions.

## Следующие 5 улучшений

1. Поднять собственный lead API: Cloudflare Worker / Railway / ПК Никиты через Cloudflare Tunnel.
2. Добавить запись лидов в Google Sheet/CRM и карточки в `TASK_INBOX.md`.
3. Сделать upload flow: файлы в Telegram сейчас норм, но можно добавить Drive/worker upload.
4. Разнести CSS: base, layout, components, mobile, pages.
5. Настроить базовую аналитику событий: Telegram click, form submit, copy template, quiz route.

## Проверка качества

Запускать перед каждым деплоем:

```bash
python3 scripts/project_healthcheck.py
python3 scripts/validate_site.py
python3 scripts/validate_lead_payload.py --sample
python3 scripts/lead_router.py --sample --json
python3 scripts/check_step3d_leads.py --self-test
git diff --check
```


## Локальный журнал лидов

- `scripts/lead_router.py --write-log` пишет нормализованную заявку в `data/leads_log.jsonl`.
- `scripts/lead_router.py --write-task` создаёт карточку в `../TASK_INBOX.md`.
- По умолчанию роутер работает в `dry-run` и не отправляет внешние сообщения.


## Google Sheet CRM

- Таблица: Step3D Leads CRM — https://docs.google.com/spreadsheets/d/1MfJmmxDq2WNpfAoUsiPQktpj7Y5N12Dc6fKYGvu6D2Y/edit
- Конфиг: `data/google_sheet_config.json`.
- Dry-run проверки: `python3 scripts/append_lead_to_sheet.py --sample --dry-run`.
- Реальная запись валидированной заявки: `python3 scripts/append_lead_to_sheet.py < lead.json`.

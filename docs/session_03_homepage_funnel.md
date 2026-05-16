# Session 03 — главная как вход в продукт

Цель: сделать главную не витриной всех возможностей сразу, а спокойным входом в основной путь Step3D App.

## Что изменено

- Header-навигация сокращена до 4 пунктов:
  - App
  - Услуги
  - Кейсы
  - Стоимость
- Мобильное нижнее меню сокращено до 4 действий:
  - Главная
  - Услуги
  - Кейсы
  - Заявка
- Hero теперь имеет 2 действия вместо 3:
  1. `Создать заявку в App`
  2. `Посмотреть услуги`
- Viewer убран с первого экрана как конкурирующий CTA. Он остаётся доступен ниже и из app/viewer-flow.
- Спрятаны верхние маркетинговые полосы `conversion-strip`, `answer-proof-strip`, `design-soft-cta--top`, чтобы первый путь был легче.
- App закреплён как основной funnel: `главная → app/#app-brief → номер S3D → файлы/статус`.

## Проверки

- `python3 scripts/project_healthcheck.py` → OK
- `python3 scripts/validate_site.py` → OK
- `python3 scripts/check_analytics_events.py` → OK
- `python3 scripts/check_request_flow.py` → OK
- `python3 scripts/check_backend_templates.py` → OK

## Итог

Главная стала ближе к Ollama-like логике: меньше навигационного шума, один главный вход, маркетинг ниже. Следующая сессия — форма заявки/fallback: сделать отправку ещё короче и честнее относительно backend/FormSubmit.

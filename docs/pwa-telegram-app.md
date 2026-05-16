# Step3D PWA and Telegram app architecture

## Что реализовано

- Installable PWA manifest: `assets/site.webmanifest`.
- Service Worker: `service-worker.js` — базовый cache для главной, кабинета, галереи, иконок и install script.
- Install CTA: `assets/pwa-install.js` — Android/Chrome install prompt + iOS подсказка через «Поделиться → На экран Домой».
- Shortcuts: заявка, личный кабинет, галерея.

## Почему PWA первым слоем

PWA работает с текущим GitHub Pages без сервера: пользователь может открыть сайт, добавить на экран телефона и быстро возвращаться к заявке/кабинету/контактам.

## Telegram слой

Следующий оптимальный вариант — не отдельная копия сайта, а Telegram Mini App entrypoint на тот же интерфейс:

1. Backend/auth для реальных кабинетов и файлов.
2. Telegram bot button → WebApp URL `https://amailab.github.io/Step3D/` или отдельный `/app/`.
3. Проверка Telegram initData на backend, если появятся персональные данные.
4. Leads и content остаются в Google Sheet/CRM как операционный слой.

## Ограничение

Нельзя хранить приватные файлы и реальные статусы заказов только в GitHub Pages/PWA. Для этого нужен backend/auth и хранилище файлов.

## Step3D App как основной хаб

Стартовая страница PWA теперь `/app/`, а `start_url` manifest ведёт на `/Step3D/app/?source=pwa`.

Назначение `/app/`:

- основной вход для клиента с телефона;
- заявка и быстрый Telegram/AI-агент;
- кабинет и демо карточки проекта;
- контакты, канал, галерея;
- объяснение безопасного обновления через GitHub deploy + service worker.

Обновление приложения:

1. контент/идеи фиксируются в Google Sheet CRM/CMS;
2. изменения проходят через GitHub diff/review;
3. `project_healthcheck` и `validate_site`;
4. deploy GitHub Pages;
5. `service-worker.js` получает новую cache version и подтягивает обновления.

Для реальной коммуникации внутри кабинета следующий обязательный слой — backend/auth и хранилище файлов.

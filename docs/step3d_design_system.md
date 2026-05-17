# Step3D Design System v1

## Цель

Собрать UX/UI Step3D в управляемую систему вместо каскада inline CSS и аварийных `!important`.

## Файлы

- `assets/step3d-design-system.css` — токены и utility-классы.
- `assets/ux-ui-100.css` — текущий premium product layer поверх старого сайта.

## Принципы

1. Один главный путь: главная → заявка → номер S3D → файлы в Telegram → карточка заявки.
2. Primary CTA — чёрный.
3. Secondary CTA — белый с тонкой границей.
4. Синий — только статус/ссылка/выбор.
5. Viewer — необязательный путь для тех, у кого уже есть STL/OBJ/3MF.
6. Account — карточка заявки, не настоящий кабинет без backend/auth.
7. На mobile показывать меньше: один CTA, 1–2 trust-сигнала, 3 пункта bottom nav.

## Следующий рефакторинг

Постепенно переносить inline `<style>` из HTML в компоненты:

- `home.css`;
- `app.css`;
- `viewer.css`;
- `account.css`;
- `components.css`;
- `mobile.css`.

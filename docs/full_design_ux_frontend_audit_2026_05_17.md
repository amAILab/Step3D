# Step3D — полный UX/UI/frontend аудит и production pass (2026-05-17)

## Инвентаризация
Проверены статические страницы: главная, app, account, account/demo, viewer, services, cases, articles, guide, gallery, workshops, 3d-printing, 3d-scan, 3d-modeling, cad-modeling, photo-to-cad, reverse-engineering, urgent-spare-parts, small-batch-production, industrial-parts, stl-po-foto, education-materials, privacy, thanks, files/logopedia-report, 404. Проверены также service-worker.js, sitemap.xml, robots.txt, data/*, scripts/*.

## Найденные системные проблемы
- Разные слои CSS (`mobile-readability`, `minimal-ui`, `ux-ui-100`, inline CSS) конфликтовали по фону, цветам, радиусам и кнопкам.
- Большинство сервисных страниц жили на собственном inline CSS и подключали только mobile-readability, поэтому визуально расходились с app/viewer/home.
- Существовали разные версии карточек, кнопок, бейджей, dark/CTA-блоков, полей и mobile bottom/nav.
- Mobile-readability решал контраст, но уводил бренд в сине-серую системность вместо premium industrial.
- Focus states были частично добавлены, но не покрывали все страницы с inline CSS.
- Для GitHub Pages важно сохранить статическую архитектуру без сборщика.

## Что сделано
- Добавлен единый финальный слой `assets/step3d-premium-system.css`: токены, типографика, сетки, карточки, кнопки, формы, focus-visible, reduced motion, mobile правила, dark/CTA-блоки.
- Подключён этот слой ко всем HTML-страницам без удаления SEO/OG/canonical/analytics/form маршрутов.
- Добавлен skip-link и `main#main` для базовой клавиатурной доступности.
- Сохранена директория `photos_do_not_touch/`: не редактировалась.
- Статическая модель проекта сохранена: без Vite/Webpack/тяжёлого сборщика.

## Проверки
- `python3 scripts/check_ux_ui_100.py`
- `python3 scripts/check_release_readiness.py`
- `python3 scripts/validate_site.py`
- `python3 scripts/check_seo_trust.py`

## Следующий уровень
- Позже стоит постепенно убрать inline CSS из сервисных страниц в компонентные файлы, но текущий pass уже нормализует внешний вид production-safe поверх существующей архитектуры.

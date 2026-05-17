# Session 09 — SEO / trust / B2B без перегруза

Цель: усилить доверие, SEO и B2B-сигналы, но не ломать минимальный путь `главная → App → заявка → проект`.

## Что изменено

### Компактный trust layer

На главную добавлен небольшой блок `Доверие без лишнего шума`:

- Москва: координация, встречи и выдача по договорённости;
- Файлы и NDA: закрытые задачи можно начать с NDA;
- B2B-документы: счёт, договор и этапы после первичной оценки;
- Честный маршрут: CAD, скан, печать, серия или отказ от 3D-печати, если это лучше.

Блок стоит ниже основных объяснений и не конкурирует с главным CTA.

### B2B без тяжёлого лендинга

B2B-карточка стала спокойнее визуально:

- белая поверхность вместо тяжёлой тёмной карточки;
- текст стал менее рекламным;
- акцент на вводные, риски и маршрут, а не на обещания.

### App structured data

В `app/index.html` добавлен JSON-LD `WebApplication`:

- название: `Step3D App`;
- категория: `BusinessApplication`;
- назначение: заявка, номер проекта, файлы инженеру;
- provider: `Step3D`.

### SEO/trust smoke check

Добавлен `scripts/check_seo_trust.py`, который проверяет:

- компактный trust block на главной;
- B2B/NDA/документные сигналы;
- `LocalBusiness` и `FAQPage`;
- `WebApplication` schema для App.

## Проверки

- `python3 scripts/project_healthcheck.py` → OK
- `python3 scripts/validate_site.py` → OK
- `python3 scripts/check_analytics_events.py` → OK
- `python3 scripts/check_request_flow.py` → OK
- `python3 scripts/check_backend_templates.py` → OK
- `python3 scripts/check_seo_trust.py` → OK
- `git diff --check` → OK

## Итог

SEO/trust/B2B слой усилен без перегруза первого экрана. Step3D остаётся минимальным сервисным продуктом: один главный путь, но ниже есть достаточно доверия для компаний и инженерных клиентов.

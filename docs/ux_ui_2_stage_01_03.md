# UX/UI 2.0 — этапы 1–3

Закрыт первый пакет после 5 экспертных аудитов.

## Этап 1 — честный naming и CTA

- Пользовательские формулировки смещены от “App/кабинет” к более честным:
  - `Заявка Step3D`;
  - `Карточка заявки`;
  - `Рассчитать по фото / STL`.
- Это снижает риск ложного ожидания полноценного backend/auth кабинета.

## Этап 2 — mobile-first первый экран

- Главная сильнее ведёт в один путь: расчёт по фото/STL.
- Viewer явно обозначен как необязательный: если файла нет, можно начать с фото и описания.

## Этап 3 — заявка как честный старт

- В App добавлен honesty-banner:
  - после номера нужно дослать фото/STL/STEP в Telegram;
  - если отправка не подтвердится, это черновик, а не принятый проект.
- В блоке файлов добавлена подсказка: файлы можно дослать после номера S3D.
- В Account добавлен preview-banner: GitHub Pages не хранит приватные файлы и не заменяет подтверждение менеджера.
- В Viewer добавлен banner: Viewer необязателен.

## Проверки

- `python3 scripts/project_healthcheck.py` → OK
- `python3 scripts/validate_site.py` → OK
- `python3 scripts/check_request_flow.py` → OK
- `python3 scripts/check_release_readiness.py` → OK
- `python3 scripts/check_seo_trust.py` → OK
- `git diff --check` → OK

## Следующие этапы

4. Submit/fallback: усилить честность success/fail и Telegram action.
5. File intake: сделать чеклист файлов видимее и проще.
6. Viewer: ещё сильнее упростить мобильный сценарий.
7. Account: статусная карточка без ощущения настоящего кабинета.
8. Accessibility: menu/modal/tabs/form errors.
9. Visual system cleanup.
10. Release 2.0 audit.

# Step3D — DESIGN / UX / UI / Frontend audit

Дата: 2026-05-17  
Публикация: https://amailab.github.io/Step3D/  
Репозиторий: `amAILab/Step3D`  
Формат проекта: статический GitHub Pages, без сборщика.

## 1. Инвентаризация

Проверены ключевые части проекта:

- Главная: `index.html`
- Приложения/сервисы: `app/`, `account/`, `account/demo/`, `viewer/`
- Услуги: `services/`, `3d-printing/`, `3d-scan/`, `3d-modeling/`, `cad-modeling/`, `photo-to-cad/`, `reverse-engineering/`, `urgent-spare-parts/`, `small-batch-production/`, `industrial-parts/`, `stl-po-foto/`, `workshops/`, `education-materials/`
- Контент: `cases/`, `articles/`, `guide/`, `gallery/`, `files/logopedia-report.html`
- Служебные страницы: `thanks/`, `privacy/`, `404.html`
- Технические файлы: `assets/*.css`, `assets/*.js`, `service-worker.js`, `sitemap.xml`, `robots.txt`, `backend/google-apps-script/`, `scripts/`

Директория `photos_do_not_touch/` не редактировалась.

## 2. Что было найдено

### Критичные / важные проблемы

1. **Разъехавшаяся дизайн-система**
   - На страницах одновременно работали inline CSS, `mobile-readability.css`, `minimal-ui.css`, `ux-ui-100.css`, `ux-ui-10.css`, `step3d-design-system.css`.
   - Карточки, кнопки, формы, footer, header и CTA выглядели по-разному на разных страницах.

2. **Недостаточная связность продукта**
   - `app`, `viewer`, `account` ощущались как отдельные интерфейсы, а не как единый маршрут Step3D.
   - Пользователю не всегда было ясно: можно ли начать без STL, что прислать, где будет номер заявки, что делать B2B-клиенту.

3. **Конверсионная логика требовала усиления**
   - Были CTA и форма, но не хватало явной карты сценариев: сломалась деталь, прототип, реверс-инжиниринг, малая серия, мастер-класс, B2B.
   - На длинных страницах услуг CTA могли теряться.

4. **Accessibility / WCAG AA риски**
   - Были изображения без `alt`.
   - В части форм не хватало явных label/for.
   - Были inline `onclick` во Viewer.
   - Нужно было усилить focus states, skip link, touch targets, reduced motion.

5. **Responsive / горизонтальный скролл**
   - На ширине 1024px обнаруживался document-level overflow из-за footer/grid и горизонтальной media strip.
   - На переходных ширинах 768–1024px некоторые сетки выглядели неидеально.

6. **Performance / кэширование**
   - Главная остаётся тяжёлой из-за большого inline CSS/HTML и DOM.
   - `service-worker.js` мог сорвать установку кэша, если один ресурс не загрузился.
   - Новый финальный CSS должен был попадать в precache, чтобы не показывался старый интерфейс.

## 3. Что исправлено

### Дизайн-система

- Добавлен единый production-safe CSS слой: `assets/step3d-premium-system.css`.
- Введены единые токены: фон, поверхности, цвет текста, muted, line, радиусы, тени, focus, touch target.
- Нормализованы:
  - кнопки primary/secondary/ghost;
  - карточки;
  - формы;
  - таблицы;
  - CTA-блоки;
  - dark/proof секции;
  - мобильные action bars;
  - header/footer поведение;
  - focus-visible;
  - reduced motion.

### UX и конверсия

- Усилен квиз на главной.
- Добавлен сценарий `B2B / команда / закупка`.
- Добавлена карта маршрутов:
  - сломалась деталь;
  - нужен прототип;
  - реверс-инжиниринг;
  - малая серия;
  - мастер-класс;
  - B2B.
- Добавлены спокойные повторные CTA на страницах услуг.
- Усилены блоки доверия: сроки, риски, тестовый образец, NDA, документы, честный отказ от печати, если метод не подходит.
- Улучшены сценарии `App`, `Viewer`, `Account`:
  - можно начать без 3D-файла;
  - файлы можно дослать после номера S3D;
  - Viewer необязателен;
  - B2B может начать с NDA/счёта/этапов.

### Accessibility

- Проставлены `alt` для изображений: проверка показала `missing_alt = 0`.
- Добавлены/усилены label/for в Viewer, Account и микро-калькуляторе.
- Убраны inline `onclick` из Viewer: проверка показала `onclick = 0`.
- Добавлены skip-link и `main#main`.
- Проверено: на каждой HTML-странице ровно один H1.
- Усилены focus states, touch targets ≥ 44px, reduced motion.

### Responsive

Проверены ширины:

- 320px
- 375px
- 390px
- 430px
- 768px
- 1024px
- 1280px
- 1440px
- 1920px

Исправлено:

- document-level overflow на 1024px;
- footer overflow на tablet;
- горизонтальная media strip на tablet;
- quiz layout на tablet;
- переходные сетки 901–1100px;
- таблицы и длинные ссылки;
- overflow в карточках и CTA.

### Performance / service worker

- Изображения получили `loading="lazy"` и `decoding="async"`, кроме priority hero-ресурсов.
- `service-worker.js` обновлён до `step3d-pwa-v4`.
- В precache добавлены CSS-слои, включая `assets/step3d-premium-system.css`.
- Установка service worker переведена на `Promise.allSettled`, чтобы один недоступный ресурс не ломал весь install.

### SEO / Pages

- Сохранены canonical, robots, sitemap, OG/Twitter metadata.
- Проверены sitemap/robots.
- GitHub Pages не переведён на сборщик, статическая архитектура сохранена.
- Проверено, что Pages deploy успешен.

## 4. Изменённые файлы

Основные:

- `index.html`
- `app/index.html`
- `viewer/index.html`
- `account/index.html`
- `files/logopedia-report.html`
- `assets/step3d-premium-system.css`
- `service-worker.js`
- `DESIGN_AUDIT.md`
- `docs/full_design_ux_frontend_audit_2026_05_17.md`
- `scripts/audit_step3d_quality.py`

Страницы услуг с добавленным conversion checkpoint:

- `services/index.html`
- `3d-printing/index.html`
- `3d-scan/index.html`
- `3d-modeling/index.html`
- `cad-modeling/index.html`
- `photo-to-cad/index.html`
- `reverse-engineering/index.html`
- `urgent-spare-parts/index.html`
- `small-batch-production/index.html`
- `industrial-parts/index.html`
- `stl-po-foto/index.html`
- `workshops/index.html`

## 5. Проверки

Запускались команды:

```bash
python3 scripts/check_ux_ui_100.py
python3 scripts/check_release_readiness.py
python3 scripts/validate_site.py
python3 scripts/check_seo_trust.py
python3 scripts/audit_step3d_quality.py
node /tmp/check_responsive_cdp.mjs
node /tmp/perf_smoke.mjs
gh run watch <pages-run-id> --repo amAILab/Step3D --exit-status
curl -I -L https://amailab.github.io/Step3D/
```

Результат:

- `UX_UI_100_CHECK_OK`
- `RELEASE_READINESS_OK`
- `Step3D validation ok: 32 HTML files checked, local links ok, JS ok`
- `SEO_TRUST_CHECK_OK`
- `QUALITY_AUDIT_OK`
- responsive/horizontal overflow: 108 проверок, issues = 0
- missing alt: 0
- inline onclick: 0
- H1 не по одному: 0 страниц
- GitHub Pages deploy: success

## 6. Как проверить вручную

1. Открыть главную:
   - https://amailab.github.io/Step3D/
2. Проверить на мобильном:
   - 320, 375, 390, 430px.
3. Проверить tablet/desktop:
   - 768, 1024, 1280, 1440, 1920px.
4. Пройти сценарии:
   - квиз → B2B;
   - сломалась деталь → запчасть по фото;
   - прототип → модель под печать;
   - Viewer без файла → заявка по фото;
   - App → форма заявки;
   - Account → B2B actions.
5. Проверить CTA:
   - Telegram ведёт на `https://t.me/step_3d_mngr` или канал Step3D там, где это канал;
   - формы ведут на `https://formsubmit.co/projects.step3d@gmail.com`;
   - заявки ведут на `#brief` или `app/#app-brief`.
6. В DevTools Application → Service Workers:
   - убедиться, что активен новый cache `step3d-pwa-v4`;
   - при необходимости нажать Update/Unregister для ручной проверки чистого состояния.

## 7. Компромиссы

- Полный вынос inline CSS/JS из `index.html`, `app`, `viewer`, `account` не выполнен в этом проходе, чтобы не сломать production и GitHub Pages.
- Вместо рискованного большого рефакторинга добавлен финальный дизайн-системный слой, который стабилизирует вид без изменения статической архитектуры.
- Главная всё ещё содержит большой DOM и inline CSS; это главный следующий технический долг.
- Viewer всё ещё зависит от CDN Three.js, но fallback и маршрут “заявка без Viewer” усилены.

## 8. Рекомендации на следующий этап

1. Постепенно вынести inline CSS из `index.html` в компонентные CSS-файлы.
2. Вынести JS из главной, App и Viewer в отдельные модули.
3. Ужесточить CSP после удаления inline script/style.
4. Сделать локальный fallback для Three.js или отдельную lightweight-загрузку Viewer.
5. Провести Lighthouse в браузере на опубликованной версии после прогрева GitHub Pages cache.
6. При подключении backend/auth отделить preview-кабинет от приватного хранилища файлов.

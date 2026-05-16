from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]

BASE_CSS = """
:root{--bg:#f5f5f2;--surface:#fff;--soft:#efefec;--ink:#101010;--muted:#5e5e59;--line:#ddd;--radius:28px;--max:1120px}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 12% 0%,rgba(37,99,235,.075),transparent 26%),linear-gradient(180deg,#f7f8f6 0%,var(--bg) 45%,#eef3fb 100%);color:var(--ink);font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;line-height:1.55;letter-spacing:-.015em}a{color:inherit;text-decoration:none}.container{width:min(100% - 40px,var(--max));margin:0 auto}.header{position:sticky;top:0;background:rgba(245,245,242,.9);backdrop-filter:blur(16px);border-bottom:1px solid var(--line);z-index:10}.head{min-height:72px;display:flex;align-items:center;justify-content:space-between;gap:18px}.brand{font-weight:900;font-size:1.25rem}.nav{display:flex;gap:10px;flex-wrap:wrap}.btn{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:12px 16px;border:1px solid var(--ink);font-weight:800}.btn.primary{background:linear-gradient(135deg,#111827,#0f172a 58%,#1d4ed8);color:white;box-shadow:0 14px 34px rgba(15,23,42,.16)}.btn.ghost{background:transparent}.btn:hover{transform:translateY(-1px)}.hero{padding:86px 0 52px}.eyebrow{text-transform:uppercase;font-weight:900;letter-spacing:.13em;font-size:.78rem;color:var(--muted);margin:0 0 10px}h1{font-size:clamp(2.4rem,6vw,5.6rem);line-height:.92;letter-spacing:-.075em;margin:0 0 22px;max-width:920px}h2{font-size:clamp(1.7rem,3vw,3.2rem);line-height:1;letter-spacing:-.055em;margin:0 0 16px}h3{font-size:1.25rem;margin:0 0 8px}.lead{font-size:clamp(1.08rem,2vw,1.35rem);color:var(--muted);max-width:790px;margin:0 0 28px}.section{padding:44px 0}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{background:rgba(255,255,255,.84);border:1px solid rgba(148,163,184,.30);border-radius:var(--radius);padding:24px;box-shadow:0 18px 55px rgba(15,23,42,.08)}.card p,.muted{color:var(--muted);margin:0}.list{padding:0;margin:14px 0 0;list-style:none;display:grid;gap:10px}.list li{display:flex;gap:9px;color:var(--muted)}.list li:before{content:'→';font-weight:900;color:var(--ink)}.trust-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.trust-card{background:var(--soft);border:1px solid var(--line);border-radius:22px;padding:18px}.trust-card strong{display:block;margin-bottom:6px}.trust-card p{color:var(--muted);margin:0}.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.step{background:var(--soft);border:1px solid var(--line);border-radius:22px;padding:18px}.step strong{display:block;font-size:1.7rem;letter-spacing:-.06em;margin-bottom:8px}@media(max-width:860px){.steps,.trust-grid{grid-template-columns:1fr 1fr}}@media(max-width:560px){.steps,.trust-grid{grid-template-columns:1fr}}.split{display:grid;grid-template-columns:1.05fr .95fr;gap:18px;align-items:start}.image{border-radius:var(--radius);overflow:hidden;border:1px solid var(--line);background:var(--soft)}.image img{width:100%;display:block}.cta{background:var(--ink);color:#fff;border-radius:34px;padding:32px;display:grid;grid-template-columns:1fr auto;gap:20px;align-items:center}.cta p{color:#ddd;margin:0}.footer{padding:52px 0 36px;color:var(--muted);background:#eeeeea;border-top:1px solid var(--line)}.footer-map{display:grid;grid-template-columns:1.35fr repeat(4,minmax(0,1fr));gap:26px;align-items:start}.footer-brand strong{display:block;color:var(--ink);font-size:1.18rem;margin-bottom:8px}.footer-brand p{margin:0;max-width:300px}.footer-col h3{margin:0 0 12px;color:var(--ink);font-size:.95rem}.footer-col ul{list-style:none;margin:0;padding:0;display:grid;gap:9px}.footer-col a{color:var(--muted)}.footer-col a:hover{color:var(--ink);text-decoration:underline}.footer-bottom{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-top:1px solid var(--line);margin-top:32px;padding-top:20px}@media(max-width:860px){.grid,.split,.cta{grid-template-columns:1fr}.footer-map{grid-template-columns:1fr 1fr}.footer-brand{grid-column:1/-1}.hero{padding-top:56px}.nav{display:none}h1{font-size:3rem}}@media(max-width:560px){.footer-map{grid-template-columns:1fr}.footer-brand{grid-column:auto}.footer-bottom{display:grid}}@media(max-width:760px){.mobile-fixed-menu{position:fixed!important;left:10px!important;right:10px!important;bottom:calc(10px + env(safe-area-inset-bottom,0px))!important;z-index:120!important;display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:6px!important;padding:7px!important;border:1px solid rgba(17,24,39,.13)!important;border-radius:22px!important;background:rgba(255,255,255,.94)!important;backdrop-filter:blur(18px)!important;box-shadow:0 16px 42px rgba(15,23,42,.18)!important;box-sizing:border-box!important}.mobile-fixed-menu .mobile-menu-item{min-width:0!important;min-height:42px!important;display:flex!important;align-items:center!important;justify-content:center!important;padding:8px 6px!important;border-radius:15px!important;color:#111827!important;background:rgba(245,245,242,.9)!important;font-size:12.5px!important;font-weight:850!important;line-height:1.05!important;text-align:center!important;white-space:normal!important;text-decoration:none!important}.mobile-fixed-menu .mobile-menu-item--accent{color:#fff!important;background:linear-gradient(135deg,#111827,#1d4ed8)!important}.site-footer{padding-bottom:calc(110px + env(safe-area-inset-bottom,0px))!important}}@media(max-width:900px){*,*::before,*::after{box-sizing:border-box}html,body{width:100%;max-width:100%;overflow-x:hidden}.container{width:calc(100vw - 28px);max-width:calc(100vw - 28px);padding:0;margin-left:auto;margin-right:auto}.head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px}.brand{min-width:0;overflow:hidden;white-space:nowrap}.nav{display:none}.btn{width:100%;max-width:100%;white-space:normal;text-align:center}.hero{padding:44px 0 34px}.grid,.split,.cta,.footer-map{grid-template-columns:1fr}.hero .split{display:block}h1{font-size:clamp(2rem,8.6vw,2.45rem);line-height:1.04;letter-spacing:-.045em;overflow-wrap:anywhere}h2{font-size:clamp(1.55rem,7vw,2.1rem);line-height:1.06;overflow-wrap:anywhere}.lead,p,li{overflow-wrap:anywhere}.image{margin-top:18px}.cta{padding:24px}.footer-map{gap:18px}.footer-brand{grid-column:auto}}
"""

TRUST_SECTION = """<section class="section" aria-labelledby="trust-title"><div class="container"><p class="eyebrow">Почему можно доверять</p><h2 id="trust-title">Перед запуском предупреждаем о рисках</h2><div class="trust-grid"><div class="trust-card"><strong>Проверяем геометрию</strong><p>Смотрим толщины, посадки, масштаб и слабые места до печати.</p></div><div class="trust-card"><strong>Подбираем технологию</strong><p>Не обещаем одну кнопку: выбираем материал и метод под задачу.</p></div><div class="trust-card"><strong>Работаем с файлами</strong><p>Принимаем STL, STEP, 3MF, OBJ, фото, эскиз или физическую деталь.</p></div><div class="trust-card"><strong>Фиксируем вводные</strong><p>Срок, количество, внешний вид и прочность уточняем до запуска.</p></div></div></div></section>"""


HEADER_FOOTER_CSS = """
.site-header{position:sticky;top:0;z-index:100;backdrop-filter:blur(18px);background:rgba(245,245,242,.9);border-bottom:1px solid rgba(211,211,207,.72)}.header-inner{min-height:74px;display:flex;align-items:center;justify-content:space-between;gap:14px;min-width:0}.brand{display:inline-flex;align-items:center;gap:12px;font-size:24px;font-weight:800;letter-spacing:-.04em;white-space:nowrap}.brand-mark{width:50px;height:42px;display:grid;place-items:center;flex:0 0 auto}.brand-logo-steel img{width:50px;height:42px;object-fit:contain;filter:drop-shadow(0 5px 8px rgba(18,18,18,.16));transform:scaleX(-1)}.nav{display:flex;align-items:center;justify-content:center;gap:4px;font-size:14px;font-weight:650;flex:1 1 auto}.nav a{padding:9px 8px;border-radius:999px;white-space:nowrap}.nav a:hover{background:#ecece8}.header-actions{display:flex;align-items:center;gap:8px}.link-avatar{display:inline-block;border-radius:50%;vertical-align:middle;margin-right:7px}.btn-primary,.btn.primary{background:linear-gradient(135deg,#111827,#0f172a 58%,#1d4ed8)!important;color:#fff!important}.btn-secondary,.btn.ghost,.btn.secondary{background:#fff;color:#111}.site-footer{padding:52px 0 36px;color:#5e5e59;background:#eeeeea;border-top:1px solid #ddd}.footer-map{display:grid;grid-template-columns:1.35fr repeat(4,minmax(0,1fr));gap:26px;align-items:start}.footer-brand strong{display:block;color:#101010;font-size:1.18rem;margin-bottom:8px}.footer-brand p{margin:0;max-width:300px}.footer-col h3{margin:0 0 12px;color:#101010;font-size:.95rem}.footer-col ul{list-style:none;margin:0;padding:0;display:grid;gap:9px}.footer-col a{color:#5e5e59}.footer-col a:hover{color:#101010;text-decoration:underline}.footer-bottom{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;border-top:1px solid #ddd;margin-top:32px;padding-top:20px}@media(max-width:900px){.header-actions{display:none}.nav{display:none}.header-inner{min-height:66px}.brand{font-size:22px}.footer-map{grid-template-columns:1fr 1fr}.footer-brand{grid-column:1/-1}}@media(max-width:560px){.footer-map{grid-template-columns:1fr}.footer-brand{grid-column:auto}.footer-bottom{display:grid}}@media(max-width:760px){.mobile-fixed-menu{position:fixed!important;left:10px!important;right:10px!important;bottom:calc(10px + env(safe-area-inset-bottom,0px))!important;z-index:120!important;display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:6px!important;padding:7px!important;border:1px solid rgba(17,24,39,.13)!important;border-radius:22px!important;background:rgba(255,255,255,.94)!important;backdrop-filter:blur(18px)!important;box-shadow:0 16px 42px rgba(15,23,42,.18)!important;box-sizing:border-box!important}.mobile-fixed-menu .mobile-menu-item{min-width:0!important;min-height:42px!important;display:flex!important;align-items:center!important;justify-content:center!important;padding:8px 6px!important;border-radius:15px!important;color:#111827!important;background:rgba(245,245,242,.9)!important;font-size:12.5px!important;font-weight:850!important;line-height:1.05!important;text-align:center!important;white-space:normal!important;text-decoration:none!important}.mobile-fixed-menu .mobile-menu-item--accent{color:#fff!important;background:linear-gradient(135deg,#111827,#1d4ed8)!important}.site-footer{padding-bottom:calc(110px + env(safe-area-inset-bottom,0px))!important}}
"""

WORLD_CLASS_CSS = r"""

/* Sticky mobile navigation polish: no redundant hamburger, safe anchor offsets. */
section, [id] { scroll-margin-top: 132px; }
@media (max-width: 760px) {
  .menu-toggle { display: none !important; }
  .header-inner { justify-content: center !important; }
  .brand { max-width: 100% !important; }
  section, [id] { scroll-margin-top: 142px !important; }
}
@media (max-width: 375px) {
  .mobile-fixed-menu { margin-left: 8px !important; margin-right: 8px !important; gap: 4px !important; padding: 5px !important; }
  .mobile-fixed-menu .mobile-menu-item { font-size: 11.5px !important; padding-left: 4px !important; padding-right: 4px !important; }
}


/* Mobile navigation final UX: visible without hamburger, sticky in document flow, no content overlay. */
.mobile-fixed-menu { display: none !important; }
@media (max-width: 760px) {
  body { padding-bottom: 0 !important; }
  main { padding-bottom: 0 !important; }
  .mobile-fixed-menu {
    position: sticky !important;
    top: 66px !important;
    left: auto !important;
    right: auto !important;
    bottom: auto !important;
    z-index: 90 !important;
    display: grid !important;
    grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
    gap: 5px !important;
    width: auto !important;
    max-width: none !important;
    margin: 8px 10px 0 !important;
    padding: 6px !important;
    border-radius: 20px !important;
    border: 1px solid rgba(198,210,223,.90) !important;
    background: rgba(255,255,255,.94) !important;
    backdrop-filter: blur(18px) !important;
    box-shadow: 0 14px 38px rgba(15,23,42,.14) !important;
    box-sizing: border-box !important;
  }
  .mobile-fixed-menu .mobile-menu-item { min-height: 38px !important; padding: 7px 5px !important; font-size: 12px !important; }
  .site-footer, footer { padding-bottom: 36px !important; }
}


/* Mobile fixed menu refinement: compact enough not to dominate content while staying always available. */
@media (max-width: 760px) {
  body { padding-bottom: calc(88px + env(safe-area-inset-bottom, 0px)) !important; }
  main { padding-bottom: 18px !important; }
  .mobile-fixed-menu { bottom: calc(8px + env(safe-area-inset-bottom, 0px)) !important; padding: 6px !important; gap: 5px !important; border-radius: 20px !important; }
  .mobile-fixed-menu .mobile-menu-item { min-height: 38px !important; padding: 7px 5px !important; font-size: 12px !important; }
  .site-footer, footer { padding-bottom: calc(118px + env(safe-area-inset-bottom, 0px)) !important; }
}


/* World-class UX/UI color system audit — premium industrial palette, higher contrast, clearer CTA hierarchy. */
:root {
  --bg: #f7f9fc !important;
  --surface: #ffffff !important;
  --surface-soft: #eef4fb !important;
  --surface-muted: #e8eef6 !important;
  --ink: #0b1220 !important;
  --muted: #475569 !important;
  --muted-2: #64748b !important;
  --line: #d8e0ea !important;
  --line-strong: #c6d2df !important;
  --accent: #2563eb !important;
  --accent-2: #06b6d4 !important;
  --accent-soft: #eaf2ff !important;
  --premium-dark: #07111f !important;
  --premium-dark-2: #0f1d31 !important;
  --premium-glow: rgba(37, 99, 235, .22) !important;
}

html { background: #f7f9fc !important; }
body {
  color: var(--ink) !important;
  background:
    radial-gradient(circle at 8% -6%, rgba(37,99,235,.13), transparent 29%),
    radial-gradient(circle at 90% 8%, rgba(6,182,212,.12), transparent 31%),
    linear-gradient(180deg, #fbfdff 0%, #f7f9fc 38%, #edf3fa 100%) !important;
}

.site-header {
  background: rgba(251,253,255,.86) !important;
  border-bottom-color: rgba(198,210,223,.72) !important;
  box-shadow: 0 10px 34px rgba(15,23,42,.045) !important;
}
.nav a:hover, .nav a:focus-visible { background: #eaf2ff !important; color: #0f3ea8 !important; }
.hero-kicker, .eyebrow { color: #1d4ed8 !important; }
.section-lead, .hero-subtitle, .lead, p, li, .muted { color: var(--muted) !important; }
h1, h2, h3, .section-title, .brand, strong { color: var(--ink) !important; }

.btn-primary, .btn.primary, .mobile-menu-item--accent {
  color: #fff !important;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 52%, #06b6d4 120%) !important;
  border-color: rgba(37,99,235,.78) !important;
  box-shadow: 0 16px 42px rgba(37,99,235,.30), inset 0 1px 0 rgba(255,255,255,.22) !important;
}
.btn-primary:hover, .btn.primary:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 22px 56px rgba(37,99,235,.36), inset 0 1px 0 rgba(255,255,255,.25) !important;
}
.btn-secondary, .btn.ghost, .btn.secondary, .btn-ghost {
  background: rgba(255,255,255,.88) !important;
  color: #0f172a !important;
  border-color: rgba(148,163,184,.55) !important;
}
.btn-secondary:hover, .btn.ghost:hover, .btn.secondary:hover, .btn-ghost:hover {
  background: #eaf2ff !important;
  border-color: rgba(37,99,235,.34) !important;
  color: #0f3ea8 !important;
}

.card, .route-card, .process-card, .service-card, .scenario-card, .timeline-item,
.price-card, .price-table, .case-card, .brief-panel, .form-panel, .micro-calc-panel,
.micro-calc-result, .article-teaser, .faq-item, .proof-card, .trust-card, .step,
.media-card, .video-card, .channel-feature, .channel-mini-card, .hero-answer-card {
  background: rgba(255,255,255,.90) !important;
  border-color: rgba(198,210,223,.82) !important;
  box-shadow: 0 18px 54px rgba(15,23,42,.075) !important;
}
.card:hover, .route-card:hover, .process-card:hover, .service-card:hover, .scenario-card:hover,
.timeline-item:hover, .case-card:hover, .article-teaser:hover, .proof-card:hover,
.channel-feature:hover, .channel-mini-card:hover {
  border-color: rgba(37,99,235,.34) !important;
  box-shadow: 0 24px 70px rgba(15,23,42,.12) !important;
}

.hero-visual, .case-media, .image {
  background:
    linear-gradient(145deg, rgba(255,255,255,.78), rgba(232,240,250,.96)),
    radial-gradient(circle at 82% 8%, rgba(37,99,235,.20), transparent 44%) !important;
  border-color: rgba(198,210,223,.82) !important;
}
.hero-card-main {
  background: linear-gradient(145deg, #ffffff, #eff6ff) !important;
  border-color: rgba(255,255,255,.88) !important;
}
.hero-chip, .price-row span, .lead-mode-tab.is-active, .quick-lead-preset:hover {
  color: #12357c !important;
  background: #eaf2ff !important;
  border-color: rgba(37,99,235,.20) !important;
}
.process-card strong, .scenario-number, .service-icon, .timeline-item strong {
  color: #1d4ed8 !important;
  background: linear-gradient(135deg, rgba(37,99,235,.12), rgba(6,182,212,.10)) !important;
  border-color: rgba(37,99,235,.20) !important;
}

.cta, .conversion-strip, .brief-cta, .final-cta, .cta-card {
  color: #fff !important;
  background:
    radial-gradient(circle at 88% 12%, rgba(6,182,212,.24), transparent 34%),
    linear-gradient(135deg, var(--premium-dark) 0%, var(--premium-dark-2) 68%, #12357c 100%) !important;
  border: 1px solid rgba(148,163,184,.22) !important;
  box-shadow: 0 24px 76px rgba(7,17,31,.26) !important;
}
.cta h2, .conversion-strip h2, .brief-cta h2, .final-cta h2, .cta-card h2,
.cta strong, .conversion-strip strong { color: #fff !important; }
.cta p, .conversion-strip p, .brief-cta p, .final-cta p, .cta-card p { color: #dbeafe !important; }
.cta .btn-primary, .conversion-strip .btn-primary, .brief-cta .btn-primary, .final-cta .btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%) !important;
  border-color: rgba(255,255,255,.32) !important;
  box-shadow: 0 18px 48px rgba(6,182,212,.30) !important;
}

.site-footer, .footer {
  color: #475569 !important;
  background: linear-gradient(180deg, #eef4fb, #e7eef7) !important;
  border-top-color: rgba(198,210,223,.86) !important;
}
.footer-col a, .site-footer a { color: #334155 !important; }
.footer-col a:hover, .site-footer a:hover { color: #1d4ed8 !important; }
.mobile-fixed-menu {
  background: rgba(255,255,255,.94) !important;
  border-color: rgba(198,210,223,.90) !important;
  box-shadow: 0 18px 50px rgba(15,23,42,.20) !important;
}
.mobile-fixed-menu .mobile-menu-item:not(.mobile-menu-item--accent) {
  color: #0f172a !important;
  background: #eef4fb !important;
}

@media (max-width: 720px) {
  body { background: linear-gradient(180deg, #fbfdff 0%, #f7f9fc 48%, #edf3fa 100%) !important; }
  .section { padding-top: 34px !important; padding-bottom: 34px !important; }
  .cta, .conversion-strip, .brief-cta, .final-cta, .cta-card { padding: 24px !important; border-radius: 28px !important; }
  .section-lead, .hero-subtitle, .lead, p { color: #475569 !important; }
}

"""

LOCAL_SECTION = """<section class="section" aria-labelledby="local-title"><div class="container"><p class="eyebrow">Локально</p><h2 id="local-title">{local_h2}</h2><div class="grid"><article class="card"><h3>Москва и область</h3><p>Можно начать с онлайн-оценки по фото, эскизу, STL/STEP или описанию задачи. Для первичного расчёта достаточно размеров, срока и назначения детали.</p><ul class="list"><li><a href="../#brief">заявка на расчёт</a></li><li><a href="../3d-printing/">3D-печать деталей</a></li></ul></article><article class="card"><h3>Вузы, технопарки и команды</h3><p>Помогаем с прототипами, демонстрационными макетами, проектными занятиями и образовательными форматами по цифровому производству.</p><ul class="list"><li><a href="../workshops/">мастер-классы и обучение</a></li><li><a href="../services/">все услуги Step3D</a></li></ul></article><article class="card"><h3>События, сцена и кейсы</h3><p>Делаем награды, бутафорию, арт-объекты и презентационные модели к конкретной дате — с учётом веса, внешнего вида и сборки.</p><ul class="list"><li><a href="../cases/">посмотреть кейсы</a></li><li><a href="../reverse-engineering/">реверс-инжиниринг</a></li></ul></article></div></div></section>"""

PAGES = {

    'stl-po-foto/index.html': {
        'project_param': 'STL-модель по фото или референсу',
        'local_h2': 'STL-модель по фото в Москве',
        'service_type': '3D-моделирование STL по фото',
        'title': 'STL-модель по фото в Москве — 3D-моделирование под печать | Step3D',
        'description': 'Создание STL-модели по фото, эскизу, скрину или декоративному референсу: адаптация под 3D-печать, разбиение на части, подготовка файлов.',
        'h1': 'STL-модель по фото или референсу',
        'lead': 'Если есть картинка, эскиз, скрин или декоративный референс, но нет 3D-файла — подготовим печатную STL-модель, адаптируем мелкие детали и при необходимости разделим объект на части.',
        'image': '../assets/img/hero-production.webp',
        'blocks': [
            ('Что можно сделать', 'Декоративные рамы, элементы интерьера, реквизит, макеты, корпуса, сувениры, формы для прототипа и объекты по визуальному референсу.', ['STL по фото или картинке', 'модель по эскизу или скрину', 'разбиение крупного объекта на сегменты', 'адаптация орнамента под FDM/SLA']),
            ('Что важно понимать', 'Картинка не равна инженерному чертежу. Мы сохраняем стиль и форму, но технически адаптируем мелкие детали, толщины и рельеф под реальную печать.', ['не обещаем точность без размеров', 'тонкие элементы утолщаем или упрощаем', 'сложный декор лучше согласовывать этапами', 'для крупного объекта планируем сборку']),
            ('Что прислать', 'Для быстрой оценки нужны изображение, примерный размер, желаемый материал или технология печати, срок и понимание, нужна цельная модель или части.', ['референс JPG/PNG/PDF', 'общие габариты в мм/см', 'максимальный размер печати', 'срок и назначение изделия']),
            ('Сроки и цена', 'Базовая STL-заготовка может быть сделана срочно, а полная художественная детализация требует отдельного этапа.', ['экспресс-оценка бесплатно', 'простая STL-модель от 10 000 ₽', 'срочная заготовка от 1 дня', 'детализация и декор — по согласованию']),
            ('Как проходит работа', 'Сначала фиксируем масштаб и ограничения, затем собираем базовую геометрию, добавляем крупный декор, проверяем толщины и экспортируем STL.', ['масштаб и сегменты', 'печатная геометрия', 'проверка тонких мест', 'STL-файлы и рекомендации']),
            ('Что получает клиент', 'Рабочий комплект для печати: STL, превью, комментарии по ориентации/сборке и список мест, которые лучше согласовать перед финальной детализацией.', ['STL-файлы', 'превью модели', 'рекомендации по печати', 'следующий этап при необходимости']),
        ]
    },
    'services/index.html': {
        'project_param': '3D-модель / промышленный дизайн',
        'local_h2': '3D-услуги Step3D в Москве',
        'service_type': '3D-печать, CAD-моделирование, сканирование и прототипирование',
        'title': '3D-услуги в Москве — печать, CAD, STL, сканирование | Step3D',
        'description': 'Основные услуги Step3D: 3D-печать, CAD-моделирование, 3D-сканирование, реверс-инжиниринг, прототипирование, малые серии и образовательные проекты.',
        'h1': 'Услуги Step3D',
        'lead': 'Помогаем пройти путь от идеи, фото или сломанной детали до готового объекта, прототипа, модели или малой серии.',
        'image': '../assets/img/hero-production.webp',
        'blocks': [
            ('3D-печать', 'Детали, макеты, корпуса, декоративные и сценические объекты. Подходит, когда есть STL/STEP/3MF или понятная форма изделия.', ['подбор технологии FDM/SLA', 'подготовка модели к печати', 'базовая постобработка и проверка']),
            ('3D-моделирование', 'Создаём модель по эскизу, фото, размерам или референсам. Сразу учитываем ограничения печати и сборки.', ['модель под производство', 'итерации и уточнение формы', 'подготовка файлов для печати']),
            ('3D-сканирование и реверс-инжиниринг', 'Восстанавливаем геометрию детали или объекта, когда нужно повторить форму, посадки или сложную поверхность.', ['сканирование объекта', 'восстановление CAD-логики', 'модель для печати или производства']),
            ('Прототипы и малые серии', 'Сначала проверяем форму и материал на прототипе, затем считаем повторяемую партию.', ['тестовый образец', 'доработка после проверки', 'расчёт малой серии']),
            ('Образовательные проекты', 'Мастер-классы и проектные занятия по 3D-печати, CAD, сканированию и цифровому производству.', ['формат под возраст участников', 'практический результат занятия', 'методическая и проектная логика']),
            ('Объекты для событий', 'Награды, бутафория, декорации, арт-объекты и презентационные макеты к конкретной дате.', ['визуальная задача', 'контроль сроков', 'подготовка к показу или сцене']),
        ]
    },
    'reverse-engineering/index.html': {
        'project_param': 'Реверсивный инжиниринг / сканирование',
        'local_h2': 'Реверс-инжиниринг деталей в Москве',
        'service_type': 'Реверс-инжиниринг и 3D-сканирование деталей',
        'title': 'Реверс-инжиниринг деталей в Москве — 3D-сканирование и CAD | Step3D',
        'description': '3D-сканирование и реверс-инжиниринг деталей: восстановление геометрии, подготовка CAD-модели и файлов для печати или производства.',
        'h1': 'Реверс-инжиниринг и 3D-сканирование',
        'lead': 'Когда нет чертежа или 3D-модели, но есть физическая деталь, мы помогаем перевести её в цифровую геометрию и подготовить к производству.',
        'image': '../assets/img/case-kawasaki.webp',
        'blocks': [
            ('Когда нужно', 'Подходит для восстановления сломанной детали, повторения формы, доработки посадок или подготовки объекта к изготовлению.', ['деталь снята с производства', 'нужно повторить сложную форму', 'есть объект, но нет CAD-файла']),
            ('Как проходит работа', 'Сначала оцениваем объект, затем сканируем или измеряем критичные зоны, после чего восстанавливаем рабочую модель.', ['осмотр и фото', 'сканирование/измерения', 'CAD-восстановление', 'проверка размеров']),
            ('Что прислать', 'Для первичной оценки достаточно фото, размеров и описания, где деталь используется.', ['3–5 фото с разных сторон', 'общие габариты', 'критичные посадочные размеры']),
        ]
    },
    '3d-printing/index.html': {
        'project_param': '3D-печать детали',
        'local_h2': '3D-печать и прототипирование в Москве',
        'service_type': '3D-печать деталей, прототипов и малых серий',
        'title': '3D-печать в Москве — детали, прототипы и малые серии | Step3D',
        'description': '3D-печать деталей, макетов, корпусов, прототипов и малых серий. Подбор технологии, подготовка модели и базовая постобработка.',
        'h1': '3D-печать и прототипирование',
        'lead': 'Печатаем детали, макеты, корпуса, арт-объекты и прототипы. Если модели нет — поможем подготовить её под печать.',
        'image': '../assets/img/hero-production.webp',
        'blocks': [
            ('Что можно сделать', 'Прототипы, корпуса, крепления, макеты, декоративные элементы, детали для проверки формы и сборки.', ['одиночные детали', 'тестовые образцы', 'малые серии после прототипа']),
            ('Что влияет на цену', 'Размер, материал, сложность модели, плотность заполнения, количество, срочность и постобработка.', ['материал и технология', 'время печати', 'уровень поверхности']),
            ('Срочная замена детали', 'Если сломалась пластиковая деталь оборудования, мебели или корпуса, можно начать с фото и размеров — оценим, получится ли быстро напечатать замену или нужен реверс-инжиниринг.', ['фото поломки и целой зоны', 'габариты и нагрузка', 'желаемый срок замены']),
            ('Какие файлы нужны', 'Лучше всего подходят STL, 3MF, OBJ для печати и STEP для инженерной доработки.', ['STL/3MF/OBJ', 'STEP при доработке', 'фото/эскиз, если файла нет']),
        ]
    },
    'urgent-spare-parts/index.html': {
        'project_param': 'Срочная 3D-печать запчасти по фото',
        'local_h2': 'Срочная 3D-печать запчастей в Москве',
        'service_type': 'Срочная 3D-печать запчастей по фото и размерам',
        'title': 'Срочная 3D-печать запчастей в Москве по фото и размерам | Step3D',
        'description': 'Быстрая оценка и изготовление пластиковой запчасти по фото, размерам, сломанной детали или STL/STEP. 3D-печать, реверс-инжиниринг и прототипирование в Москве.',
        'h1': 'Срочная запчасть по фото, размерам или сломанной детали',
        'lead': 'Если пластиковая деталь сломалась, потерялась или снята с производства — начните с фото и габаритов. Быстро скажем, можно ли напечатать замену, нужен ли реверс-инжиниринг и какой будет порядок бюджета.',
        'image': '../assets/img/proof-engineering.webp',
        'blocks': [
            ('Что прислать для расчёта', 'Не нужен идеальный чертёж. Для первого ответа достаточно понятных вводных, чтобы оценить риск и технологию.', ['3–5 фото детали и места установки', 'общие габариты в миллиметрах', 'где работает деталь и какая нагрузка', 'желаемый срок и количество']),
            ('Какие детали подходят', 'Лучше всего заходят корпуса, крышки, крепления, декоративные элементы, держатели, ручки, заглушки и прототипы для проверки формы.', ['пластиковые элементы оборудования', 'детали мебели и корпусов', 'крепления и переходники', 'единичные замены и малые серии']),
            ('Когда предупредим о риске', 'Мы не обещаем магию: если деталь несёт большую нагрузку, работает при температуре или требует точной посадки, заранее скажем, что нужно проверить.', ['нагрузка и износ', 'температура и химия', 'резьбы, защёлки и посадки', 'нужен тестовый прототип']),
            ('Быстрый сценарий', 'Сначала делаем экспресс-оценку. Если задача реалистична — готовим модель, печатаем тест или сразу рабочую деталь.', ['оценка по фото', 'модель или доработка файла', 'печать прототипа', 'повтор после проверки']),
            ('Что получает клиент', 'Понятный ответ: можно/нельзя, чем печатать, что может сломаться, сколько примерно стоит первый образец и что делать дальше.', ['порядок бюджета', 'срок изготовления', 'рекомендация по материалу', 'следующий шаг без лишней переписки']),
            ('Для бизнеса', 'Подходит мастерским, небольшим производствам, лабораториям, вузам, театрам и командам, которым нужно быстро закрыть единичную техническую проблему.', ['быстрая замена', 'проверка гипотезы', 'малые партии после теста', 'файлы для повторного изготовления']),
        ]
    },
    'workshops/index.html': {
        'project_param': 'Мастер-класс / обучение',
        'local_h2': 'Мастер-классы по 3D-печати и CAD в Москве',
        'service_type': 'Мастер-классы по 3D-печати, CAD и цифровому производству',
        'title': 'Мастер-классы и образовательные проекты — Step3D',
        'description': 'Практические занятия по 3D-печати, CAD, реверс-инжинирингу и цифровому производству для школ, вузов, технопарков и команд.',
        'h1': 'Мастер-классы и образовательные проекты',
        'lead': 'Собираем понятные практические форматы: от знакомства с 3D-печатью до проектной работы с CAD, сканированием и прототипированием.',
        'image': '../assets/img/proof-education.webp',
        'blocks': [
            ('Форматы', 'Мастер-класс, интенсив, проектное занятие, демонстрация оборудования или практикум под событие.', ['для школьников и студентов', 'для технопарков и вузов', 'для мероприятий и проектных смен']),
            ('Что получают участники', 'Понимание полного цикла: идея, цифровая модель, подготовка, печать, проверка результата.', ['практический опыт', 'готовый объект или прототип', 'понимание инженерной логики']),
            ('Что нужно для расчёта', 'Возраст и количество участников, длительность, площадка, желаемый результат и уровень подготовки.', ['возраст группы', 'количество участников', 'длительность и цель занятия']),
        ]
    },
    'cases/index.html': {
        'project_param': 'Объект для события / сцены',
        'local_h2': 'Кейсы 3D-печати и реверс-инжиниринга в Москве',
        'service_type': 'Кейсы 3D-печати, сканирования и прототипирования',
        'title': 'Кейсы Step3D — 3D-печать, сканирование, объекты и обучение',
        'description': 'Кейсы Step3D: награды, реверс-инжиниринг, сценические объекты, арт-прототипы, образовательные проекты и робототехника.',
        'h1': 'Кейсы Step3D',
        'lead': 'Здесь собраны типы задач, по которым проще понять формат работы: входные данные, решение и результат.',
        'image': '../assets/img/case-awards.webp',
        'blocks': [
            ('Награда для премии СТД России', 'Объект для публичного события: дизайн, печать, сборка и подготовка поверхности к конкретной дате.', ['задача: выразительный объект', 'решение: дизайн + печать + сборка', 'результат: готовая награда']),
            ('Kawasaki Puccetti Racing', '3D-сканирование и восстановление сложной геометрии спортивного обвеса.', ['задача: восстановить форму', 'решение: сканирование и reverse engineering', 'результат: цифровая геометрия']),
            ('Фальшсветильники для спектакля', 'Лёгкие сценические объекты для театральной постановки с контролем веса и внешнего вида.', ['задача: сценический эффект', 'решение: печать и подготовка', 'результат: готовые элементы декораций']),
            ('Морские шахматы', 'Предметный арт-объект: идея, 3D-модель, прототип и демонстрационный результат.', ['задача: выразительная форма', 'решение: моделирование и печать', 'результат: прототип для показа']),
        ]
    },

    'cad-modeling/index.html': {
        'project_param': 'CAD-моделирование на заказ',
        'local_h2': 'CAD-моделирование на заказ в Москве',
        'service_type': 'CAD-моделирование деталей и изделий на заказ',
        'title': 'CAD-моделирование на заказ в Москве — модель по эскизу | Step3D',
        'description': 'CAD-моделирование деталей и изделий на заказ: модель по эскизу, размерам, фото или задаче, подготовка к 3D-печати и производству.',
        'h1': 'CAD-моделирование на заказ',
        'lead': 'Создаём инженерные 3D-модели по эскизу, размерам, фото, старой детали или техническому описанию. Сразу учитываем печать, сборку, посадки и ограничения материала.',
        'image': '../assets/img/proof-engineering.webp',
        'blocks': [
            ('Когда нужно CAD-моделирование', 'Когда идеи, фото или детали недостаточно для производства: нужен аккуратный файл, который можно проверить, напечатать или доработать.', ['нет 3D-модели', 'есть только эскиз или фото', 'нужно подготовить STL/STEP', 'важны размеры и посадки']),
            ('Что получаете', 'Рабочую цифровую модель, рекомендации по технологии и список рисков до запуска печати или серии.', ['CAD/STL/STEP по задаче', 'проверка толщин', 'подготовка под печать', 'правки после теста']),
            ('Что прислать', 'Для оценки подойдут фото, габариты, назначение детали, пример материала, срок и количество.', ['фото/эскиз', 'размеры', 'где используется', 'нужный формат файла']),
        ]
    },
    '3d-modeling/index.html': {
        'project_param': '3D-моделирование для печати',
        'local_h2': '3D-моделирование для печати в Москве',
        'service_type': '3D-моделирование для печати по фото, эскизу и размерам',
        'title': '3D-моделирование для печати по фото и эскизу | Step3D',
        'description': '3D-моделирование для печати: модель по фото, эскизу, размерам или референсу, подготовка STL и проверка печатности.',
        'h1': '3D-моделирование для печати',
        'lead': 'Помогаем превратить фото, скрин, эскиз или идею в печатную 3D-модель. Проверяем толщины, масштаб, детализацию и разбиение объекта.',
        'image': '../assets/img/hero-production.webp',
        'blocks': [
            ('Для каких задач', 'Декор, реквизит, макеты, корпуса, прототипы, сувениры, простые технические детали и объекты к событию.', ['модель по фото', 'модель по эскизу', 'STL под FDM/SLA', 'разбиение на части']),
            ('Как снижаем риск', 'До финального экспорта проверяем мелкие элементы, тонкие места, масштаб и ограничения печати.', ['утолщение деталей', 'проверка масштаба', 'ориентация печати', 'рекомендации по сборке']),
            ('Результат', 'STL/OBJ/STEP при необходимости, превью, комментарии по печати и список мест для согласования.', ['STL-файл', 'превью', 'печатаемая геометрия', 'следующий шаг']),
        ]
    },
    '3d-scan/index.html': {
        'project_param': '3D-сканирование детали',
        'local_h2': '3D-сканирование деталей и объектов в Москве',
        'service_type': '3D-сканирование деталей и объектов',
        'title': '3D-сканирование деталей в Москве — объект в цифровую модель | Step3D',
        'description': '3D-сканирование деталей и объектов в Москве: цифровая геометрия, подготовка к реверс-инжинирингу, печати или контролю формы.',
        'h1': '3D-сканирование деталей и объектов',
        'lead': 'Переводим физические детали и объекты в цифровую геометрию, когда нет исходной модели или нужно восстановить форму для реверса и производства.',
        'image': '../assets/img/case-kawasaki.webp',
        'blocks': [
            ('Когда нужно сканирование', 'Если форма сложная, нет чертежа, нужно повторить поверхность или сравнить объект с моделью.', ['сложная поверхность', 'нет CAD-файла', 'нужен реверс', 'контроль формы']),
            ('Что важно', 'Скан даёт геометрию поверхности, а для производства часто нужна инженерная доработка CAD-модели.', ['облако/mesh', 'очистка геометрии', 'CAD-восстановление', 'проверка размеров']),
            ('Что прислать', 'Фото объекта, размеры, материал, назначение и зоны, где важна точность.', ['фото с разных сторон', 'габариты', 'критичные посадки', 'требования к точности']),
        ]
    },
    'small-batch-production/index.html': {
        'project_param': 'Малосерийное производство пластиковых деталей',
        'local_h2': 'Малосерийное производство пластиковых деталей в Москве',
        'service_type': 'Малосерийная 3D-печать пластиковых деталей',
        'title': 'Малосерийная 3D-печать пластиковых деталей | Step3D Москва',
        'description': 'Малосерийное производство пластиковых деталей: тестовый образец, подбор материала, расчёт партии и повторяемая 3D-печать.',
        'h1': 'Малосерийное производство пластиковых деталей',
        'lead': 'После проверки прототипа помогаем посчитать и изготовить небольшую партию деталей: корпуса, крепления, оснастку, макеты и функциональные элементы.',
        'image': '../assets/img/hero-production.webp',
        'blocks': [
            ('Когда подходит малая серия', 'Если нужна партия до запуска литья, тест рынка, запасные элементы или ограниченное производство.', ['10–100+ деталей', 'тест партии', 'корпуса и крепления', 'оснастка и макеты']),
            ('Как работаем', 'Сначала тестовый образец, затем корректировка модели, подбор материала и расчёт повторяемого процесса.', ['прототип', 'правки', 'материал', 'партия']),
            ('Что влияет на цену', 'Размер, материал, время печати, количество, постобработка и требования к повторяемости.', ['габариты', 'материал', 'количество', 'срок']),
        ]
    },
    'industrial-parts/index.html': {
        'project_param': 'Изготовление пластиковых деталей для оборудования',
        'local_h2': 'Изготовление пластиковых деталей для оборудования в Москве',
        'service_type': 'Изготовление пластиковых деталей для оборудования',
        'title': 'Изготовление пластиковых деталей для оборудования | Step3D Москва',
        'description': 'Изготовление пластиковых деталей для оборудования: восстановление по фото или образцу, CAD, реверс-инжиниринг и 3D-печать.',
        'h1': 'Пластиковые детали для оборудования по фото или образцу',
        'lead': 'Помогаем восстановить редкие пластиковые элементы, крепления, крышки, корпуса и переходники, когда нет чертежа или деталь снята с производства.',
        'image': '../assets/img/proof-engineering.webp',
        'blocks': [
            ('Типовые задачи', 'Корпуса, крышки, крепления, заглушки, держатели, переходники, элементы оснастки и вспомогательные детали.', ['деталь снята с производства', 'сломался пластиковый элемент', 'нужен аналог', 'нет чертежа']),
            ('О чём предупреждаем', 'Для силовых, температурных и ответственных узлов заранее оцениваем риск и предлагаем тест.', ['нагрузка', 'температура', 'износ', 'посадки']),
            ('Что нужно для старта', 'Фото, размеры, место установки, условия эксплуатации, количество и желаемый срок.', ['фото детали', 'габариты', 'назначение', 'срок']),
        ]
    },
    'photo-to-cad/index.html': {
        'project_param': 'CAD-модель по фото и размерам',
        'local_h2': 'CAD-модель по фото и размерам в Москве',
        'service_type': 'CAD-модель по фото и размерам',
        'title': 'CAD-модель по фото и размерам — восстановление детали | Step3D',
        'description': 'CAD-модель по фото и размерам: восстановление формы детали, подготовка STEP/STL, проверка посадок и печать прототипа.',
        'h1': 'CAD-модель по фото и размерам',
        'lead': 'Если есть фото детали и основные размеры, можно начать восстановление цифровой модели без чертежа. Для точных посадок подскажем, где нужны дополнительные замеры или сканирование.',
        'image': '../assets/img/proof-engineering.webp',
        'blocks': [
            ('Что можно восстановить по фото', 'Простые корпуса, крепления, декоративные элементы, крышки, держатели и формы с понятной геометрией.', ['фото с 2–3 сторон', 'общие размеры', 'критичные отверстия', 'назначение детали']),
            ('Когда нужен скан', 'Если форма сложная, есть криволинейные поверхности или точные сопряжения, фото лучше дополнить 3D-сканированием.', ['сложная поверхность', 'точные посадки', 'износ', 'много сопряжений']),
            ('Результат', 'STEP/STL, рекомендации по печати, список рисков и план тестовой детали.', ['CAD-модель', 'STL/STEP', 'проверка печати', 'следующий шаг']),
        ]
    },
}


def render_page(data):
    project_query = quote(data.get('project_param', ''))
    cards = []
    for title, text, items in data['blocks']:
        lis = ''.join(f'<li>{item}</li>' for item in items)
        cards.append(f'<article class="card"><h3>{title}</h3><p>{text}</p><ul class="list">{lis}</ul></article>')
    local_section = LOCAL_SECTION.replace('{local_h2}', data.get('local_h2', '3D-печать и прототипирование в Москве'))
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{data['title']}</title>
<meta name="description" content="{data['description']}">
<meta property="og:type" content="website">
<meta property="og:title" content="{data['title']}">
<meta property="og:description" content="{data['description']}">
<meta property="og:url" content="https://amailab.github.io/Step3D/{data.get('canonical','')}">
<meta property="og:image" content="https://amailab.github.io/Step3D/assets/img/og-step3d.webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://amailab.github.io/Step3D/{data.get('canonical','')}">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{BASE_CSS}{HEADER_FOOTER_CSS}{WORLD_CLASS_CSS}
.pwa-install-card{{position:fixed;left:16px;right:16px;bottom:16px;z-index:180;display:grid;grid-template-columns:1fr auto auto;gap:12px;align-items:center;max-width:760px;margin:0 auto;padding:14px 14px 14px 18px;border:1px solid rgba(148,163,184,.36);border-radius:24px;background:rgba(255,255,255,.94);backdrop-filter:blur(18px);box-shadow:0 22px 70px rgba(15,23,42,.22);color:#111827}}.pwa-install-card strong{{display:block;font-weight:900;letter-spacing:-.03em}}.pwa-install-card span{{display:block;color:#475569;font-size:14px;line-height:1.35}}.pwa-install-button{{border:0;border-radius:999px;background:linear-gradient(135deg,#111827,#1d4ed8);color:#fff;font-weight:900;padding:11px 14px}}.pwa-dismiss{{width:34px;height:34px;border:0;border-radius:999px;background:#eef2f7;color:#334155;font-size:22px;line-height:1}}.pwa-install-card--hint{{grid-template-columns:1fr auto}}@media(max-width:640px){{.pwa-install-card{{grid-template-columns:1fr;bottom:calc(86px + env(safe-area-inset-bottom,0px));left:10px;right:10px}}.pwa-dismiss{{position:absolute;right:8px;top:8px}}.pwa-install-button{{width:100%}}}}
</style>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{data['h1']}",
  "serviceType": "{data.get('service_type', data['h1'])}",
  "provider": {{"@type": "LocalBusiness", "name": "Step3D", "areaServed": "Москва", "email": "projects.step3d@gmail.com"}},
  "areaServed": [{{"@type": "City", "name": "Москва"}}, {{"@type": "AdministrativeArea", "name": "Московская область"}}],
  "url": "https://amailab.github.io/Step3D/{data.get('canonical','')}"
}}
</script>
<link rel="manifest" href="../assets/site.webmanifest">
<meta name="theme-color" content="#111827">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Step3D">
<link rel="apple-touch-icon" href="../assets/step3d-logo-192.png">
</head>
<body>
<header aria-label="Верхнее меню сайта" class="site-header"><div class="container header-inner"><a aria-label="Step3D на начало страницы" class="brand" href="../"><span aria-hidden="true" class="brand-mark brand-mark--image"><span class="brand-logo-steel"><img src="../assets/step3d-logo-steel.webp" alt="" width="96" height="82" decoding="async"/></span></span>Step3D</a><nav aria-label="Основная навигация" class="nav"><a href="../#services">Услуги</a><a href="../stl-po-foto/">STL по фото</a><a href="../#cases">Кейсы</a><a href="../gallery/">Галерея</a><a href="../app/">App</a><a href="../account/">Кабинет</a><a href="../#prices">Стоимость</a><a href="../#brief">Заявка</a></nav><div class="header-actions"><a class="btn btn-secondary" href="https://t.me/Step3D_Lab" rel="noopener" target="_blank" data-metric="telegram_click"><img class="link-avatar" src="../assets/avatar-channel-step3d.webp" alt="" width="24" height="24" loading="lazy" decoding="async"><span>Канал</span></a><a class="btn btn-primary" href="../?project={project_query}#brief" data-metric="brief_click">Рассчитать</a></div></div></header>
<nav class="mobile-fixed-menu" aria-label="Закреплённое мобильное меню"><a class="mobile-menu-item" href="../">Главная</a><a class="mobile-menu-item" href="../services/">Услуги</a><a class="mobile-menu-item" href="../gallery/">Галерея</a><a class="mobile-menu-item" href="../app/">App</a><a class="mobile-menu-item" href="../account/">Кабинет</a><a class="mobile-menu-item mobile-menu-item--accent" href="../?project={project_query}#brief" data-metric="brief_click">Заявка</a></nav>
<main>
<section class="hero"><div class="container split"><div><p class="eyebrow">Step3D</p><h1>{data['h1']}</h1><p class="lead">{data['lead']}</p><p><a class="btn primary" href="../?project={project_query}#brief">Оставить заявку</a> <a class="btn ghost" href="../">На главную</a></p></div><div class="image"><img src="{data['image']}" alt="{data['h1']} Step3D" loading="eager"></div></div></section>
<section class="section"><div class="container grid">{''.join(cards)}</div></section>
<section class="section"><div class="container"><p class="eyebrow">Как работаем</p><h2>Понятный цикл без лишней бюрократии</h2><div class="steps"><div class="step"><p class="muted">Получаем фото, размеры, файл или описание задачи.</p></div><div class="step"><p class="muted">Оцениваем технологию, риски, срок и порядок бюджета.</p></div><div class="step"><p class="muted">Делаем модель, сканирование, прототип или печать.</p></div><div class="step"><p class="muted">Проверяем результат и готовим изделие или файлы к передаче.</p></div></div></div></section>
{TRUST_SECTION}
{local_section}
<section class="section"><div class="container cta"><div><h2>Хотите оценить похожую задачу?</h2><p>Пришлите фото, размеры, срок и короткое описание — подскажем технологию, риски и порядок бюджета.</p></div><a class="btn primary" href="../?project={project_query}#brief">Заполнить заявку</a></div></section>
</main>
<footer class="site-footer" aria-label="Карта сайта Step3D"><div class="container"><div class="footer-map"><div class="footer-brand"><strong>Step3D</strong><p>Единое производство 3D-услуг в Москве: AI-оценка задачи, CAD, 3D-сканирование, печать, прототипы и малые серии.</p></div><nav class="footer-col" aria-label="Услуги"><h3>Услуги</h3><ul><li><a href="../services/">Все услуги</a></li><li><a href="../3d-printing/">3D-печать</a></li><li><a href="../reverse-engineering/">Реверс-инжиниринг</a></li><li><a href="../urgent-spare-parts/">Запчасть по фото</a></li><li><a href="../workshops/">Мастер-классы</a></li></ul></nav><nav class="footer-col" aria-label="Разделы сайта"><h3>Разделы</h3><ul><li><a href="../#promise">Как работаем</a></li><li><a href="../#cases">Кейсы</a></li><li><a href="../gallery/">Галерея</a></li><li><a href="../#project-quiz">Квиз подбора</a></li><li><a href="../#prices">Стоимость</a></li><li><a href="../#faq">FAQ</a></li></ul></nav><nav class="footer-col" aria-label="Материалы"><h3>Материалы</h3><ul><li><a href="../cases/">Страница кейсов</a></li><li><a href="../gallery/">Галерея работ</a></li><li><a href="../app/">Step3D App</a></li><li><a href="../account/">Личный кабинет</a></li><li><a href="../articles/">Статьи и гайды</a></li><li><a href="../guide/">Как подготовить задачу</a></li><li><a href="../sitemap.xml">Sitemap.xml</a></li></ul></nav><nav class="footer-col" aria-label="Контакты"><h3>Контакты</h3><ul><li><a href="../#brief">Оставить заявку</a></li><li><a href="https://t.me/step_3d_mngr" rel="noopener" target="_blank" data-metric="telegram_click"><img class="link-avatar" src="../assets/avatar-ai-agent-step3d.webp" alt="" width="24" height="24" loading="lazy" decoding="async">AI-агент</a></li><li><a href="https://t.me/Step3D_Lab" rel="noopener" target="_blank" data-metric="telegram_click"><img class="link-avatar" src="../assets/avatar-channel-step3d.webp" alt="" width="24" height="24" loading="lazy" decoding="async">Канал Step3D</a></li><li><a href="mailto:projects.step3d@gmail.com">projects.step3d@gmail.com</a></li><li><a href="tel:+79959009141">+7 (995) 900-91-41</a></li><li>Москва · ответ обычно в рабочий день</li><li><a href="../privacy/">Политика данных</a></li></ul></nav></div><div class="footer-bottom"><span>© Step3D. 3D-печать · дизайн · прототипирование</span><span>Москва · AI-оценка 3D-задач по фото, эскизу или STL/STEP</span></div></div></footer>
<script src="../assets/pwa-install.js" defer></script>
</body>
</html>'''

for rel, data in PAGES.items():
    # Keep canonical URLs aligned with sitemap.xml: directory pages should use the
    # clean trailing-slash URL, not /index.html, to avoid duplicate URL signals.
    data['canonical'] = rel[:-10] if rel.endswith('/index.html') else rel
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_page(data), encoding='utf-8')

print('created', len(PAGES), 'pages')

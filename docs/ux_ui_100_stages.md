# Step3D UX/UI 10/10 — 100 последовательных этапов

Ориентиры:

- **Ollama** — спокойный минимализм, сильный первый экран, чёрно-белая база, один главный CTA, почти без визуального шума.
- **NotebookLM** — работа с источниками: вводные, файлы, что принято, что нужно дослать, какой ответ будет дальше.

## Принцип 10/10

Не “ещё красивее”, а понятнее:

`Показал деталь → оставил заявку → получил номер S3D → дослал файлы → получил инженерный ответ`

## 100 этапов

### Foundation / Design System
1. Зафиксировать ориентиры Ollama + NotebookLM.
2. Создать 100-stage план.
3. Добавить отдельный `ux-ui-10.css` без ломки старого сайта.
4. Ввести спокойные токены: фон, surface, ink, muted, line.
5. Primary CTA — чёрный, secondary — белый.
6. Убрать визуальное соревнование CTA.
7. Ввести NotebookLM-like блок “вводные / файлы / ответ”.
8. Ввести App как рабочую поверхность, не лендинг.
9. Зафиксировать Viewer как optional tool.
10. Добавить smoke-check для UX/UI 100.

### Home
11. Hero: один смысл — показать деталь.
12. Hero subtitle: один путь.
13. Hero CTA: “Оставить заявку”.
14. Secondary CTA: Telegram или примеры, но слабее.
15. Скрыть лишние proof-блоки на mobile.
16. Сделать flow из 3 шагов.
17. Убрать повторяющиеся CTA ниже первого экрана.
18. Trust оставить компактным.
19. Цена/срок — объяснять как факторы, не шум.
20. Mobile hero 360px.

### App
21. App first screen как продуктовая рабочая область.
22. Заголовок: короткий, человеческий.
23. Avatar как один identity-элемент.
24. Услуги как быстрый выбор, не карточная галерея.
25. Убрать декоративные элементы, не влияющие на заявку.
26. Form = обязательное сейчас.
27. Files = optional later.
28. Project card = next action.
29. Bottom nav = 3 действия.
30. Telegram action = большой и понятный.

### File intake / NotebookLM-like sources
31. “Источники заявки”: фото, STL/STEP, размеры, контекст.
32. Показывать, что уже принято.
33. Показывать, чего не хватает.
34. Показывать, какой ответ даст инженер.
35. Добавить language around “sources”.
36. Сформировать короткий шаблон Telegram.
37. Не требовать идеального ТЗ.
38. Уточнить placeholder’ы.
39. Сохранить viewer import.
40. Проверить fallback.

### Viewer
41. Viewer = инструмент, не продукт.
42. Hero “есть STL?”
43. CTA “сохранить в заявку”.
44. Метрики компактнее.
45. Калькулятор вторичен.
46. Mobile: модель сначала.
47. Панель после модели.
48. Empty state дружелюбнее.
49. CDN fallback не пугает.
50. Viewer handoff smoke.

### Account / Thanks
51. Account = карточка заявки.
52. Не “личный кабинет”.
53. Preview-banner сильный.
54. “Что принято”.
55. “Что дослать”.
56. “Следующий ответ”.
57. Thanks = сразу файлы.
58. Thanks CTA Telegram primary.
59. Thanks account secondary.
60. ProjectId safe.

### Accessibility / Mobile
61. Focus visible.
62. Reduced motion.
63. Mobile menu hidden state.
64. Modal focus trap.
65. Tabs keyboard.
66. Form errors.
67. Touch targets.
68. Safe area.
69. 320px hardening.
70. 390px hardening.

### Visual polish
71. Typography Russian pass.
72. Card radius consistency.
73. Shadow reduction.
74. Border consistency.
75. Background consistency.
76. Badge style.
77. Button hierarchy.
78. Icon restraint.
79. Avatar consistency.
80. Dark section contrast.

### Technical cleanup
81. Reduce `!important` in new layers.
82. Stop adding inline CSS unless necessary.
83. Document future CSS extraction.
84. Check JS syntax.
85. Check HTML links.
86. Check analytics hooks.
87. Check request flow.
88. Check release readiness.
89. Check UX/UI 25.
90. Add UX/UI 100 check.

### Release
91. Docs update.
92. Memory update.
93. Full local gate.
94. Commit.
95. Push.
96. Watch deploy.
97. Live curl proof.
98. Report links.
99. List remaining honest blockers.
100. Next production recommendation.

## Stage 1–10 result

Запущен новый слой `assets/ux-ui-10.css`: более спокойный, Ollama-like и NotebookLM-like. Он не удаляет старые слои, но начинает переводить продукт в интерфейс “заявка как рабочая область”.


## Stages 11–25 — Home + App core flow

- Главный CTA на главной упрощён до `Оставить заявку`.
- Вторичный CTA стал `Посмотреть примеры`.
- Добавлена минималистичная note-строка: без регистрации, без сложного ТЗ, без обещания цены по одному фото.
- App заголовок упрощён: `Опишите деталь. Получите маршрут.`
- Форма стала более человеческой: `Напишите как человеку...`.
- Кнопка формы: `Оставить заявку`.
- Укреплены стили input/project/source blocks.


## Stages 26–45 — Form / files / project card / Viewer handoff

- NotebookLM-like source cards стали пошаговыми: вводные → файлы → ответ.
- Project card теперь прямо говорит: главное действие — дослать файлы.
- File intake визуально спокойнее и понятнее.
- Viewer handoff переименован: `Передать расчёт в заявку`.
- Viewer saved state: расчёт становится источником для оценки.


## Stages 46–65 — Viewer / Account / accessibility core

- Viewer language shifted from tool/dashboard to source for request.
- Viewer extra panels hidden in the 10/10 layer to reduce dashboard feeling.
- Account title shifted to `Карточка заявки S3D`.
- Account copy explicitly says: not a personal cabinet, manager confirms.
- Focus-visible and input font-size reinforced.


## Stages 66–85 — Mobile / performance / visual polish

- Added 390px hardening.
- Reduced heavy hover/transition behavior.
- Added containment/content-visibility hints for cards/images/visuals.
- Improved active state for buttons.
- Softened blur layers.
- Preserved mobile bottom nav safe readability.


## Stages 86–100 — Release

- Added `scripts/check_ux_ui_100.py`.
- Connected UX/UI 100 check to backend template checks.
- Full gate must pass before deploy.
- Honest remaining blocker: old inline CSS still exists; real 10/10 architecture requires extracting page CSS into component files.

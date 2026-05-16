# Step3D Google Apps Script backend

Минимальный backend для заявок Step3D: принимает `FormData`, валидирует контакт/описание, пишет строку в Google Sheet и опционально отправляет Telegram-уведомление.

## Быстрый запуск

1. Создать Google Sheet с листом `Leads`.
2. Открыть `Extensions → Apps Script`.
3. Вставить `Code.gs`.
4. В `STEP3D_CONFIG.SHEET_ID` указать ID таблицы.
5. Deploy → New deployment → Web app.
6. Access: `Anyone with the link`.
7. Скопировать Web App URL.
8. В `assets/lead-config.js` поставить:

```js
primaryEndpoint: 'https://script.google.com/macros/s/.../exec'
```

`formSubmitEndpoint` оставить как fallback.

## Проверка

Открыть Web App URL в браузере — должен вернуться JSON:

```json
{ "ok": true, "service": "Step3D Lead Intake", "status": "ready" }
```

Потом отправить тестовую заявку с сайта/app.

## Важно

- Не хранить приватные файлы в публичном GitHub Pages.
- Для файлов: Drive upload folder / Telegram / отдельный backend upload.
- Apps Script подходит как быстрый MVP, но для production лучше Railway/Firebase/Cloud Run.

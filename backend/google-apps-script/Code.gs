/**
 * Step3D Lead Intake — Google Apps Script Web App
 * Deploy: Apps Script → Deploy → New deployment → Web app → Anyone with the link.
 * Then paste deployment URL into assets/lead-config.js as primaryEndpoint.
 */
const STEP3D_CONFIG = {
  SHEET_ID: 'PASTE_SPREADSHEET_ID_HERE',
  SHEET_NAME: 'Leads',
  TELEGRAM_BOT_TOKEN: '', // optional
  TELEGRAM_CHAT_ID: '',   // optional
};

const STEP3D_COLUMNS = [
  'projectId', 'createdAt', 'status', 'name', 'contact', 'email', 'service', 'projectType',
  'task', 'description', 'deadline', 'quantity', 'dimensions', 'hasFiles', 'files',
  'source', 'page', 'utm_source', 'utm_medium', 'utm_campaign', 'referrer', 'userAgent'
];

function doPost(e) {
  try {
    const payload = normalizePayload_(e);
    validatePayload_(payload);
    const projectId = payload.projectId || makeProjectId_();
    payload.projectId = projectId;
    payload.createdAt = payload.createdAt || payload.submittedAt || new Date().toISOString();
    payload.status = payload.status || 'created';
    appendLead_(payload);
    notifyTelegram_(payload);
    return json_({ ok: true, id: projectId, status: payload.status });
  } catch (err) {
    return json_({ ok: false, error: String(err && err.message ? err.message : err) }, 400);
  }
}

function doGet() {
  return json_({ ok: true, service: 'Step3D Lead Intake', status: 'ready' });
}

function normalizePayload_(e) {
  const data = {};
  if (e && e.parameter) Object.keys(e.parameter).forEach((key) => data[key] = String(e.parameter[key] || '').trim());
  if (e && e.postData && e.postData.contents && String(e.postData.type || '').includes('application/json')) {
    Object.assign(data, JSON.parse(e.postData.contents));
  }
  data.userAgent = (e && e.headers && e.headers['User-Agent']) || '';
  return data;
}

function validatePayload_(payload) {
  const contact = String(payload.contact || '').trim();
  const task = String(payload.task || payload.description || '').trim();
  if (contact.length < 3) throw new Error('contact is required');
  if (task.length < 8) throw new Error('task/description is required');
  if (String(payload.botField || payload._honey || '').trim()) throw new Error('honeypot filled');
}

function appendLead_(payload) {
  const sheet = SpreadsheetApp.openById(STEP3D_CONFIG.SHEET_ID).getSheetByName(STEP3D_CONFIG.SHEET_NAME)
    || SpreadsheetApp.openById(STEP3D_CONFIG.SHEET_ID).insertSheet(STEP3D_CONFIG.SHEET_NAME);
  if (sheet.getLastRow() === 0) sheet.appendRow(STEP3D_COLUMNS);
  sheet.appendRow(STEP3D_COLUMNS.map((key) => payload[key] || ''));
}

function notifyTelegram_(payload) {
  if (!STEP3D_CONFIG.TELEGRAM_BOT_TOKEN || !STEP3D_CONFIG.TELEGRAM_CHAT_ID) return;
  const text = [
    '🦞 Новая заявка Step3D',
    'Номер: ' + payload.projectId,
    'Контакт: ' + (payload.contact || '-'),
    'Услуга: ' + (payload.service || payload.projectType || '-'),
    'Задача: ' + (payload.task || payload.description || '-'),
    'Файлы: ' + (payload.files || payload.hasFiles || '-'),
  ].join('\n');
  UrlFetchApp.fetch('https://api.telegram.org/bot' + STEP3D_CONFIG.TELEGRAM_BOT_TOKEN + '/sendMessage', {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ chat_id: STEP3D_CONFIG.TELEGRAM_CHAT_ID, text })
  });
}

function makeProjectId_() {
  return 'S3D-' + Utilities.formatDate(new Date(), 'GMT', 'yyMMdd') + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();
}

function json_(data, status) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

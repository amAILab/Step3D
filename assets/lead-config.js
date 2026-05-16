window.STEP3D_LEAD_CONFIG = Object.freeze({
  // Сейчас GitHub Pages работает через FormSubmit. Когда будет backend/Apps Script/Railway,
  // заменить primaryEndpoint на новый URL и оставить formSubmitEndpoint как fallback.
  transport: 'formsubmit',
  primaryEndpoint: '',
  formSubmitEndpoint: 'https://formsubmit.co/ajax/projects.step3d@gmail.com',
  managerTelegram: 'https://t.me/step_3d_mngr',
  supportEmail: 'projects.step3d@gmail.com',
  ccEmail: 'stepgptai@gmail.com',
  schemaUrl: '/Step3D/data/lead_schema.json'
});

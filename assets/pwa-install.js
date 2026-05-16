(() => {
  const isStep3D = location.pathname.startsWith('/Step3D/');
  const base = isStep3D ? '/Step3D/' : '/';

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register(`${base}service-worker.js`, { scope: base }).catch(() => {});
    });
  }

  let deferredPrompt = null;
  const isStandalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone;
  if (isStandalone) document.documentElement.classList.add('is-pwa-standalone');

  const createBanner = () => {
    if (isStandalone || document.querySelector('[data-pwa-install]')) return;
    const banner = document.createElement('aside');
    banner.className = 'pwa-install-card';
    banner.setAttribute('data-pwa-install', '');
    banner.innerHTML = `
      <div>
        <strong>Step3D как приложение</strong>
        <span>Добавьте Step3D App на экран телефона: заявка, файлы, кабинет и статус проекта будут под рукой.</span>
      </div>
      <button type="button" class="pwa-install-button">Установить</button>
      <button type="button" class="pwa-dismiss" aria-label="Скрыть">×</button>
    `;
    document.body.appendChild(banner);
    banner.querySelector('.pwa-dismiss')?.addEventListener('click', () => {
      localStorage.setItem('step3d_pwa_dismissed', String(Date.now()));
      banner.remove();
    });
    banner.querySelector('.pwa-install-button')?.addEventListener('click', async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        await deferredPrompt.userChoice.catch(() => null);
        deferredPrompt = null;
        banner.remove();
      } else {
        banner.classList.add('pwa-install-card--hint');
        banner.querySelector('span').textContent = 'На iPhone: Поделиться → На экран «Домой». На Android: меню браузера → Установить приложение.';
      }
    });
  };

  window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault();
    deferredPrompt = event;
    if (!localStorage.getItem('step3d_pwa_dismissed')) createBanner();
  });

  window.addEventListener('load', () => {
    setTimeout(() => {
      if (!localStorage.getItem('step3d_pwa_dismissed')) createBanner();
    }, 1400);
  });
})();

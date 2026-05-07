document.getElementById('year').textContent = new Date().getFullYear();

const requestForm = document.getElementById('requestForm');
if (requestForm) {
  requestForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(requestForm);
    const body = `Заявка Step3D\n\nИмя: ${data.get('name') || ''}\nКонтакт: ${data.get('contact') || ''}\nТип проекта: ${data.get('projectType') || ''}\nСрок: ${data.get('deadline') || ''}\nКоличество: ${data.get('quantity') || ''}\nФайлы/исходники: ${data.get('files') || ''}\n\nЗадача:\n${data.get('task') || ''}\n\nИсточник: сайт Step3D`;
    window.location.href = `mailto:stepgptai@gmail.com?subject=${encodeURIComponent('Заявка Step3D')}&body=${encodeURIComponent(body)}`;
  });
}
const presetButtons = document.querySelectorAll('[data-task-preset]');
if (requestForm && presetButtons.length) {
  const projectType = requestForm.elements.projectType;
  const task = requestForm.elements.task;
  const formStatus = document.getElementById('formStatus');

  presetButtons.forEach((button) => {
    button.addEventListener('click', () => {
      if (projectType && button.dataset.projectType) {
        projectType.value = button.dataset.projectType;
      }

      if (task && button.dataset.taskPreset) {
        task.value = button.dataset.taskPreset;
      }

      if (formStatus) {
        formStatus.textContent = 'Черновик заявки подставлен — добавьте детали, размеры и срок.';
      }

      requestForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
      window.setTimeout(() => { task?.focus(); }, 420);
    });
  });
}


const briefButton = document.getElementById('copyBrief');
if (briefButton) {
  const briefText = `Задача для Step3D:

1. Что нужно сделать:
2. Размеры / примерные габариты:
3. Материал или требования к прочности:
4. Количество экземпляров:
5. Срок:
6. Где будет использоваться изделие:
7. Есть ли фото, эскиз, STL/STEP или чертёж:`;

  briefButton.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(briefText);
      briefButton.textContent = 'Шаблон скопирован';
      briefButton.classList.add('is-copied');
      setTimeout(() => {
        briefButton.textContent = 'Скопировать шаблон';
        briefButton.classList.remove('is-copied');
      }, 2200);
    } catch (error) {
      briefButton.textContent = 'Не удалось скопировать';
      setTimeout(() => { briefButton.textContent = 'Скопировать шаблон'; }, 2200);
    }
  });
}


const storyModal = document.getElementById('storyModal');
const storyImage = document.getElementById('storyImage');
const storyTitle = document.getElementById('storyTitle');
const storyCounter = document.getElementById('storyCounter');
const storyMeta = document.getElementById('storyMeta');
const storySource = document.getElementById('storySource');
const storyPauseButton = document.querySelector('[data-story-pause]');
const storyProgress = document.getElementById('storyProgress');
let storyItems = [];
let storyIndex = 0;
let storyLastFocus = null;
let touchStartX = 0;
let touchStartY = 0;
let storyTimer = null;
let storyPaused = false;
const storyDuration = 5600;
const storyCanAutoplay = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const preloadStoryImage = (index) => {
  if (!storyItems.length) return;
  const item = storyItems[(index + storyItems.length) % storyItems.length];
  const img = new Image();
  img.src = item.src;
};

const clearStoryTimer = () => {
  if (storyTimer) window.clearTimeout(storyTimer);
  storyTimer = null;
};

const scheduleStoryAdvance = () => {
  clearStoryTimer();
  if (!storyCanAutoplay || storyPaused || storyItems.length < 2) return;
  storyTimer = window.setTimeout(() => moveStory(1), storyDuration);
};

const setStoryPaused = (isPaused) => {
  storyPaused = isPaused;
  storyModal?.classList.toggle('is-paused', storyPaused);
  if (storyPauseButton) {
    storyPauseButton.textContent = storyPaused ? 'Продолжить' : 'Пауза';
    storyPauseButton.setAttribute('aria-label', storyPaused ? 'Продолжить story' : 'Поставить story на паузу');
  }
  scheduleStoryAdvance();
};

const renderStory = () => {
  if (!storyItems.length || !storyImage) return;
  const item = storyItems[storyIndex];
  storyImage.src = item.src;
  storyImage.alt = `${item.title}: фото ${storyIndex + 1}`;
  storyTitle.textContent = item.title;
  storyCounter.textContent = item.caption || 'Листайте фото, чтобы увидеть процесс и детали.';
  if (storyMeta) storyMeta.textContent = `${storyIndex + 1} / ${storyItems.length}`;
  if (storySource) storySource.href = item.sourceHref || 'https://t.me/STEP_3D_Lab';
  if (storyProgress) {
    storyProgress.innerHTML = storyItems.map((_, index) => {
      const state = index < storyIndex ? 'is-done' : index === storyIndex ? 'is-current' : '';
      return `<span class="${state}"><i></i></span>`;
    }).join('');
  }
  preloadStoryImage(storyIndex + 1);
  preloadStoryImage(storyIndex - 1);
  scheduleStoryAdvance();
};

const openStory = (button) => {
  const images = (button.dataset.gallery || '').split(',').map((src) => src.trim()).filter(Boolean);
  if (!images.length || !storyModal) return;
  storyLastFocus = document.activeElement;
  const captions = (button.dataset.galleryCaptions || '').split('|').map((text) => text.trim());
  const source = button.closest('article, .media-story-card')?.querySelector('a[href]');
  storyItems = images.map((src, index) => ({
    src,
    title: button.dataset.galleryTitle || 'История проекта',
    caption: captions[index] || '',
    sourceHref: source?.href || 'https://t.me/STEP_3D_Lab'
  }));
  storyIndex = 0;
  storyPaused = false;
  storyModal.classList.add('is-open');
  renderStory();
  storyModal.setAttribute('aria-hidden', 'false');
  document.body.classList.add('story-open');
  storyModal.querySelector('.story-close')?.focus();
};

const closeStory = () => {
  if (!storyModal) return;
  storyModal.classList.remove('is-open');
  storyModal.setAttribute('aria-hidden', 'true');
  document.body.classList.remove('story-open');
  clearStoryTimer();
  storyImage.removeAttribute('src');
  storyItems = [];
  storyLastFocus?.focus();
};

const moveStory = (direction) => {
  if (!storyItems.length) return;
  storyIndex = (storyIndex + direction + storyItems.length) % storyItems.length;
  renderStory();
};

document.querySelectorAll('.story-trigger').forEach((button) => {
  const title = button.dataset.galleryTitle || 'История проекта';
  button.setAttribute('aria-label', `Открыть галерею: ${title}`);
  button.addEventListener('click', () => openStory(button));
});

document.querySelectorAll('[data-story-close]').forEach((button) => button.addEventListener('click', closeStory));
document.querySelectorAll('[data-story-next]').forEach((button) => button.addEventListener('click', () => moveStory(1)));
document.querySelectorAll('[data-story-prev]').forEach((button) => button.addEventListener('click', () => moveStory(-1)));
storyPauseButton?.addEventListener('click', () => setStoryPaused(!storyPaused));
storyModal?.querySelector('.story-viewer')?.addEventListener('mouseenter', () => setStoryPaused(true));
storyModal?.querySelector('.story-viewer')?.addEventListener('mouseleave', () => setStoryPaused(false));
storyImage?.addEventListener('click', (event) => {
  const half = storyImage.getBoundingClientRect().width / 2;
  moveStory(event.offsetX < half ? -1 : 1);
});

storyModal?.addEventListener('touchstart', (event) => {
  touchStartX = event.changedTouches[0].clientX;
  touchStartY = event.changedTouches[0].clientY;
}, { passive: true });

storyModal?.addEventListener('touchend', (event) => {
  const dx = event.changedTouches[0].clientX - touchStartX;
  const dy = event.changedTouches[0].clientY - touchStartY;
  if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy)) {
    moveStory(dx < 0 ? 1 : -1);
  }
  if (dy > 86 && Math.abs(dy) > Math.abs(dx)) {
    closeStory();
  }
}, { passive: true });

document.addEventListener('visibilitychange', () => {
  if (document.hidden) setStoryPaused(true);
});

document.addEventListener('keydown', (event) => {
  if (!storyModal?.classList.contains('is-open')) return;
  if (event.key === 'Escape') closeStory();
  if (event.key.toLowerCase() === 'p') setStoryPaused(!storyPaused);
  if (event.key === 'ArrowLeft') moveStory(-1);
  if (event.key === 'ArrowRight' || event.key === ' ') {
    event.preventDefault();
    moveStory(1);
  }
});


const menuToggle = document.querySelector('.menu-toggle');
const primaryNav = document.getElementById('primaryNav');
const setMenuOpen = (isOpen) => {
  document.body.classList.toggle('menu-open', isOpen);
  menuToggle?.setAttribute('aria-expanded', String(isOpen));
  menuToggle?.setAttribute('aria-label', isOpen ? 'Закрыть меню' : 'Открыть меню');
};
menuToggle?.addEventListener('click', () => setMenuOpen(!document.body.classList.contains('menu-open')));
primaryNav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenuOpen(false)));
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') setMenuOpen(false);
});

const scrollProgressBar = document.getElementById('scrollProgressBar');
const navLinks = [...document.querySelectorAll('.nav a[href^="#"]')];
const navTargets = navLinks
  .map((link) => document.querySelector(link.getAttribute('href')))
  .filter(Boolean);

const updateScrollUX = () => {
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const progress = scrollable > 0 ? Math.min(1, Math.max(0, window.scrollY / scrollable)) : 0;
  if (scrollProgressBar) scrollProgressBar.style.transform = `scaleX(${progress})`;

  let activeId = navTargets[0]?.id;
  navTargets.forEach((section) => {
    if (section.getBoundingClientRect().top <= 130) activeId = section.id;
  });
  navLinks.forEach((link) => link.classList.toggle('is-active', link.getAttribute('href') === `#${activeId}`));
};
updateScrollUX();
window.addEventListener('scroll', updateScrollUX, { passive: true });
window.addEventListener('resize', updateScrollUX);

const taskTextarea = requestForm?.elements.task;
const taskHelper = document.getElementById('taskHelper');
const updateTaskHelper = () => {
  if (!taskTextarea || !taskHelper) return;
  const length = taskTextarea.value.trim().length;
  if (!length) {
    taskHelper.textContent = 'Подсказка: добавьте размер, материал, количество и срок — так расчёт будет быстрее.';
    return;
  }
  if (length < 80) {
    taskHelper.textContent = `Описание пока короткое: ${length} знаков. Добавьте размеры, материал и условия эксплуатации.`;
    return;
  }
  taskHelper.textContent = `Хорошее описание: ${length} знаков. Можно отправлять или добавить фото/чертёж к письму.`;
};
taskTextarea?.addEventListener('input', updateTaskHelper);
updateTaskHelper();

const readinessScore = document.getElementById('readinessScore');
const readinessBar = document.getElementById('readinessBar');
const readinessItems = document.querySelectorAll('[data-readiness-item]');
const updateReadiness = () => {
  if (!requestForm || !readinessScore || !readinessBar || !readinessItems.length) return;
  const data = new FormData(requestForm);
  const checks = {
    type: Boolean(data.get('projectType')),
    task: String(data.get('task') || '').trim().length >= 80,
    deadline: String(data.get('deadline') || '').trim().length >= 3,
    quantity: String(data.get('quantity') || '').trim().length >= 1,
    files: String(data.get('files') || '').trim().length >= 2,
  };
  const done = Object.values(checks).filter(Boolean).length;
  const score = Math.round((done / Object.keys(checks).length) * 100);
  readinessScore.textContent = `${score}%`;
  readinessBar.style.transform = `scaleX(${score / 100})`;
  readinessItems.forEach((item) => {
    item.classList.toggle('is-done', Boolean(checks[item.dataset.readinessItem]));
  });
};
requestForm?.addEventListener('input', updateReadiness);
requestForm?.addEventListener('change', updateReadiness);
presetButtons.forEach((button) => button.addEventListener('click', () => window.setTimeout(updateReadiness, 0)));
updateReadiness();

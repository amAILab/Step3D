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
const storyProgress = document.getElementById('storyProgress');
let storyItems = [];
let storyIndex = 0;
let storyLastFocus = null;
let touchStartX = 0;
let touchStartY = 0;

const preloadStoryImage = (index) => {
  if (!storyItems.length) return;
  const item = storyItems[(index + storyItems.length) % storyItems.length];
  const img = new Image();
  img.src = item.src;
};

const renderStory = () => {
  if (!storyItems.length || !storyImage) return;
  const item = storyItems[storyIndex];
  storyImage.src = item.src;
  storyImage.alt = `${item.title}: фото ${storyIndex + 1}`;
  storyTitle.textContent = item.title;
  storyCounter.textContent = `${storyIndex + 1} / ${storyItems.length}`;
  storyProgress.innerHTML = storyItems.map((_, index) => `<span class="${index <= storyIndex ? 'is-active' : ''}"></span>`).join('');
  preloadStoryImage(storyIndex + 1);
  preloadStoryImage(storyIndex - 1);
};

const openStory = (button) => {
  const images = (button.dataset.gallery || '').split(',').map((src) => src.trim()).filter(Boolean);
  if (!images.length || !storyModal) return;
  storyLastFocus = document.activeElement;
  storyItems = images.map((src) => ({ src, title: button.dataset.galleryTitle || 'История проекта' }));
  storyIndex = 0;
  renderStory();
  storyModal.classList.add('is-open');
  storyModal.setAttribute('aria-hidden', 'false');
  document.body.classList.add('story-open');
  storyModal.querySelector('.story-close')?.focus();
};

const closeStory = () => {
  if (!storyModal) return;
  storyModal.classList.remove('is-open');
  storyModal.setAttribute('aria-hidden', 'true');
  document.body.classList.remove('story-open');
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
document.querySelector('[data-story-prev]')?.addEventListener('click', () => moveStory(-1));
document.querySelector('[data-story-next]')?.addEventListener('click', () => moveStory(1));
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

document.addEventListener('keydown', (event) => {
  if (!storyModal?.classList.contains('is-open')) return;
  if (event.key === 'Escape') closeStory();
  if (event.key === 'ArrowLeft') moveStory(-1);
  if (event.key === 'ArrowRight' || event.key === ' ') {
    event.preventDefault();
    moveStory(1);
  }
});

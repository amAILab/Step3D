document.getElementById('year').textContent = new Date().getFullYear();

const requestForm = document.getElementById('requestForm');
if (requestForm) {
  requestForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(requestForm);
    const body = `Заявка STEP_3D\n\nИмя: ${data.get('name') || ''}\nКонтакт: ${data.get('contact') || ''}\n\nЗадача:\n${data.get('task') || ''}\n\nИсточник: сайт STEP_3D`;
    window.location.href = `mailto:stepgptai@gmail.com?subject=${encodeURIComponent('Заявка STEP_3D')}&body=${encodeURIComponent(body)}`;
  });
}

const briefButton = document.getElementById('copyBrief');
if (briefButton) {
  const briefText = `Задача для STEP_3D:

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

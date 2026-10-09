(() => {
  const button = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#primary-nav');
  if (!button || !navigation) return;
  document.documentElement.classList.add('js');
  const setOpen = (open) => {
    button.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
    button.querySelector('span').textContent = open ? '−' : '+';
  };
  button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
  navigation.addEventListener('click', (event) => {
    if (event.target.closest('a')) setOpen(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      button.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.header-inner')) setOpen(false);
  });
  window.matchMedia('(min-width: 801px)').addEventListener('change', () => setOpen(false));
})();

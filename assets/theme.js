(() => {
  const storageKey = 'appearance';
  const choices = ['system', 'light', 'dark'];
  const root = document.documentElement;
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  const themeColor = document.querySelector('meta[name="theme-color"]');
  const validate = (value) => choices.includes(value) ? value : 'system';
  let appearance = 'system';
  let updateControl = () => {};

  try {
    appearance = validate(localStorage.getItem(storageKey));
  } catch {
    // Appearance still works for this page when browser storage is unavailable.
  }

  const applyAppearance = () => {
    const theme = appearance === 'system' ? (system.matches ? 'dark' : 'light') : appearance;
    root.dataset.appearance = appearance;
    root.dataset.theme = theme;
    if (themeColor) themeColor.content = theme === 'dark' ? '#181c19' : '#f6f5f0';
    updateControl();
  };

  // This script runs before the stylesheet to apply the preference before paint.
  applyAppearance();
  system.addEventListener('change', () => {
    if (appearance === 'system') applyAppearance();
  });
  window.addEventListener('storage', (event) => {
    if (event.key !== storageKey && event.key !== null) return;
    appearance = validate(event.newValue);
    applyAppearance();
  });

  document.addEventListener('DOMContentLoaded', () => {
    const control = document.querySelector('.appearance-control');
    if (!control) return;
    const toggle = control.querySelector('.appearance-toggle');
    const icon = toggle.querySelector('use');
    const current = control.querySelector('#appearance-current');
    const menu = control.querySelector('#appearance-menu');
    const options = [...menu.querySelectorAll('[data-appearance]')];

    updateControl = () => {
      const label = appearance.charAt(0).toUpperCase() + appearance.slice(1);
      icon.setAttribute('href', `#appearance-${appearance}-icon`);
      toggle.title = `Appearance: ${label}`;
      current.textContent = `Current appearance: ${label}`;
      options.forEach((option) => {
        option.setAttribute('aria-checked', String(option.dataset.appearance === appearance));
      });
    };

    const close = (restoreFocus = false) => {
      toggle.setAttribute('aria-expanded', 'false');
      if (restoreFocus) toggle.focus();
      menu.hidden = true;
    };
    const open = (index = choices.indexOf(appearance)) => {
      menu.hidden = false;
      toggle.setAttribute('aria-expanded', 'true');
      options[index].focus();
    };

    toggle.addEventListener('click', () => menu.hidden ? open() : close());
    toggle.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault();
        open(event.key === 'ArrowDown' ? 0 : options.length - 1);
      }
    });
    options.forEach((option) => {
      option.addEventListener('click', () => {
        appearance = option.dataset.appearance;
        applyAppearance();
        try {
          localStorage.setItem(storageKey, appearance);
        } catch {
          // Keep the choice for this page even if persistence is blocked.
        }
        close(true);
      });
    });
    menu.addEventListener('keydown', (event) => {
      const index = options.indexOf(document.activeElement);
      if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
        event.preventDefault();
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? options.length - 1
          : (index + (event.key === 'ArrowDown' ? 1 : -1) + options.length) % options.length;
        options[next].focus();
      } else if (event.key === 'Tab') {
        close(true);
      }
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && !menu.hidden) {
        event.preventDefault();
        close(true);
      }
    });
    document.addEventListener('click', (event) => {
      if (!control.contains(event.target)) close();
    });
    control.addEventListener('focusout', (event) => {
      if (!control.contains(event.relatedTarget)) close();
    });

    updateControl();
    control.hidden = false;
  });
})();

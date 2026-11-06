import { mountShell } from '../components/shell.js';
import { store } from '../lib/store.js';

// "Copy email address": some visitors have no mail app set up, so mailto links do nothing for them.
document.addEventListener('click', async (e) => {
  const btn = e.target.closest('[data-copy-email]');
  if (!btn) return;
  const email = btn.dataset.copyEmail;
  const status = document.querySelector('.copy-status');
  try {
    await navigator.clipboard.writeText(email);
    status.textContent = `Copied ${email}`;
  } catch {
    // Clipboard blocked: select the address so it can be copied by hand.
    const link = document.querySelector('.person-links a[href^="mailto:"]');
    const range = document.createRange();
    range.selectNodeContents(link);
    getSelection().removeAllRanges();
    getSelection().addRange(range);
    status.textContent = 'Press Ctrl+C (or Cmd+C) to copy the selected address.';
  }
});

mountShell('contact');
store.init();

// Header, navigation, diet/allergy bar and the Saved drawer. Shared by every page.
import { store } from '../lib/store.js';
import { foodById } from '../lib/data.js';
import { foodRow } from './ui.js';
import { headerHTML, filtersHTML, icons } from './markup.js';

// Drawer-only state: which list is waiting for confirmation, and what can be undone.
let confirming = null; // 'like' | 'hide' | null
let undo = null;       // { kind, ids } after a clear

const LIST = { like: { title: 'Liked', noun: 'liked' }, hide: { title: 'Hidden', noun: 'hidden' } };

function listHead(kind, count) {
  const { title, noun } = LIST[kind];
  let control = '';
  if (confirming === kind) {
    control = `<span class="confirm" role="group" aria-label="Confirm clearing ${noun} foods">
        <span>Remove all ${count} ${noun} ${count === 1 ? 'food' : 'foods'}?</span>
        <button type="button" class="btn-mini danger" data-clear-confirm="${kind}">Clear</button>
        <button type="button" class="btn-mini" data-clear-cancel>Cancel</button>
      </span>`;
  } else if (count) {
    control = `<button type="button" class="btn-mini" data-clear-ask="${kind}">Clear all</button>`;
  }
  return `<div class="list-head"><h3>${title} <span class="n">${count}</span></h3>${control}</div>`;
}

function undoHTML(kind) {
  if (!undo || undo.kind !== kind) return '';
  const n = undo.ids.length;
  return `<p class="undo" role="status">Cleared ${n} ${LIST[kind].noun} ${n === 1 ? 'food' : 'foods'}.
    <button type="button" class="link-btn inline" data-clear-undo>Undo</button></p>`;
}

function savedHTML() {
  const liked = [...store.liked].map((id) => foodById[id]).filter(Boolean);
  const hidden = [...store.hidden].map((id) => foodById[id]).filter(Boolean);
  return `
    <div class="drawer-head">
      <h2>Saved foods</h2>
      <button type="button" class="icon-btn" data-close-saved aria-label="Close">${icons.close}</button>
    </div>
    <p class="drawer-note">Saved in this browser for now. Sign-in is planned, so your list can follow you to other devices.</p>
    ${liked.length ? '<p class="drawer-link"><a href="./my-foods.html">See what your liked foods cover</a></p>' : ''}
    ${listHead('like', liked.length)}
    ${undoHTML('like')}
    ${liked.length
      ? `<ul class="food-list">${liked.map((f) => foodRow(f, { link: true })).join('')}</ul>`
      : '<p class="empty-note">Tap the heart next to any food to keep it here.</p>'}
    ${listHead('hide', hidden.length)}
    ${undoHTML('hide')}
    ${hidden.length
      ? `<ul class="food-list">${hidden.map((f) => foodRow(f, { link: true })).join('')}</ul>`
      : "<p class=\"empty-note\">Foods you hide won't be suggested anywhere on the site.</p>"}`;
}

export function mountShell(page) {
  const header = document.getElementById('site-header');
  const filters = document.getElementById('filters');
  const dialog = document.createElement('dialog');
  dialog.className = 'drawer';
  dialog.setAttribute('aria-label', 'Saved foods');
  document.body.append(dialog);

  const render = () => {
    header.innerHTML = headerHTML(page, store.liked.size);
    if (dialog.open) dialog.innerHTML = savedHTML();
    if (!filters) return;
    // Keep the chip row's scroll position and keyboard focus across re-renders.
    const scroll = filters.querySelector('.chips')?.scrollLeft ?? 0;
    const focused = document.activeElement?.closest?.('#filters [data-avoid], #filters input');
    const focusKey = focused?.dataset.avoid ?? focused?.value;
    filters.innerHTML = filtersHTML(store.prefs);
    filters.querySelector('.chips').scrollLeft = scroll;
    if (focusKey) filters.querySelector(`[data-avoid="${focusKey}"], input[value="${focusKey}"]`)?.focus();
  };
  store.subscribe(render);
  render();

  // Sticky elements below the filter bar need to know its height.
  if (filters) new ResizeObserver(([entry]) => {
    document.documentElement.style.setProperty('--filters-h', `${Math.ceil(entry.borderBoxSize?.[0]?.blockSize ?? filters.offsetHeight)}px`);
  }).observe(filters);

  filters?.addEventListener('change', (e) => {
    if (e.target.name === 'diet') store.setDiet(e.target.value);
  });

  // One delegated handler for buttons that appear anywhere on the page.
  document.addEventListener('click', (e) => {
    const t = e.target.closest('button, a');
    if (!t) return;
    if (t.tagName === 'A' && dialog.contains(t)) dialog.close();
    if (t.dataset.avoid) store.toggleAvoid(t.dataset.avoid);
    else if (t.hasAttribute('data-clear')) store.clearFilters();
    else if (t.dataset.like) store.toggleLike(t.dataset.like);
    else if (t.dataset.hide) store.toggleHidden(t.dataset.hide);
    else if (t.hasAttribute('data-open-saved')) {
      confirming = null; undo = null;
      dialog.innerHTML = savedHTML();
      dialog.showModal();
    } else if (t.hasAttribute('data-close-saved')) dialog.close();
    else if (t.dataset.clearAsk) {
      confirming = t.dataset.clearAsk; undo = null;
      dialog.innerHTML = savedHTML();
      dialog.querySelector('[data-clear-cancel]')?.focus();
    } else if (t.hasAttribute('data-clear-cancel')) {
      const kind = confirming; confirming = null;
      dialog.innerHTML = savedHTML();
      dialog.querySelector(`[data-clear-ask="${kind}"]`)?.focus();
    } else if (t.dataset.clearConfirm) {
      const kind = t.dataset.clearConfirm;
      confirming = null;
      const ids = store.clearReactions(kind);
      undo = { kind, ids };
      dialog.innerHTML = savedHTML(); // redraw now that Undo is known
      dialog.querySelector('[data-clear-undo]')?.focus();
    } else if (t.hasAttribute('data-clear-undo') && undo) {
      const { kind, ids } = undo; undo = null;
      store.restoreReactions(kind, ids);
      dialog.querySelector(`[data-clear-ask="${kind}"]`)?.focus();
    }
  });
  dialog.addEventListener('click', (e) => {
    if (e.target === dialog) dialog.close(); // click on backdrop
  });
}


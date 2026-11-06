import { store } from '../lib/store.js';
import { mountShell } from '../components/shell.js';
import { esc, symbolHTML, foodRow, reactionButtons } from '../components/ui.js';
import {
  groups, nutrients, nutrientById, foods, foodById, groupById, foodsFor, categories,
  pctDV, perServing, formatAmount, formatPct, measuredCount,
} from '../lib/data.js';
import { isAllowed, excludedReason, allergenWord } from '../lib/filters.js';
import { mailto } from '../config.js';

const grid = document.getElementById('ptable');
const panel = document.getElementById('panel');
const search = document.getElementById('food-search');
const options = document.getElementById('food-options');
const LIST_LIMIT = 12;

// Selection lives in the URL hash so it can be shared: #n=iron, #f=spinach, #c=fruit
let sel = parseHash();
let showExcluded = false;
let showAll = false;

function parseHash() {
  const m = location.hash.match(/^#([nfc])=([\w-]+)$/);
  if (!m) return null;
  const [, kind, id] = m;
  if (kind === 'n' && nutrientById[id]) return { kind, id };
  if (kind === 'f' && foodById[id]) return { kind, id };
  if (kind === 'c' && categories[id]) return { kind, id };
  return null;
}
function select(next) {
  sel = next;
  showExcluded = false;
  showAll = false;
  history.replaceState(null, '', next ? `#${next.kind}=${next.id}` : location.pathname + location.search);
  render();
}

const allowed = (f) => isAllowed(f, store.prefs, store.hidden);
const allowedCount = (nId) => {
  const { high, good } = foodsFor(nId);
  return [...high, ...good].filter(allowed).length;
};

/* ---------- Periodic table ---------- */
function tableHTML() {
  const food = sel?.kind === 'f' ? foodById[sel.id] : null;
  const legend = `
    <div class="legend">
      ${food
        ? `<p class="legend-food"><strong>${esc(food.name)}</strong> lights up what one serving (${esc(food.serving.label)}) gives you.</p>
           <ul class="key"><li><span class="lvl lvl-high"></span>Rich, 20%+ DV</li><li><span class="lvl lvl-good"></span>Good, 10–19%</li></ul>
           <button type="button" class="link-btn" data-clear-sel>Clear food</button>`
        : `<ul class="groups">${groups.map((g) => `<li><span class="sw g-${g.id}"></span>${esc(g.name)}</li>`).join('')}</ul>
           <p class="hint">The small number on each tile counts foods that are rich or good sources and fit your choices.</p>`}
    </div>`;

  const tiles = nutrients.map((n) => {
    const count = allowedCount(n.id);
    const lvl = food ? (food.high.includes(n.id) ? 'high' : food.good.includes(n.id) ? 'good' : 'off') : '';
    const selected = sel?.kind === 'n' && sel.id === n.id;
    const pct = food ? pctDV(food, n.id) : null;
    return `
      <button type="button" class="tile g-${n.group}${count ? '' : ' is-empty'}${lvl ? ` lit-${lvl}` : ''}"
        style="--c:${n.col}; --r:${n.row}" data-n="${n.id}" aria-pressed="${selected}"
        aria-label="${esc(n.name)}, ${food ? (pct == null ? 'not measured' : `${formatPct(pct)} of daily value`) : `${count} ${count === 1 ? 'food' : 'foods'}`}">
        <span class="num">${n.n}</span>
        <span class="count">${food ? (pct == null ? '' : formatPct(pct)) : count}</span>
        <span class="sym">${symbolHTML(n.symbol)}</span>
        <span class="tname">${esc(n.tileName || n.name)}</span>
      </button>`;
  }).join('');

  return legend + tiles;
}

/* ---------- Panel states ---------- */
function emptyPanel() {
  const cats = Object.entries(categories).map(([id, label]) => {
    const all = foods.filter((f) => f.category === id);
    const ok = all.filter(allowed).length;
    return `<li><button type="button" class="cat-btn" data-cat="${id}"${ok ? '' : ' disabled'}>
      <span>${esc(label)}</span><span class="n">${ok}${ok !== all.length ? ` of ${all.length}` : ''}</span></button></li>`;
  }).join('');
  return `
    <div class="panel-empty">
      <h2>Pick a nutrient</h2>
      <p>Select any tile to see which foods are rich in it, how much one serving gives you, and why you need it.</p>
      <p>Or search for a food to light up everything it gives you.</p>
      <h3>Browse ${foods.length} foods by type</h3>
      <ul class="cat-list">${cats}</ul>
    </div>`;
}

function nutrientPanel(n) {
  const g = groupById[n.group];
  const { high, good } = foodsFor(n.id);
  const sortLiked = (a, b) => store.liked.has(b.id) - store.liked.has(a.id);
  const split = (list) => ({
    in: list.filter(allowed).sort(sortLiked),
    out: list.filter((f) => !allowed(f)),
  });
  const H = split(high);
  const G = split(good);
  const outCount = H.out.length + G.out.length;
  let budget = showAll ? Infinity : LIST_LIMIT;
  let hiddenByLimit = 0;

  const section = (title, part) => {
    let items = [...part.in, ...(showExcluded ? part.out : [])];
    if (items.length > budget) { hiddenByLimit += items.length - budget; items = items.slice(0, budget); }
    budget -= items.length;
    return items.length
      ? `<h3>${title}</h3><ul class="food-list">${items.map((f) => foodRow(f, { nutrientId: n.id })).join('')}</ul>`
      : '';
  };
  const none = !H.in.length && !G.in.length;
  const limited = n.source === 'ods';

  return `
    <header class="p-head g-${n.group}">
      <span class="p-tile"><span class="num">${n.n}</span><span class="sym">${symbolHTML(n.symbol)}</span></span>
      <div>
        <h2>${esc(n.name)}</h2>
        <p class="p-group">${esc(g.name)}. Daily Value ${formatAmount(n.dv, n.unit)}${n.id === 'omega3' ? ' (reference)' : ''}</p>
      </div>
      <button type="button" class="icon-btn" data-clear-sel aria-label="Close">×</button>
    </header>
    <p class="role">${esc(n.role)}</p>
    <p class="short"><strong>Without enough:</strong> ${esc(n.short)}</p>
    ${n.note ? `<p class="note">${esc(n.note)}</p>` : ''}
    ${limited ? `<p class="data-limit">Measured for ${measuredCount[n.id]} of ${foods.length} foods.</p>` : ''}
    ${none ? `<p class="gap">None of the foods here are a good source that fits your choices.${outCount ? ' Fortified foods or a supplement may be worth asking a doctor or dietitian about.' : ''}</p>` : ''}
    <p class="col-head"><span>Per serving</span><span>% DV, amount</span></p>
    ${section('Rich sources', H)}
    ${section('Good sources', G)}
    <div class="panel-actions">
      ${hiddenByLimit ? `<button type="button" class="link-btn" data-show-all>Show all ${hiddenByLimit + (showAll ? 0 : LIST_LIMIT)} foods</button>` : ''}
      ${outCount ? `<button type="button" class="link-btn" data-toggle-out>${showExcluded ? 'Hide' : 'Show'} ${outCount} ${outCount === 1 ? 'food' : 'foods'} your choices leave out</button>` : ''}
    </div>
    <p class="p-foot"><a href="./why.html#${n.id}">Read why ${esc(n.name)} matters</a></p>`;
}

function foodPanel(f) {
  const reason = excludedReason(f, store.prefs, store.hidden);
  const byPct = (ids) => [...ids].sort((a, b) => pctDV(f, b) - pctDV(f, a));
  const chips = (ids) => byPct(ids).map((id) => {
    const n = nutrientById[id];
    return `<li><button type="button" class="n-chip g-${n.group}" data-n="${n.id}"><span class="sym">${symbolHTML(n.symbol)}</span>${esc(n.name)}<strong>${formatPct(pctDV(f, id))}</strong></button></li>`;
  }).join('');
  const rowsHTML = nutrients.map((n) => {
    const per = perServing(f, n.id);
    return `<tr class="${per == null ? 'nm' : ''}">
      <th scope="row"><span class="dot g-${n.group}"></span>${esc(n.name)}</th>
      <td>${per == null ? 'not measured' : formatAmount(per, n.unit)}</td>
      <td>${formatPct(pctDV(f, n.id))}</td>
      <td>${formatAmount(f.per100[n.id], n.unit)}${srcMark(f.src?.[n.id])}</td></tr>`;
  }).join('');
  return `
    <header class="p-head p-food">
      <div>
        <h2>${esc(f.name)}</h2>
        <p class="p-group">${esc(categories[f.category])}, ${esc(f.form.toLowerCase())}</p>
        ${f.allergens.length ? `<p class="p-allergens">Contains ${f.allergens.map(allergenWord).join(', ')}</p>` : ''}
      </div>
      ${reactionButtons(f)}
      <button type="button" class="icon-btn" data-clear-sel aria-label="Close">×</button>
    </header>
    ${reason ? `<p class="gap">${esc(reason)}. It still shows here because you searched for it.</p>` : ''}
    ${f.tip ? `<p class="note">${esc(f.tip)}</p>` : ''}
    <p class="serving">One serving: <strong>${esc(f.serving.label)}</strong></p>
    ${f.high.length ? `<h3>Rich in</h3><ul class="n-chips">${chips(f.high)}</ul>` : ''}
    ${f.good.length ? `<h3>Good source of</h3><ul class="n-chips">${chips(f.good)}</ul>` : ''}
    ${!f.high.length && !f.good.length ? '<p class="gap">One serving gives less than 10% of the Daily Value for every nutrient measured.</p>' : ''}
    <details class="all-nutrients">
      <summary>All nutrients</summary>
      <div class="table-scroll">
        <table>
          <thead><tr><th scope="col">Nutrient</th><th scope="col">Serving</th><th scope="col">% DV</th><th scope="col">100 g</th></tr></thead>
          <tbody>${rowsHTML}</tbody>
        </table>
      </div>
    </details>
    ${sourceNote(f)}`;
}

const SRC = {
  fnd: { mark: '†', label: 'USDA Foundation Foods' },
  ods: { mark: '*', label: 'NIH Office of Dietary Supplements' },
};
const srcMark = (k) => (SRC[k] ? `<sup title="From ${SRC[k].label}">${SRC[k].mark}</sup>` : '');

function sourceNote(f) {
  const used = new Set(Object.values(f.src || {}));
  const fnd = f.foundation;
  const lines = [];
  if (fnd && used.has('fnd')) {
    lines.push(`† USDA Foundation Foods #${esc(fnd.fdcId)}${fnd.name ? `, “${esc(fnd.name)}”` : ''}${fnd.published ? `, published ${esc(fnd.published)}` : ''}.`);
  }
  if (used.has('ods')) lines.push('* NIH Office of Dietary Supplements.');
  const allFnd = fnd && nutrients.every((n) => f.per100[n.id] == null || f.src?.[n.id]);
  if (!allFnd) lines.push(`${lines.length ? 'Other values: ' : ''}USDA SR Legacy #${esc(f.usda)}, “${esc(f.usdaName)}”.`);
  const report = mailto(`Nutrayo: possible mistake in ${f.name}`, `Food: ${f.name} (USDA #${f.usda})\nNutrient:\nWhat looks wrong:\nSource (if you have one):\n`);
  return `<div class="source"><p>Sources</p>${lines.map((l) => `<p>${l}</p>`).join('')}<p class="report">Spotted a mistake? <a href="${report}">Email me about it</a></p></div>`;
}

function categoryPanel(id) {
  const list = foods.filter((f) => f.category === id).sort((a, b) => a.name.localeCompare(b.name));
  const ok = list.filter(allowed);
  const out = list.filter((f) => !allowed(f));
  const items = [...ok, ...(showExcluded ? out : [])];
  return `
    <header class="p-head">
      <div><h2>${esc(categories[id])}</h2><p class="p-group">${ok.length} of ${list.length} fit your choices</p></div>
      <button type="button" class="icon-btn" data-clear-sel aria-label="Close">×</button>
    </header>
    ${items.length ? `<ul class="food-list">${items.map((f) => foodRow(f)).join('')}</ul>` : '<p class="gap">None of these fit your choices.</p>'}
    ${out.length ? `<div class="panel-actions"><button type="button" class="link-btn" data-toggle-out>${showExcluded ? 'Hide' : 'Show'} ${out.length} your choices leave out</button></div>` : ''}`;
}

const groupKey = document.getElementById('group-key');
function keyHTML() {
  return sel?.kind === 'f'
    ? `<span><span class="lvl lvl-high"></span>Rich, 20%+ DV</span><span><span class="lvl lvl-good"></span>Good, 10–19%</span><span>Numbers show % DV per serving</span>`
    : groups.map((g) => `<span><span class="sw g-${g.id}"></span>${esc(g.name)}</span>`).join('') + '<span>Number on a tile: foods that fit your choices</span>';
}

function render() {
  grid.innerHTML = tableHTML();
  groupKey.innerHTML = keyHTML();
  grid.classList.toggle('food-mode', sel?.kind === 'f');
  panel.innerHTML = !sel ? emptyPanel()
    : sel.kind === 'n' ? nutrientPanel(nutrientById[sel.id])
    : sel.kind === 'f' ? foodPanel(foodById[sel.id])
    : categoryPanel(sel.id);
  if (sel) panel.insertAdjacentHTML('afterbegin', '<button type="button" class="back-btn" data-back>Back to the table</button>');
  panel.dataset.state = sel ? 'open' : 'empty';
  if (document.activeElement !== search) search.value = sel?.kind === 'f' ? foodById[sel.id].name : '';
}

/* ---------- Search ---------- */
const sorted = foods.slice().sort((a, b) => a.name.localeCompare(b.name));
options.innerHTML = sorted.map((f) => `<option value="${esc(f.name)}"></option>`).join('');
const findFood = (q) => {
  q = q.trim().toLowerCase();
  if (!q) return null;
  return sorted.find((x) => x.name.toLowerCase() === q)
    || sorted.find((x) => x.name.toLowerCase().startsWith(q))
    || sorted.find((x) => x.name.toLowerCase().includes(q))
    || sorted.find((x) => x.usdaName.toLowerCase().includes(q));
};
search.addEventListener('input', () => {
  const f = sorted.find((x) => x.name.toLowerCase() === search.value.trim().toLowerCase());
  if (f) select({ kind: 'f', id: f.id });
});
document.getElementById('search-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const f = findFood(search.value);
  const msg = document.getElementById('search-msg');
  msg.textContent = f || !search.value.trim() ? '' : `No food matches “${search.value.trim()}”. Try a simpler name, like “bean” or “berry”.`;
  if (f) { select({ kind: 'f', id: f.id }); search.blur(); }
});

/* ---------- Events ---------- */
const narrow = () => window.matchMedia('(max-width: 1023px)').matches;
const revealPanel = () => { if (narrow()) panel.scrollIntoView({ behavior: 'smooth', block: 'start' }); };

document.addEventListener('click', (e) => {
  const t = e.target.closest('button');
  if (!t) return;
  if (t.dataset.n) {
    const same = sel?.kind === 'n' && sel.id === t.dataset.n;
    select(same ? null : { kind: 'n', id: t.dataset.n });
    if (!same && t.classList.contains('tile')) revealPanel();
  } else if (t.dataset.food) { select({ kind: 'f', id: t.dataset.food }); grid.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
  else if (t.dataset.cat) select({ kind: 'c', id: t.dataset.cat });
  else if (t.hasAttribute('data-clear-sel')) select(null);
  else if (t.hasAttribute('data-toggle-out')) { showExcluded = !showExcluded; render(); }
  else if (t.hasAttribute('data-show-all')) { showAll = true; render(); }
  else if (t.hasAttribute('data-back')) grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
});
window.addEventListener('hashchange', () => { sel = parseHash(); render(); });
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && sel && !document.querySelector('dialog[open]')) select(null);
});

mountShell('table');
store.subscribe(render);
store.init();
render();

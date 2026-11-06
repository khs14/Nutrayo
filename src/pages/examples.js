import { store } from '../lib/store.js';
import { mountShell } from '../components/shell.js';
import { esc, symbolHTML } from '../components/ui.js';
import { examples, nutrients, nutrientById, foodById } from '../lib/data.js';
import { excludedReason } from '../lib/filters.js';
import { coverage } from '../lib/coverage.js';

const list = document.getElementById('examples');
const onlyFit = document.getElementById('only-fit');

function miniTable(covered) {
  return `
    <div class="mini" role="img" aria-label="Covers ${covered.size} of ${nutrients.length} nutrients">
      ${nutrients.map((n) => {
        const lvl = covered.get(n.id);
        return `<span class="mini-cell g-${n.group}${lvl ? ` on on-${lvl}` : ''}" style="--c:${n.col}; --r:${n.row}" title="${esc(n.name)}${lvl ? (lvl === 'high' ? ': rich' : ': good') : ': not covered'}">${symbolHTML(n.symbol)}</span>`;
      }).join('')}
    </div>`;
}

function render() {
  const cards = examples.map((ex) => {
    const items = ex.foods.map((id) => foodById[id]);
    const conflicts = items
      .map((f) => ({ f, reason: excludedReason(f, store.prefs, store.hidden) }))
      .filter((x) => x.reason);
    if (onlyFit.checked && conflicts.length) return '';
    const { covered, missing } = coverage(ex.foods);
    return `
      <article class="example${conflicts.length ? ' has-conflict' : ''}" id="${ex.id}">
        <div class="ex-text">
          <h2>${esc(ex.title)}</h2>
          <ul class="ex-foods">
            ${items.map((f) => {
              const c = conflicts.find((x) => x.f.id === f.id);
              return `<li${c ? ' class="is-out"' : ''}><a href="./index.html#f=${f.id}">${esc(f.name)}</a>${c ? ` <span class="why-out">${esc(c.reason)}</span>` : ''}</li>`;
            }).join('')}
          </ul>
          <p>${esc(ex.why)}</p>
          <p class="ex-count"><strong>${covered.size} of ${nutrients.length}</strong> nutrients covered.
            ${missing.length ? `Still missing: ${missing.map((id) => esc(nutrientById[id].name)).join(', ')}.` : ''}</p>
        </div>
        ${miniTable(covered)}
      </article>`;
  }).join('');
  list.innerHTML = cards || '<p class="empty-note">No examples fit your current choices. Clear a filter above or turn off “Only show meals that fit my choices”.</p>';
}

onlyFit.addEventListener('change', render);
mountShell('examples');
store.subscribe(render);
store.init();
render();

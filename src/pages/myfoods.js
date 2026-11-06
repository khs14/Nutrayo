// "My foods": what the foods you've liked cover, by food type and by nutrient.
// Liking a food is not the same as eating it, so this is framed as coverage of
// your favourite foods, not a diet assessment.
import { store } from '../lib/store.js';
import { mountShell } from '../components/shell.js';
import { esc, symbolHTML, foodRow } from '../components/ui.js';
import { foods, foodById, nutrients, nutrientById, categories, foodsFor, pctDV, measuredCount } from '../lib/data.js';
import { isAllowed, excludedReason } from '../lib/filters.js';
import { coverage } from '../lib/coverage.js';

const root = document.getElementById('my-foods');
const SUGGESTIONS = 3;

const allowed = (f) => isAllowed(f, store.prefs, store.hidden);
const plural = (n, one, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;

/** Best foods to fill a gap: allowed, not liked yet, highest %DV first. */
function suggestionsFor(nId) {
  const { high, good } = foodsFor(nId);
  return [...high, ...good].filter((f) => allowed(f) && !store.liked.has(f.id)).slice(0, SUGGESTIONS);
}

/** One easy food per type to get started: the one rich in the most nutrients. */
function starterFoods() {
  return Object.keys(categories)
    .map((cat) => foods.filter((f) => f.category === cat && allowed(f)).sort((a, b) => b.high.length - a.high.length)[0])
    .filter(Boolean);
}

function coverageTable(covered) {
  return `
    <div class="mini mini-lg" aria-label="Nutrients covered by your liked foods">
      ${nutrients.map((n) => {
        const lvl = covered.get(n.id);
        return `<a class="mini-cell g-${n.group}${lvl ? ` on on-${lvl}` : ''}" style="--c:${n.col}; --r:${n.row}"
          href="#${lvl ? 'covered' : 'gap'}-${n.id}" title="${esc(n.name)}: ${lvl ? (lvl === 'high' ? 'rich source in your foods' : 'good source in your foods') : 'not covered yet'}">${symbolHTML(n.symbol)}</a>`;
      }).join('')}
    </div>`;
}

function typesSection(liked) {
  const cells = Object.entries(categories).map(([cat, label]) => {
    const inCat = foods.filter((f) => f.category === cat);
    const fits = inCat.filter(allowed);
    const mine = liked.filter((f) => f.category === cat);
    const state = !fits.length ? 'out' : mine.length ? 'done' : 'todo';
    const detail = state === 'out' ? 'Left out by your choices'
      : state === 'done' ? esc(mine.slice(0, 3).map((f) => f.name).join(', ')) + (mine.length > 3 ? ` and ${mine.length - 3} more` : '')
      : `<a href="./index.html#c=${cat}">Browse ${fits.length}</a>`;
    return `
      <li class="type type-${state}">
        <span class="type-mark" aria-hidden="true"></span>
        <div><p class="type-name">${esc(label)}${state === 'done' ? ` <span class="n">${mine.length}</span>` : ''}</p>
        <p class="type-detail">${detail}</p></div>
        <span class="sr-only">${state === 'done' ? 'Liked' : state === 'todo' ? 'Not liked yet' : 'Not in your choices'}</span>
      </li>`;
  });
  const todo = Object.keys(categories).filter((cat) => {
    const fits = foods.some((f) => f.category === cat && allowed(f));
    return fits && !liked.some((f) => f.category === cat);
  });
  return `
    <section class="mf-section" aria-labelledby="types-title">
      <h2 id="types-title">Food types</h2>
      <p class="mf-lead">${todo.length
        ? `You haven't liked anything from ${plural(todo.length, 'type')} yet: ${todo.map((c) => esc(categories[c].toLowerCase())).join(', ')}.`
        : 'You have liked foods from every type that fits your choices.'}</p>
      <ul class="types">${cells.join('')}</ul>
    </section>`;
}

function nutrientSection(liked) {
  const { covered, missing } = coverage(liked.map((f) => f.id));
  const gaps = missing.map((id) => nutrientById[id]);
  const gapHTML = gaps.map((n) => {
    const picks = suggestionsFor(n.id);
    const limited = n.source === 'ods';
    return `
      <li class="gap-item g-${n.group}" id="gap-${n.id}">
        <div class="gap-head">
          <a class="why-tile" href="./index.html#n=${n.id}" aria-label="See all foods for ${esc(n.name)}">${symbolHTML(n.symbol)}</a>
          <div><h3>${esc(n.name)}</h3><p>${esc(n.role)}</p></div>
        </div>
        ${limited ? `<p class="data-limit">Measured for only ${measuredCount[n.id]} foods, so your foods may contain it without it showing here.</p>` : ''}
        ${picks.length
          ? `<p class="col-head"><span>Foods that would cover it</span><span>% DV, amount</span></p><ul class="food-list">${picks.map((f) => foodRow(f, { nutrientId: n.id })).join('')}</ul>`
          : `<p class="gap">No food in the table covers it within your choices.${n.note ? ` ${esc(n.note)}` : ''}</p>`}
      </li>`;
  }).join('');

  const coveredHTML = nutrients.filter((n) => covered.has(n.id)).map((n) => {
    const from = liked
      .filter((f) => f.high.includes(n.id) || f.good.includes(n.id))
      .sort((a, b) => pctDV(b, n.id) - pctDV(a, n.id));
    return `<li id="covered-${n.id}"><span class="dot g-${n.group}"></span><strong>${esc(n.name)}</strong>
      <span class="covered-from">${from.map((f) => esc(f.name)).join(', ')}</span></li>`;
  }).join('');

  return `
    <section class="mf-section" aria-labelledby="nutrients-title">
      <h2 id="nutrients-title">Nutrients</h2>
      <p class="mf-lead">Your liked foods are a rich or good source of <strong>${covered.size} of ${nutrients.length}</strong> nutrients.${gaps.length ? ` ${plural(gaps.length, 'nutrient')} ${gaps.length === 1 ? "isn't" : "aren't"} covered yet.` : ' Every nutrient is covered.'}</p>
      <div class="mf-grid">
        <div class="mf-table">
          ${coverageTable(covered)}
          <ul class="mf-key"><li><span class="key-sw key-high"></span>Rich source</li><li><span class="key-sw key-good"></span>Good source</li><li><span class="key-sw key-none"></span>Not covered yet</li></ul>
        </div>
        <div class="mf-gaps">
          ${gaps.length ? `<h3 class="mf-sub">Not covered yet</h3><ul class="gap-list">${gapHTML}</ul>` : ''}
          ${covered.size ? `<details class="mf-covered"${gaps.length ? '' : ' open'}><summary>Covered (${covered.size})</summary><ul>${coveredHTML}</ul></details>` : ''}
        </div>
      </div>
    </section>`;
}

function render() {
  const allLiked = [...store.liked].map((id) => foodById[id]).filter(Boolean);
  const liked = allLiked.filter(allowed);
  const outside = allLiked.filter((f) => !allowed(f));
  const outsideNote = outside.length
    ? `<p class="note">${plural(outside.length, 'liked food')} ${outside.length === 1 ? "doesn't" : "don't"} fit your current choices and ${outside.length === 1 ? "isn't" : "aren't"} counted: ${outside.map((f) => `${esc(f.name)} (${esc(excludedReason(f, store.prefs, store.hidden).toLowerCase())})`).join(', ')}.</p>`
    : '';

  if (!liked.length) {
    root.innerHTML = `
      ${outsideNote}
      <section class="mf-empty">
        <h2>You haven't liked any foods yet</h2>
        <p>Tap the heart next to a food, here or anywhere on the site, and this page shows which food types and nutrients your liked foods cover, and what to add to fill the gaps.</p>
        <h3>Some to start with, one from each type</h3>
        <ul class="food-list starter">${starterFoods().map((f) => foodRow(f)).join('')}</ul>
        <p><a class="btn btn-primary" href="./index.html">Browse the table</a></p>
      </section>`;
    return;
  }
  root.innerHTML = `
    <p class="mf-summary">Based on <strong>${plural(liked.length, 'liked food')}</strong>. <button type="button" class="link-btn inline" data-open-saved>See or change your list</button></p>
    ${outsideNote}
    ${typesSection(liked)}
    ${nutrientSection(liked)}`;
}

mountShell('mine');
store.subscribe(render);
store.init();
render();


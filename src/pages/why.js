import { store } from '../lib/store.js';
import { mountShell } from '../components/shell.js';
import { esc, symbolHTML } from '../components/ui.js';
import { groups, nutrients, foodsFor, formatAmount } from '../lib/data.js';
import { isAllowed } from '../lib/filters.js';

const root = document.getElementById('why-groups');

const GROUP_INTRO = {
  macro: 'You need these in large amounts every day. They give you energy and the material your body is built from.',
  fat: 'These dissolve in fat, so the body stores them. Eating them with a little fat helps you absorb them.',
  water: 'These dissolve in water and most are not stored for long, so you need them regularly.',
  major: 'Minerals you need in larger amounts, measured in hundreds of milligrams a day.',
  trace: 'Needed in tiny amounts, but nothing else can do their job.',
};

function render() {
  root.innerHTML = groups.map((g) => {
    const items = nutrients.filter((n) => n.group === g.id).map((n) => {
      const top = foodsFor(n.id).high.filter((f) => isAllowed(f, store.prefs, store.hidden)).slice(0, 3);
      return `
        <li class="why-item" id="${n.id}">
          <a class="why-tile g-${n.group}" href="./index.html#n=${n.id}" aria-label="See foods rich in ${esc(n.name)}">${symbolHTML(n.symbol)}</a>
          <div>
            <h3>${esc(n.name)}</h3>
            <p class="dv">Daily Value ${formatAmount(n.dv, n.unit)}${n.id === 'omega3' ? ' (NIH reference)' : ''}</p>
            <p>${esc(n.role)}</p>
            <p class="short"><strong>Without enough:</strong> ${esc(n.short)}</p>
            <p class="srcs">${top.length
              ? `Try ${top.map((f) => `<a href="./index.html#f=${f.id}">${esc(f.name)}</a>`).join(', ')}.`
              : `<a href="./index.html#n=${n.id}">No rich source fits your choices. See all options.</a>`}</p>
          </div>
        </li>`;
    }).join('');
    return `
      <section class="why-group g-${g.id}">
        <h2>${esc(g.name)}</h2>
        <p class="why-group-intro">${GROUP_INTRO[g.id]}</p>
        <ul class="why-list">${items}</ul>
      </section>`;
  }).join('');

  // Honour #iron style links after content renders
  if (location.hash && !render.scrolled) {
    document.getElementById(location.hash.slice(1))?.scrollIntoView();
    render.scrolled = true;
  }
}

mountShell('why');
store.subscribe(render);
store.init();
render();

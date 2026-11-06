// Pure markup for the header and filter bar. No browser APIs, no data imports,
// so the same functions run in two places:
//   - at build/dev time (vite.config.js) to write the header into each HTML page,
//     so it appears instantly with no flash;
//   - in the browser (shell.js) to update it with the user's saved choices.
import { DIETS, AVOIDS } from '../lib/filters.js';
import { CONTACT, mailto } from '../config.js';

export const PAGES = [
  { id: 'table', href: './index.html', label: 'Table' },
  { id: 'mine', href: './my-foods.html', label: 'My foods' },
  { id: 'examples', href: './examples.html', label: 'Examples' },
  { id: 'why', href: './why.html', label: 'Why we need it', short: 'Why' },
  { id: 'contact', href: './contact.html', label: 'Contact' },
];

export const icons = {
  heart: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5s-7.5-4.6-9.3-9.2C1.4 7.9 3.6 4.5 7 4.5c2 0 3.6 1.1 5 2.9 1.4-1.8 3-2.9 5-2.9 3.4 0 5.6 3.4 4.3 6.8-1.8 4.6-9.3 9.2-9.3 9.2z"/></svg>`,
  hide: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3l18 18M10.6 10.6a2 2 0 002.8 2.8M9.9 5.1A9.7 9.7 0 0112 5c5 0 8.5 4.3 9.5 7-.4 1-1.2 2.4-2.4 3.6M6.6 6.6C4.6 7.9 3.1 9.9 2.5 12c1 2.7 4.5 7 9.5 7 1.6 0 3-.4 4.3-1.1"/></svg>`,
  close: `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>`,
};

export function headerHTML(page, likedCount = 0) {
  return `
    <div class="bar">
      <a class="brand" href="./index.html" aria-label="Nutrayo home">
        <span class="brand-tile"><span>Ny</span></span>
        <span class="brand-name">Nutrayo</span>
      </a>
      <nav class="nav" aria-label="Pages">
        ${PAGES.map((p) => `<a href="${p.href}"${p.id === page ? ' aria-current="page"' : ''}>${p.short
          ? `<span class="lbl-long">${p.label}</span><span class="lbl-short" aria-hidden="true">${p.short}</span>`
          : p.label}</a>`).join('')}
      </nav>
      <button type="button" class="saved-btn" data-open-saved aria-haspopup="dialog">
        ${icons.heart}<span>Saved</span>${likedCount ? `<span class="badge">${likedCount}</span>` : ''}
      </button>
    </div>`;
}

export function filtersHTML(prefs = { diet: 'all', avoid: [] }) {
  const { diet, avoid } = prefs;
  const active = diet !== 'all' || avoid.length;
  const eggNote = diet === 'vegetarian' && !avoid.includes('egg');
  return `
    <div class="filters-inner">
      <div class="fgroup diet" role="radiogroup" aria-labelledby="lbl-diet">
        <span class="flabel" id="lbl-diet">Diet</span>
        <div class="seg">
          ${DIETS.map((d) => `
            <label title="${d.hint}"><input type="radio" name="diet" value="${d.id}"${d.id === diet ? ' checked' : ''}><span>${d.label}</span></label>`).join('')}
        </div>
      </div>
      <div class="fgroup avoid" role="group" aria-labelledby="lbl-avoid">
        <span class="flabel" id="lbl-avoid">Avoid</span>
        <div class="chips">
          ${AVOIDS.map((a) => `
            <button type="button" class="chip" data-avoid="${a.id}" aria-pressed="${avoid.includes(a.id)}">${a.label}</button>`).join('')}
          ${active ? '<button type="button" class="clear" data-clear>Clear</button>' : ''}
        </div>
      </div>
      ${eggNote ? '<p class="diet-note">Vegetarian includes eggs and dairy. Choose <strong>Eggs</strong> under Avoid to leave eggs out.</p>' : ''}
    </div>`;
}

const host = (url) => url.replace(/^https?:\/\/(www\.)?/, '').replace(/\/$/, '');

const TOPICS = [
  { symbol: 'Fb', group: 'water', title: 'Feedback or a mistake',
    text: 'Something confusing, broken or missing, or a value that looks wrong. For a value, tell me the food and the nutrient; each food lists its USDA record number, which helps me check it.' },
  { symbol: 'Qu', group: 'major', title: 'Questions',
    text: 'About how Nutrayo works, where the numbers come from, or how to read the table.' },
  { symbol: 'Co', group: 'trace', title: 'Collaborations',
    text: 'Ideas for working together: nutrition data, new features, research or a project that could use Nutrayo.' },
];

export function contactHTML() {
  return `
    <div class="contact-grid">
      <section class="person" aria-labelledby="person-name">
        <div class="person-head">
          <span class="person-tile" aria-hidden="true">${CONTACT.initials}</span>
          <div>
            <h2 id="person-name">${CONTACT.name}</h2>
            <p class="person-role">${CONTACT.role}</p>
          </div>
        </div>
        <dl class="person-links">
          <div><dt>Email</dt><dd><a href="${mailto()}">${CONTACT.email}</a></dd></div>
          <div><dt>LinkedIn</dt><dd><a href="${CONTACT.linkedin}" target="_blank" rel="noopener">${host(CONTACT.linkedin)}<span class="sr-only"> (opens in a new tab)</span></a></dd></div>
          <div><dt>Website</dt><dd><a href="${CONTACT.website}" target="_blank" rel="noopener">${host(CONTACT.website)}<span class="sr-only"> (opens in a new tab)</span></a></dd></div>
        </dl>
        <div class="person-actions">
          <a class="btn btn-primary" href="${mailto()}">Email me</a>
          <button type="button" class="btn btn-quiet" data-copy-email="${CONTACT.email}">Copy email address</button>
        </div>
        <p class="copy-status" role="status" aria-live="polite"></p>
      </section>
      <section class="topics" aria-labelledby="topics-title">
        <h2 id="topics-title">What to write about</h2>
        <ul>
          ${TOPICS.map((t) => `
            <li class="topic g-${t.group}">
              <span class="topic-tile" aria-hidden="true">${t.symbol}</span>
              <div><h3>${t.title}</h3><p>${t.text}</p></div>
            </li>`).join('')}
        </ul>
      </section>
    </div>`;
}

export function footerHTML(page) {
  return `
    <p>Nutrient values: <a href="https://fdc.nal.usda.gov/" rel="noopener">USDA FoodData Central</a>. Biotin, iodine and omega-3: <a href="https://ods.od.nih.gov/factsheets/list-all/" rel="noopener">NIH Office of Dietary Supplements</a>. Daily Values and serving sizes: <a href="https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels" rel="noopener">FDA</a>.</p>
    <p>General information, not medical advice. Nutrient levels vary with variety, season and how food is stored and cooked.</p>
    ${page === 'contact' ? '' : '<p>Spotted a mistake or have an idea? <a href="./contact.html">Contact me</a>.</p>'}`;
}

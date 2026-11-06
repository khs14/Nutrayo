// Small shared rendering helpers.
import { categories, levelOf, pctDV, perServing, nutrientById, formatAmount, formatPct } from '../lib/data.js';
import { store } from '../lib/store.js';
import { excludedReason } from '../lib/filters.js';
import { icons } from './markup.js';

export const esc = (s) =>
  String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

/** "B12" -> B<sub>12</sub>, "ω3" -> ω<sub>3</sub> */
export const symbolHTML = (s) => esc(s).replace(/^([A-Za-zω])(\d+)$/, '$1<sub>$2</sub>');

export { icons };

export function reactionButtons(food) {
  const liked = store.liked.has(food.id);
  const hidden = store.hidden.has(food.id);
  return `
    <span class="reactions">
      <button type="button" class="react like" data-like="${food.id}" aria-pressed="${liked}"
        title="${liked ? 'Remove from liked' : 'Like'}" aria-label="${liked ? 'Unlike' : 'Like'} ${esc(food.name)}">${icons.heart}</button>
      <button type="button" class="react hide" data-hide="${food.id}" aria-pressed="${hidden}"
        title="${hidden ? 'Show this food again' : "Hide, I don't eat this"}" aria-label="${hidden ? 'Unhide' : 'Hide'} ${esc(food.name)}">${icons.hide}</button>
    </span>`;
}

/**
 * One food line. With `nutrientId` it shows %DV and amount per serving.
 * `link` makes the name a link to the table page instead of an in-page button.
 */
export function foodRow(food, { nutrientId, link = false } = {}) {
  const reason = excludedReason(food, store.prefs, store.hidden);
  const level = nutrientId ? levelOf(food, nutrientId) : null;
  const nameEl = link
    ? `<a class="food-name" href="./index.html#f=${food.id}">${esc(food.name)}</a>`
    : `<button type="button" class="food-name" data-food="${food.id}">${esc(food.name)}</button>`;
  const amount = nutrientId
    ? `<span class="amt"><strong>${formatPct(pctDV(food, nutrientId))}</strong><small>${formatAmount(perServing(food, nutrientId), nutrientById[nutrientId].unit)}</small></span>`
    : '';
  return `
    <li class="food-row${reason ? ' is-out' : ''}${store.liked.has(food.id) ? ' is-liked' : ''}">
      ${level ? `<span class="lvl lvl-${level}" title="${level === 'high' ? 'Rich source' : 'Good source'}"></span>` : ''}
      <span class="food-main">
        ${nameEl}
        <span class="food-meta">${esc(nutrientId ? `${food.form}, ${food.serving.label}` : `${categories[food.category]}, ${food.form.toLowerCase()}`)}${reason ? ` <span class="why-out">${esc(reason)}</span>` : ''}</span>
      </span>
      ${amount}
      ${reactionButtons(food)}
    </li>`;
}

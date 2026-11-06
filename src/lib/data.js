// Single place that loads and indexes the static data.
// When you later move data to a database, only this file needs to change.
import nutrientData from '../data/nutrients.json';
import foodData from '../data/foods.json';
import examples from '../data/examples.json';

export const groups = nutrientData.groups;
export const nutrients = nutrientData.nutrients;
export const foods = foodData.foods;
export const categories = foodData.categories;
export const dataSource = foodData.source;
export { examples };

export const nutrientById = Object.fromEntries(nutrients.map((n) => [n.id, n]));
export const foodById = Object.fromEntries(foods.map((f) => [f.id, f]));
export const groupById = Object.fromEntries(groups.map((g) => [g.id, g]));

/** Level of a nutrient in a food: 'high' | 'good' | null */
export function levelOf(food, nutrientId) {
  if (food.high.includes(nutrientId)) return 'high';
  if (food.good.includes(nutrientId)) return 'good';
  return null;
}

/** Amount in one serving, in the nutrient's unit, or null if not measured. */
export function perServing(food, nutrientId) {
  const v = food.per100[nutrientId];
  return v == null ? null : (v * food.serving.g) / 100;
}

/** Percent of the Daily Value in one serving, or null if not measured. */
export function pctDV(food, nutrientId) {
  const amt = perServing(food, nutrientId);
  return amt == null ? null : (amt / nutrientById[nutrientId].dv) * 100;
}

/** Foods that supply a nutrient, highest %DV first. */
export function foodsFor(nutrientId) {
  const byPct = (a, b) => pctDV(b, nutrientId) - pctDV(a, nutrientId);
  const high = foods.filter((f) => f.high.includes(nutrientId)).sort(byPct);
  const good = foods.filter((f) => f.good.includes(nutrientId)).sort(byPct);
  return { high, good };
}

/** How many foods have a measured value for this nutrient. */
export const measuredCount = Object.fromEntries(
  nutrients.map((n) => [n.id, foods.filter((f) => f.per100[n.id] != null).length]),
);

export function formatAmount(value, unit) {
  if (value == null) return '–';
  const v = value >= 100 ? Math.round(value) : value >= 10 ? value.toFixed(1) : value >= 1 ? value.toFixed(2) : value.toFixed(3);
  const s = String(v).includes('.') ? String(v).replace(/0+$/, '').replace(/\.$/, '') : String(v);
  return `${s} ${unit}`;
}

export const formatPct = (p) => (p == null ? '–' : p === 0 ? '0%' : p < 0.5 ? '<1%' : p >= 10 ? `${Math.round(p)}%` : `${p.toFixed(0)}%`);
